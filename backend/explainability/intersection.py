import torch
import numpy as np
import cv2
from .integrated_gradients import normalize_map

def cluster_saliency_regions(saliency_map, threshold=0.5):
    saliency = saliency_map.squeeze().cpu().numpy()
    binary = (saliency > threshold).astype(np.uint8)
    num_labels, labels = cv2.connectedComponents(binary)
    return num_labels, labels

def extract_bounding_boxes(labels):
    boxes = []
    unique_labels = np.unique(labels)
    for lab in unique_labels:
        if lab == 0:
            continue
        ys, xs = np.where(labels == lab)
        if len(xs) < 10:
            continue
        x_min = int(xs.min())
        x_max = int(xs.max())
        y_min = int(ys.min())
        y_max = int(ys.max())
        boxes.append((x_min, y_min, x_max, y_max))
    return boxes

def saliency_intersection(map1, map2, top_percent=0.2):
    """
    Computes the intersection of the top-k salient regions from two saliency maps.
    """
    map1 = normalize_map(map1)
    map2 = normalize_map(map2)
    k = int(map1.numel() * top_percent)
    thresh1 = torch.topk(map1.flatten(), k).values.min()
    thresh2 = torch.topk(map2.flatten(), k).values.min()
    mask1 = map1 >= thresh1
    mask2 = map2 >= thresh2
    intersection = mask1 & mask2
    score = intersection.sum().float() / k
    return intersection.float(), score.item()
