<div align="center">
  
  <img src="https://readme-typing-svg.herokuapp.com?font=Inter&weight=700&size=36&pause=1000&color=3B82F6&center=true&vCenter=true&width=800&height=80&lines=MyFER:+Facial+Emotion+Recognition;Powered+by+Explainable+AI+(XAI);Deep+Learning+meets+Interpretability" alt="Typing SVG" />

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  </p>

  <h3>A modern, full-stack application for detecting and explaining human emotions in real-time.</h3>
</div>

---

## ✨ Features

- **🧠 Multi-Model Architecture**: Supports **four** deep learning models out of the box, selectable dynamically from the UI:
  - **CBAM** — ResNet18 with Convolutional Block Attention Module
  - **VGG16** — Classic VGG16 architecture
  - **ResNet50** — Deep 50-layer Residual Network
  - **ResNet18** — Lightweight 18-layer Residual Network
- **🔍 Explainable AI (XAI)**: Demystifies black-box models using state-of-the-art interpretability techniques:
  - *Integrated Gradients*
  - *Layer-wise Relevance Propagation (LRP)*
  - *Intersection Saliency Maps*
- **👤 Automatic Face Detection**: Uses OpenCV's Haar Cascade to detect and crop faces from uploaded images before inference.
- **⚡ Lightning Fast API**: Backend powered by `FastAPI` and `Uvicorn`, capable of handling asynchronous image processing.
- **🎨 Minimal UI**: A responsive, glassmorphic frontend built with React and Vite.
- **📊 Real-time Confidence Dashboards**: Visualizes model predictions, XAI heatmaps, and bounding boxes dynamically.
- **🔌 Plug-and-Play Models**: Adding a new model is as simple as creating a PyTorch wrapper and registering it in the model registry — the frontend automatically picks it up.

---

## 🧪 Supported Models

All models are trained on the **RAF-DB** dataset with 7 emotion classes: *Surprise, Fear, Disgust, Happy, Sad, Angry, Neutral*.

| Model | Architecture | Test Accuracy | Status |
| :--- | :--- | :---: | :---: |
| **CBAM** | ResNet18 + CBAM | ~83% | ✅ Trained |
| **VGG16** | VGG16 | ~83% | ✅ Trained |
| **ResNet50** | ResNet50 | ~85% | ✅ Trained |
| **ResNet18** | ResNet18 | ~84% | ✅ Trained |

---

## 🛠️ Technology Stack

| Architecture / Tool | Technologies Used |
| :--- | :--- |
| **Frontend** | React, Vite, Vanilla CSS, Recharts, Lucide Icons |
| **Backend API** | FastAPI, Uvicorn, Pydantic, Python-Multipart |
| **Machine Learning** | PyTorch, Torchvision, OpenCV, NumPy, Pillow |
| **Environment** | Python 3.11, Node.js |

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Dhrishit04/MyFER.git
cd MyFER
```

### 2. Backend Setup (FastAPI + PyTorch)
Make sure you have Python 3.11 installed.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Start the API Server:**
```bash
uvicorn main:app --reload --port 8000
```
*The backend will be available at `http://localhost:8000/docs` (interactive Swagger UI).*

### 3. Frontend Setup (React + Vite)
Open a new terminal window.

```bash
cd frontend
npm install
```

**Start the Development Server:**
```bash
npm run dev
```
*The web app will launch at `http://localhost:5173`.*

---

## 📂 Project Structure

```text
MyFER/
├── backend/                  # FastAPI Application
│   ├── explainability/       # XAI logic (LRP, Integrated Gradients, Intersection)
│   ├── models/               # PyTorch model wrappers (CBAM, VGG16, ResNet18, ResNet50)
│   │   ├── base_model.py     # Abstract base class for all FER models
│   │   ├── cbam_model.py     # CBAM attention-based model
│   │   ├── vgg16_model.py    # VGG16 model
│   │   ├── resnet_models.py  # ResNet18 & ResNet50 models
│   │   └── model_registry.py # Central model registry (plug-and-play)
│   ├── utils/                # Image processing & tensor transformations
│   ├── weights/              # Pretrained .pth model weights
│   └── main.py               # API Entrypoint
├── frontend/                 # React Application
│   ├── src/                  # Components, Pages, and API services
│   └── public/               # Static assets
├── Models/                   # Training notebooks (.ipynb) & raw weights
└── README.md
```

---

## 🔌 Adding a New Model

1. Create a new PyTorch wrapper in `backend/models/` inheriting from `BaseFERModel` and `nn.Module`.
2. Implement `__init__`, `forward`, and `load_weights` methods.
3. Add an entry to the `MODELS` dictionary in `backend/models/model_registry.py`.
4. Place the trained `.pth` weights in `backend/weights/`.
5. Restart the server — the new model automatically appears in the frontend dropdown!

---

<div align="center">
  <i>Built with passion for deep learning and transparency.</i>
</div>
