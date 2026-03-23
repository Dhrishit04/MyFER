import torch

def normalize_map(saliency):
    smin, smax = saliency.min(), saliency.max()
    return (saliency - smin) / (smax - smin + 1e-8)

def integrated_gradients(model, image, target_class, steps=50):
    """
    Computes Integrated Gradients attribution for the given image and target class.
    """
    model.eval()
    device = next(model.parameters()).device
    baseline = torch.zeros_like(image).to(device)
    scaled_inputs = [
        baseline + (i / steps) * (image - baseline)
        for i in range(steps + 1)
    ]
    grads = []
    for scaled in scaled_inputs:
        scaled = scaled.clone().detach().requires_grad_(True)
        output = model(scaled)
        loss = output[0, target_class]
        model.zero_grad()
        loss.backward()
        grads.append(scaled.grad.detach())
    avg_grad = torch.mean(torch.stack(grads), dim=0)
    attribution = (image - baseline) * avg_grad
    saliency = attribution.abs().sum(dim=1)
    return normalize_map(saliency)
