import torch
from models.cbam_model import CBAMModel

def main():
    model = CBAMModel()
    model.load_weights('./weights/cbam_v1.pth')

    x = torch.randn(4, 3, 224, 224)
    
    model.train()
    with torch.no_grad():
        out_train = torch.softmax(model(x), dim=1).tolist()
        
    model.eval()
    with torch.no_grad():
        out_eval = torch.softmax(model(x), dim=1).tolist()
        
    print("--- TRAIN MODE (Uses Batch BN Stats) ---")
    for row in out_train: print(row)
        
    print("--- EVAL MODE (Uses Saved BN Stats) ---")
    for row in out_eval: print(row)

if __name__ == "__main__":
    main()
