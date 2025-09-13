# HandSense Controller
---

## 📌 Project Overview  
This project introduces a **vision-based hand gesture recognition system** that integrates **computer vision, machine learning, and IoT applications**. The system enables natural and intuitive interaction with both **multimedia software** and **physical devices**.  

By leveraging **Mediapipe Hand Tracking** for landmark extraction and a trained **Support Vector Machine (SVM)** classifier, the project demonstrates:  
- **Gesture-controlled media playback** (play, pause, rewind, fast forward, volume).  
- **Gesture-based IoT device control** on a Raspberry Pi (LED switching, patterns, flashing).  

This project illustrates the potential of **gesture-based human–computer interaction (HCI)** in enhancing **smart environments** and **assistive technology** solutions.  


---

## 📊 Dataset  
The dataset used in this project consists of essential details for training the gesture recognition model.  
👉 [https://www.kaggle.com/datasets/marusagar/hand-gesture-detection-system]  

---

## 👤 Author Information  
- **Name:**  MohammadAmin Mohammadion Shabestari
- **Email:**  Shabestari8303p@gmail.com
- **LinkedIn:** [linkedin.com/in/](https://linkedin.com/in/mohammadamin-shabestari)  
- **GitHub:** [github.com/](https://github.com/msh8303)
- **Teammates:** Sogol Salamat / Yekta Khalili
- **Course:** Introduction to Mechatronic systems by **DR.Mehdi Delrobaei**
- **University:** K. N. Toosi University of Technology
- **Date:** September 2025  

---

## 🧑‍🔬 Methodology  

1. **Landmark Extraction**  
   - Used **Mediapipe Hands** to extract 3D coordinates (x, y, z) of 21 hand landmarks.  

2. **Feature Engineering**  
   - Landmarks were flattened into structured vectors representing gestures.  
   - Data was normalized to improve classifier robustness.  

3. **Model Training**  
   - Implemented in `training notebook.ipynb`.  
   - Classifier: **Support Vector Machine (SVM)** with multi-class support.  
   - Saved model for real-time deployment.  

4. **Gesture Inference**  
   - Captured live webcam/Raspberry Pi camera feed.  
   - Extracted landmarks → Classified gesture → Mapped to control commands.  

5. **Applications**  
   - **Media Controller**: Sends keyboard events (`space`, arrow keys, volume) via `pyautogui`.  
   - **IoT Controller**: Controls LEDs (on/off, flashing, swipe patterns) via **GPIO pins** on Raspberry Pi 3.  

---

## 🎮 Gesture Set  

| ID | Gesture       | Media Control Action | IoT LED Action                 |
|----|---------------|----------------------|--------------------------------|
| 0  | Left Swipe    | Rewind               | Left-to-right LED pattern      |
| 1  | Right Swipe   | Fast Forward         | Right-to-left LED pattern      |
| 2  | Stop          | Play/Pause toggle    | Turn OFF all LEDs              |
| 3  | Thumbs Down   | Volume Down          | Flash all LEDs                 |
| 4  | Thumbs Up     | Volume Up            | Turn ON all LEDs (low light)   |  

---

## 📊 Results and Discussion  
- The **SVM classifier** achieved **high recognition accuracy** on the predefined gesture set.  
- Real-time implementation showed **low latency (<100 ms)** for gesture recognition and command execution.  
- **Strengths:**  
  - Works without wearable sensors.  
  - Low hardware cost (webcam/Raspberry Pi).  
  - Supports both software and hardware applications.  
- **Limitations:**  
  - Sensitive to poor lighting conditions.  
  - Single-hand tracking only.

---

## 🎓 Academic Relevance  
This project contributes to research in the fields of:  
- **Computer Vision & Pattern Recognition** (real-time hand tracking).  
- **Machine Learning Applications** (gesture classification using SVM).  
- **Human–Computer Interaction (HCI)** and **Human–IoT Interaction**.  
- **Assistive Technology** (non-verbal communication for accessibility).  

The system demonstrates how **vision-based gesture recognition** can enhance **smart environments** and be extended to domains like **robotics, healthcare, and AR/VR systems**.  

---
