---
title: IModel Face Estimator
emoji: 👁️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
---

# I Model (Face Detection & Age/Glow Estimator)


A premium, modern web application that analyzes a user's face (via live webcam or image upload) to estimate their **age** and **skin glow index** (brightness, texture smoothness, and color uniformity). Based on the results, it generates personalized, age-customized skincare routines and lifestyle recommendations (**Khao, Piyo, Lagao**) to protect the skin against dust, pollution, and pimples.

Built with **Python (FastAPI)**, **OpenCV**, **MediaPipe**, and **DeepFace**.

---

## ✨ Features

- **Live Webcam Capture & File Upload**: Capture snapshots directly using your browser camera or upload high-quality face images.
- **AI Core Processing (MediaPipe / OpenCV)**: Detects facial landmarks and extracts specific skin patches (forehead, left cheek, right cheek) while ignoring hair, eyes, and background.
- **DeepFace Age Estimation**: Predicts chronological skin age using deep learning neural networks.
- **Glow & Clarity Scoring**:
  - *Skin Brightness*: Measures luminance (Y channel) of skin patches.
  - *Skin Smoothness*: Calculates high-frequency texture noise using a Laplacian filter.
  - *Color Uniformity*: Determines skin tone consistency and blemish density.
- **Tailored Recommendations (Khao, Piyo, Lagao)**:
  - *Khao (Diet)*: Nutrient and vitamin-dense food tips.
  - *Piyo (Drinks)*: Hydration levels and detox drinks.
  - *Lagao (Apply)*: Topical remedies (cleansers, sunscreens, serums).
  - *AM/PM Skincare Routines*: Timeline schedules mapped to your age group (<25, 25-45, >45) and glow percentage.
  - *Acne & Pollution Shield*: Practical advice in Hinglish/English to defend skin from dust and pollution.
- **Premium Glassmorphic UI**: High-tech dashboard with scanning line animations, interactive progress rings, and responsive layout.

---

## 🛠 Tech Stack

- **Backend**: FastAPI, Uvicorn, Python 3.10+
- **Computer Vision & AI**: OpenCV, MediaPipe, DeepFace (TensorFlow/Keras backend)
- **Frontend**: Vanilla HTML5, CSS3 (Custom Glassmorphism), JavaScript, Lucide Icons

---

## 🚀 Local Setup & Installation

Follow these steps to run the application locally on your computer:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rohan1519/i-model-face-estimator.git
   cd i-model-face-estimator
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   - **PowerShell (Windows)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Command Prompt (Windows)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Web Server:**
   ```bash
   uvicorn app:app --reload
   ```

6. **Open in Browser:**
   Go to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** to test the application!

---

## 🐳 Cloud Deployment (Hugging Face Spaces / Docker)

This repository includes a `Dockerfile` for one-click cloud deployment. Because of TensorFlow's memory requirements, we recommend **Hugging Face Spaces** (Docker SDK, CPU Basic 16GB RAM free tier).

### Deploying to Hugging Face Spaces:
1. Create a new Space on [Hugging Face](https://huggingface.co/new-space) and select **Docker** as the SDK (with a blank template).
2. Link your GitHub repository or push to the Space remote:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/i-model-face-estimator
   git push -f hf main
   ```
3. Your application will build and go live automatically!

---

## 📄 License

This project is licensed under the MIT License.
