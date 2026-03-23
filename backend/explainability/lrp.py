import torch
from .integrated_gradients import normalize_map

def lrp_saliency(model, image, target_class):
    """
    Computes a gradient × input approximation of LRP for the given image and target class.
    """
    model.eval()
    device = next(model.parameters()).device
    
    # We move to device explicitly and keep requires_grad
    if image.device != device:
        image = image.to(device)
        
    image = image.clone().detach().requires_grad_(True)
    output = model(image)
    score = output[0, target_class]
    model.zero_grad()
    score.backward()
    relevance = image.grad * image
    saliency = relevance.abs().sum(dim=1)
    return normalize_map(saliency)
