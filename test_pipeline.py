import urllib.request
from PIL import Image
import torch
from backend.models.cbam_model import CBAMModel
from backend.utils.image_utils import detect_and_crop_face, preprocess_image

# 1. Download image
url = "https://raw.githubusercontent.com/muxspace/facial_expressions/master/data/images/disgust/100.jpg"
urllib.request.urlretrieve(url, "backend/test_disgust.jpg")

# 2. Pipeline
pil_image = Image.open("backend/test_disgust.jpg").convert("RGB")
cropped = detect_and_crop_face(pil_image)

tensor = preprocess_image(cropped)

model = CBAMModel()
model.load_weights('backend/weights/cbam_v1.pth')
model.eval()

with torch.no_grad():
    logits = model(tensor)
    probs = torch.softmax(logits, dim=1)[0]
    
classes = ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
for c, p in zip(classes, probs):
    print(f"{c}: {p.item()*100:.2f}%")
