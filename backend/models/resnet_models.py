import torch
import torch.nn as nn
from torchvision.models import resnet18, resnet50
from .base_model import BaseFERModel
import os

class ResNet18Model(BaseFERModel, nn.Module):
    def __init__(self):
        super(ResNet18Model, self).__init__()
        nn.Module.__init__(self)
        self.num_classes = 7
        self.backbone = resnet18(weights=None)
        
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, self.num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)
        
    def load_weights(self, path: str):
        if not os.path.exists(path):
            print(f"[WARNING] Weights file {path} not found for ResNet18. Proceeding with randomly initialized architecture!")
            return
            
        device = next(self.parameters()).device
        checkpoint = torch.load(path, map_location=device)
        
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

class ResNet50Model(BaseFERModel, nn.Module):
    def __init__(self):
        super(ResNet50Model, self).__init__()
        nn.Module.__init__(self)
        self.num_classes = 7
        self.backbone = resnet50(weights=None)
        
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, self.num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)
        
    def load_weights(self, path: str):
        if not os.path.exists(path):
            print(f"[WARNING] Weights file {path} not found for ResNet50. Proceeding with randomly initialized architecture!")
            return
            
        device = next(self.parameters()).device
        checkpoint = torch.load(path, map_location=device)
        
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
