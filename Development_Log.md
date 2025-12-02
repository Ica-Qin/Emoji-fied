# Development & Iteration Log  
*Process documentation for OpenMV + Arduino system*

This document records the major iterations, problems and decisions made during the development of the installation.  
It is divided into two parts: **OpenMV iterations** and **Arduino iterations**.

---

# 1. OpenMV Iterations

## 1.1 Initial Attempt: Custom CNN Model (Failed)
- Trained a CNN using **Keras + FER2013** on PC.
- Converted the model into **TensorFlow Lite**.
- Attempted to load on OpenMV CAM 7 Plus.
- **Issues encountered:**
  - OpenMV did not have enough RAM → *MemoryError*
  - Unsupported TFLite operators → *conversion failure*
  - Inference speed too slow → *not real-time*
 
![屏幕截图 2025-11-25 004311](https://git.arts.ac.uk/user-attachments/assets/680792ac-8362-4021-8d59-8f02e7312140)

- **Decision:** Abandon custom model and switch to OpenMV’s built-in lightweight classifier.

---

## 1.2 Switching to Built-in Expression Classifier
- Adopted OpenMV’s example model for **emotion classification**.
- Advantages:
  - Real-time inference
  - Fully compatible with OpenMV hardware
  - Small model size
- **Added training data**:
  - Supplemented with self-captured facial photos to reduce dataset bias.
  - Adjusted lighting and positioning for more stability.
![image](https://git.arts.ac.uk/user-attachments/assets/9dfbb2b7-4dfb-40c2-a1d7-3c2f0be1fbe6)


---

## 1.3 Face Detection → Emotion Classification Pipeline
- Integrated Haar-like face detection with the classifier.
- Encountered a bug where:
  - Expression classification ran *even when no face was present* → random scores printed.
- **Fix:**
  - Add explicit face-detection threshold.
  - Only classify when a face is detected.

---

## 1.4 Bitmap Generation & Serial Output
- Converted ROI face images into **1-bit bitmaps**.
- Implemented byte-packet sending to Arduino.
- Challenges:
  - OpenMV’s serial port sends characters one-by-one.
  - Needed to tune frame size to avoid overflow.
- Final result:
  - Stable bitmap transmission aligned with emotion label and score.

---

# 2. Arduino Iterations

## 2.1 Early Design: Handshake Protocol (Failed)
- Initial plan: a **2-step handshake** between Arduino ↔ OpenMV.
- Process:
  - Arduino sends `"start next loop"`
  - OpenMV detects face + sends emotion
  - Arduino sends `"start img"` for bitmap
- **Problem discovered:**
  - OpenMV receives serial commands **letter-by-letter**
  - Handshake timing is constantly desynchronised
  - System frequently **froze** or missed messages

**Decision:** Remove handshake entirely → switch to one-directional control.

---

## 2.2 Final Design: One-Directional Trigger Flow
- Arduino sends a single `"S"` command to OpenMV.
- OpenMV performs:
  - Face detection  
  - Emotion classification  
  - Bitmap sending  
- Arduino routes data to the correct printer.
- This eliminated all freeze issues and allowed continuous looping.

---

## 2.3 Thermal Printer Baud Rate Debugging
- Initially used **115200 baud** for faster printing.  
- Result: printers output **garbled characters**.
- Found printer documentation stating:
  - **Supported baud rate = 9600**
- Updated code accordingly → printing became stable.

---

## 2.4 Multi-Serial Routing for 3 Printers
- Arduino Mega 2560 Pro chosen for **multiple hardware serial ports**.
- Mapping:
  - Serial1 → OpenMV
  - Serial2 → Printer 1
  - Serial3 → Printer 2
  - Serial4 → Printer 3
- Implemented routing logic based on emotion labels.

---

## 2.5 Fan Activation Logic
- Used **D9 + relay module**.
- Fan turns on for **30 seconds** after each print.
- Initial timing caused overlap when prints were frequent.
- Improved logic:
  - Reset the timer only after the previous cycle finishes.

---

# 3. Wiring and Soldering

## One Mistake
- I happened to connect rx with rx and tx with tx at first, leading to no information switches between Arduino and OpenMV.

## Wiring & Power Design

![image](https://git.arts.ac.uk/user-attachments/assets/6096ac90-8933-4fa0-bb7b-2553fdac90fe)


![3d8b83060efac5b319d6ebcdcdfdaabd](https://git.arts.ac.uk/user-attachments/assets/9fd0c4f2-7607-43ae-91e5-1116c732ad20)

![image](https://git.arts.ac.uk/user-attachments/assets/56864b60-d376-42dd-b91e-3957366e91c2)


![wiring](https://git.arts.ac.uk/user-attachments/assets/7b69a787-aabe-4954-b268-1195c29631b5)

![image](https://git.arts.ac.uk/user-attachments/assets/4de41a36-0d1b-4384-a62d-a0a81150a8b2)



## Frame Instalment

![image](https://git.arts.ac.uk/user-attachments/assets/d9d10f97-0be0-4286-bca8-c088b197e022)

![image](https://git.arts.ac.uk/user-attachments/assets/d4c48eba-5511-42de-9a7d-8c235f69185e)


---

# 4. Summary of Key Insights
- Handshake-based embedded communication is unstable on OpenMV; **one-way triggers** are more reliable.
- Emotional classification errors shape the *meaning* of the work rather than being purely technical problems.
- Physical printing reveals machine logic as **material artefacts**—bitmaps, distortions, noise.
- Lightweight embedded ML always involves **reduction**, aligning with the concept of emoji-fication.

---

