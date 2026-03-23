import urllib.request
from PIL import Image
import torch
import sys

# Because we are running from backend dir
sys.path.append('.')

from models.cbam_model import CBAMModel
from utils.image_utils import detect_and_crop_face, preprocess_image

def main():
    try:
        url = "https://upload.wikimedia.org/wikipedia/commons/4/44/Abraham_Lincoln_head_on_shoulders_photo_portrait.jpg"
        urllib.request.urlretrieve(url, "test_face.jpg")
        
        pil_image = Image.open("test_face.jpg").convert("RGB")
        print(f"Original Size: {pil_image.size}")
        
        cropped = detect_and_crop_face(pil_image)
        print(f"Cropped Size: {cropped.size}")
        
        tensor = preprocess_image(cropped)
        print(f"Tensor Shape: {tensor.shape}, Mean: {tensor.mean().item():.4f}, Std: {tensor.std().item():.4f}")
        
        model = CBAMModel()
        model.load_weights('./weights/cbam_v1.pth')
        model.eval()

        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0]
            
        classes = ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
        print("Predictions:")
        for c, p in zip(classes, probs):
            print(f"{c}: {p.item()*100:.2f}%")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
