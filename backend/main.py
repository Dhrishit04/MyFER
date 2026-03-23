import os
import torch
import torch.nn.functional as F
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import io
from PIL import Image

# Import models, explainability, utils
from models.model_registry import MODELS
from utils.image_utils import (
    preprocess_image,
    overlay_heatmap,
    generate_bar_chart,
    pil_to_base64,
    detect_and_crop_face,
    draw_bounding_boxes
)
from explainability.integrated_gradients import integrated_gradients
from explainability.lrp import lrp_saliency
from explainability.intersection import (
    saliency_intersection, 
    cluster_saliency_regions, 
    extract_bounding_boxes
)

# Load .env
load_dotenv()
DEVICE = os.environ.get("DEVICE", "cpu")

app = FastAPI(title="FER Web Application API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Loading models...")
    for model_id, model_info in MODELS.items():
        try:
            model_class = model_info["class"]
            model_instance = model_class()
            model_instance.load_weights(model_info["weights_path"])
            model_instance.to(DEVICE)
            model_instance.eval()
            MODELS[model_id]["instance"] = model_instance
            print(f"Loaded {model_id} successfully.")
        except Exception as e:
            print(f"Failed to load {model_id} from {model_info['weights_path']}: {e}")

@app.get("/models")
def get_models():
    models_list = []
    for model_id, info in MODELS.items():
        # Only surface models that successfully loaded
        if info["instance"] is not None:
            models_list.append({
                "id": model_id,
                "name": info["name"],
                "description": info["description"],
                "emotion_classes": info["emotion_classes"]
            })
    return models_list

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    model_id: str = Form(...)
):
    # 1. Validate Image
    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only JPG and PNG files are supported.")
    
    content = await image.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 10MB.")
        
    if model_id not in MODELS or MODELS[model_id]["instance"] is None:
        raise HTTPException(status_code=400, detail="Invalid or unloaded model ID.")
        
    # Get model and classes
    model_info = MODELS[model_id]
    model = model_info["instance"]
    classes = model_info["emotion_classes"]
    
    try:
        pil_image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    # 1.5 Extract Face
    pil_image = detect_and_crop_face(pil_image)

    # 2. Preprocess
    input_tensor = preprocess_image(pil_image).to(DEVICE)
    
    # 3. Inference
    with torch.no_grad():
        logits = model(input_tensor)
        probs = F.softmax(logits, dim=1)[0]
        
    top_prob_val, top_class_idx = torch.max(probs, dim=0)
    predicted_emotion = classes[top_class_idx.item()]
    confidence = top_prob_val.item()
    
    # Build all scores dict
    all_scores = {classes[i]: probs[i].item() for i in range(len(classes))}
    
    # 4. IG Saliency
    ig_map = integrated_gradients(model, input_tensor, top_class_idx.item())
    ig_pil = overlay_heatmap(pil_image, ig_map)
    
    # 5. LRP Saliency
    lrp_map = lrp_saliency(model, input_tensor, top_class_idx.item())
    lrp_pil = overlay_heatmap(pil_image, lrp_map)
    
    # 6. Saliency Intersection
    intersection_map, int_score = saliency_intersection(ig_map, lrp_map)
    int_pil = overlay_heatmap(pil_image, intersection_map)
    
    # 6.5 Bounding Boxes
    num_labels, labels = cluster_saliency_regions(intersection_map, threshold=0.5)
    boxes = extract_bounding_boxes(labels)
    boxed_pil = draw_bounding_boxes(pil_image, boxes)
    
    # 7. Confidence Bar Chart
    chart_pil = generate_bar_chart(classes, all_scores)
    
    # 8. Base64 encoding
    ig_b64 = pil_to_base64(ig_pil)
    lrp_b64 = pil_to_base64(lrp_pil)
    int_b64 = pil_to_base64(int_pil)
    chart_b64 = pil_to_base64(chart_pil)
    boxed_b64 = pil_to_base64(boxed_pil)
    
    return {
        "predicted_emotion": predicted_emotion,
        "confidence": confidence,
        "all_scores": all_scores,
        "ig_image_b64": ig_b64,
        "lrp_image_b64": lrp_b64,
        "intersection_image_b64": int_b64,
        "chart_image_b64": chart_b64,
        "boxed_image_b64": boxed_b64,
        "intersection_score": int_score
    }
