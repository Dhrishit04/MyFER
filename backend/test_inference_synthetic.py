import torch
from models.cbam_model import CBAMModel

model = CBAMModel()
model.load_weights('./weights/cbam_v1.pth')
model.eval()

with torch.no_grad():
    print("Zero:", torch.softmax(model(torch.zeros(1, 3, 224, 224)), dim=1).tolist()[0])
    print("Ones:", torch.softmax(model(torch.ones(1, 3, 224, 224)), dim=1).tolist()[0])
    print("Randn:", torch.softmax(model(torch.randn(1, 3, 224, 224)), dim=1).tolist()[0])
    print("Randn * 10:", torch.softmax(model(torch.randn(1, 3, 224, 224)*10), dim=1).tolist()[0])
