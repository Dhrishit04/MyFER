import requests
import json
import base64
import sys

URL = "http://localhost:8000/predict"

def test_inference(image_path):
    print(f"Testing with image: {image_path}")
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {"model_id": "cbam_v1"}
        response = requests.post(URL, files=files, data=data)

    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("Success! Inference response:")
    print(f"Predicted: {data['predicted_emotion']} ({data['confidence']:.4f})")
    print(f"Class Scores: {json.dumps(data['all_scores'], indent=2)}")
    print(f"Intersection Score: {data['intersection_score']:.4f}")

    # Check that base64 images exist
    images = ["ig_image_b64", "lrp_image_b64", "intersection_image_b64", "chart_image_b64"]
    for img in images:
        b64 = data.get(img)
        if b64:
            print(f"- {img} length: {len(b64)} chars")
        else:
            print(f"- ERROR: Missing {img}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_inference(sys.argv[1])
    else:
        print("Provide image path to test")
