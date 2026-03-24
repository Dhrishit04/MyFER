import torch
import torch.nn as nn
from torchvision.models import vgg16
from .base_model import BaseFERModel
import os

class VGG16Model(BaseFERModel, nn.Module):
    def __init__(self):
        super(VGG16Model, self).__init__()
        nn.Module.__init__(self)
        
        self.num_classes = 7
        # Load base architecture without pretrained weights (we load our own state_dict)
        self.backbone = vgg16(weights=None)
        
        # Replicate the modification made in the training notebook
        num_features = self.backbone.classifier[6].in_features
        self.backbone.classifier[6] = nn.Linear(num_features, self.num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # VGG16 standard forward pass
        return self.backbone(x)
        
    def load_weights(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model weights not found at {path}")
            
        device = next(self.parameters()).device
        checkpoint = torch.load(path, map_location=device)
        
        # Handle cases where it is nested or just the direct state_dict
        if isinstance(checkpoint, dict) and "model" in checkpoint:
            state_dict = checkpoint["model"]
        else:
            state_dict = checkpoint
            
        new_state_dict = {}
        for k, v in state_dict.items():
            if not k.startswith("backbone."):
                new_state_dict[f"backbone.{k}"] = v
            else:
                new_state_dict[k] = v
                
        self.load_state_dict(new_state_dict)
