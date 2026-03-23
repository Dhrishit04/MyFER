import torch
from PIL import Image
from models.cbam_model import CBAMModel
from utils.image_utils import detect_and_crop_face, preprocess_image

img = Image.open('test_disgust.jpg').convert('RGB')
cropped = detect_and_crop_face(img)
print(f"Original size: {img.size}, Cropped size: {cropped.size}")

tensor = preprocess_image(cropped)
print(f"Tensor mean: {tensor.mean().item()}, std: {tensor.std().item()}")

model = CBAMModel()
model.load_weights('./weights/cbam_v1.pth')
model.eval()

with torch.no_grad():
    logits = model(tensor)
    probs = torch.softmax(logits, dim=1)[0]
    
classes = ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
for c, p in zip(classes, probs):
    print(f"{c}: {p.item()*100:.2f}%")
