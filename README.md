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

- **🧠 Advanced Deep Learning**: Utilizes the **CBAM** (Convolutional Block Attention Module) architecture for highly accurate emotion classification.
- **🔍 Explainable AI (XAI)**: Demystifies black-box models using state-of-the-art interpretability techniques:
  - *Integrated Gradients*
  - *Layer-wise Relevance Propagation (LRP)*
  - *Intersection Saliency Maps*
- **⚡ Lightning Fast API**: Backend powered by `FastAPI` and `Uvicorn`, capable of handling asynchronous image processing.
- **🎨 Minimal UI**: A responsive, glassmorphic frontend built with React, Vite, and Tailwind CSS.
- **📊 Real-time Confidence Dashboards**: Visualizes model predictions and XAI heatmaps dynamically.

---

## 🛠️ Technology Stack

| Architecture / Tool | Technologies Used |
| :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS, Recharts |
| **Backend API** | FastAPI, Uvicorn, Pydantic, Python-Multipart |
| **Machine Learning** | PyTorch, Torchvision, OpenCV, NumPy |
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
│   ├── explainability/       # XAI logic (LRP, Integrated Gradients)
│   ├── models/               # PyTorch Model architectures (CBAM)
│   ├── utils/                # Image processing & tensor transformations
│   ├── weights/              # Pretrained `.pth` models
│   └── main.py               # API Entrypoint
├── frontend/                 # React Application
│   ├── src/                  # Components, Pages, and API services
│   ├── public/               # Static assets
│   └── tailwind.config.js    # Styling configuration
├── Dataset/                  # Training Datasets (Ignored in Git)
└── README.md
```

---

<div align="center">
  <i>Built with passion for deep learning and transparency.</i>
</div>
