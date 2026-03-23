import os
import io
import base64
import torch 
from torchvision import transforms
from PIL import Image, ImageDraw
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')  # use non-interactive backend
import matplotlib.pyplot as plt

# The transformation pipeline replicating the training setting
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# Inference transforms
inference_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])

def preprocess_image(pil_image: Image.Image) -> torch.Tensor:
    # Ensure image is RGB (ImageFolder does this by default)
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    tensor = inference_transforms(pil_image)
    return tensor.unsqueeze(0)  # Shape: (1, 3, 224, 224)

def tensor_to_pil(tensor: torch.Tensor) -> Image.Image:
    # Reverse of normalization
    tensor = tensor.clone().detach().cpu().squeeze(0)
    for t, m, s in zip(tensor, MEAN, STD):
        t.mul_(s).add_(m)
    tensor = torch.clamp(tensor, 0, 1)
    # Convert to PIL
    np_img = tensor.permute(1, 2, 0).numpy()
    np_img = (np_img * 255).astype(np.uint8)
    return Image.fromarray(np_img)

def overlay_heatmap(original_pil: Image.Image, saliency_map_2d: torch.Tensor, alpha=0.6) -> Image.Image:
    """
    Applies JET colormap to the 2D tensor saliency map and overlays on the original image (resized).
    """
    # Resize original immediately to match heatmap size (224x224)
    original_pil = original_pil.resize((224, 224)).convert("RGB")
    orig_np = np.array(original_pil)

    # Convert saliency map to numpy and scale to [0, 255] uint8
    saliency_np = saliency_map_2d.clone().detach().cpu().squeeze().numpy()
    # Handle NaN
    saliency_np = np.nan_to_num(saliency_np)
    smin, smax = saliency_np.min(), saliency_np.max()
    if smax > smin:
        saliency_np = (saliency_np - smin) / (smax - smin)
    saliency_np = (saliency_np * 255).astype(np.uint8)

    # Invert the saliency_np so high values are red in typical JET mapping?
    # JET maps 0=blue, 255=red. High attribution should be red (high relevance).
    heatmap = cv2.applyColorMap(saliency_np, cv2.COLORMAP_JET)

    # OpenCV produces BGR, convert to RGB
    heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    # Blend
    blended = cv2.addWeighted(orig_np, 1 - alpha, heatmap_rgb, alpha, 0)
    return Image.fromarray(blended)

def generate_bar_chart(emotion_classes: list, scores_dict: dict) -> Image.Image:
    """
    Generates a dark-themed horizontal bar chart of confidence scores using matplotlib.
    """
    emotions = list(scores_dict.keys())
    scores = list(scores_dict.values())

    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Dark theme settings
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')
    
    y_pos = np.arange(len(emotions))
    bars = ax.barh(y_pos, scores, align='center', color='#00ffff') # Cyan accent
    
    ax.set_yticks(y_pos, labels=emotions, color='white')
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Confidence', color='white')
    
    # Hide spine
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444444')
    ax.spines['bottom'].set_color('#444444')
    ax.tick_params(colors='white')
    
    # Annotate bars with percentage
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width*100:.1f}%',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center', color='white', fontsize=9)
    plt.tight_layout()
    
    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)

def draw_bounding_boxes(original_pil: Image.Image, boxes: list) -> Image.Image:
    """
    Draws red bounding boxes on a copy of the original image based on a list of (x_min, y_min, x_max, y_max).
    """
    img_copy = original_pil.resize((224, 224)).convert("RGB")
    draw = ImageDraw.Draw(img_copy)
    
    for box in boxes:
        draw.rectangle(box, outline="red", width=2)
        
    return img_copy

def pil_to_base64(pil_image: Image.Image) -> str:
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Initialize Face Cascade globally
cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)

def detect_and_crop_face(pil_image: Image.Image) -> Image.Image:
    """
    Detects the largest face in an image and crops it. 
    Returns the original image if no face is detected.
    """
    # Convert PIL Image to OpenCV format (BGR)
    open_cv_image = np.array(pil_image.convert('RGB'))
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        return pil_image  # Fallback to original image if no face found
        
    # Find the largest face (by area)
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    
    # Crop the face with a slight margin
    margin_ratio = 0.2
    margin_w = int(w * margin_ratio)
    margin_h = int(h * margin_ratio)
    
    x_start = max(0, x - margin_w)
    y_start = max(0, y - margin_h)
    x_end = min(open_cv_image.shape[1], x + w + margin_w)
    y_end = min(open_cv_image.shape[0], y + h + margin_h)
    
    cropped = open_cv_image[y_start:y_end, x_start:x_end]
    
    # Convert back to RGB PIL Image
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cropped_rgb)
