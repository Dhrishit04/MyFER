from models.cbam_model import CBAMModel
from models.vgg16_model import VGG16Model
from models.resnet_models import ResNet18Model, ResNet50Model

MODELS = {
    "cbam_v1": {
        "id": "cbam_v1",
        "instance": None,
        "class": CBAMModel,
        "weights_path": "./weights/cbam_v1.pth",
        "name": "CBAM Model (v1)",
        "description": "ResNet18 CBAM-based CNN trained on FER2013/RAF-DB dataset",
        "emotion_classes": ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
    },
    "vgg16_v1": {
        "id": "vgg16_v1",
        "instance": None,
        "class": VGG16Model,
        "weights_path": "./weights/vgg16_v1.pth",
        "name": "VGG16 Model",
        "description": "Standard VGG16 architecture trained on RAF-DB",
        "emotion_classes": ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
    },
    "resnet50_v1": {
        "id": "resnet50_v1",
        "instance": None,
        "class": ResNet50Model,
        "weights_path": "./weights/resnet50_v1.pth",
        "name": "ResNet50 Model",
        "description": "Deep ResNet50 architecture trained on RAF-DB",
        "emotion_classes": ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
    },
    "resnet18_untrained": {
        "id": "resnet18_untrained",
        "instance": None,
        "class": ResNet18Model,
        "weights_path": "./weights/empty.pth",
        "name": "ResNet18 Model",
        "description": "Standard ResNet18 architecture",
        "emotion_classes": ["Surprise", "Fear", "Disgust", "Happy", "Sad", "Angry", "Neutral"]
    }
}
