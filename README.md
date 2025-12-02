# Emoji-fied: Tangible Emotion-to-Bitmap Machine System
## Advanced-Final-Project-Peiyang-Qin

*A physical installation visualising how machines simplify and categorise human emotions.*

[Thesis](PeiyangQin_Emoji-fied.pdf)

---

## ⭐ Overview

This project builds a complete real-time pipeline that transforms **facial expression → emotion label → bitmap → printed material output**.  
Using an OpenMV CAM 7 Plus, Arduino Mega 2560 Pro, three thermal printers and 4 fans, the system materialises the computational reduction of human emotion into discrete, machine-readable “signals”.

The installation visualises the hidden process of emoji-fication described in the thesis.

---

## 🎬 Demo Video




https://github.com/user-attachments/assets/3ee92d83-e0cc-42b4-839e-c0125d08e00f






---

## 🖼 Showcase Photo

![showcase03](https://github.com/user-attachments/assets/64a2868c-4ef0-471e-a04f-d1f6ba57f40e)
<img width="1522" height="1012" alt="image" src="https://github.com/user-attachments/assets/64796730-729f-4701-9a33-0704aeda2255" />
![showcase01](https://github.com/user-attachments/assets/ab0a5cef-3348-44b0-a922-a307c8fc21fb)


<img width="1280" height="672" alt="test2" src="https://github.com/user-attachments/assets/802bc59a-19f5-440f-a5b1-90e943105535" />
<img width="1280" height="677" alt="test3" src="https://github.com/user-attachments/assets/9f7d3804-6000-4900-b329-74ac2ceb7941" />
<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/8ee38c77-897a-4099-82b3-2515e1d4cbce" />


---

## 🧩 System Overview

### 1. Facial Input (OpenMV CAM 7 Plus)
- Real-time face detection  
- Lightweight expression classifier trained with FER2013 + custom photos  
- Bitmap conversion and serial transmission  
- Outputs: **emotion label + confidence score + 1-bit bitmap**  


### 2. Arduino Mega 2560 Pro (Central Controller)
- Receives serial data from OpenMV  
- Routes print jobs using **three hardware serial ports**  
- Manages thermal printers and fan activation  
- Operates printers at **9600 baud** (115200 produced garbled output)  

### 3. Thermal Printers (3-way categorical output)
| Printer | Paper Colour | Emotion Categories |
|---------|--------------|-------------------|
| Printer 1 | Yellow | Happy, Surprise |
| Printer 2 | Blue | Sad |
| Printer 3 | Green | Fear, Angry |

### 4. Mechanical Output (Fan)
- Fan activates for **30 seconds** after each print  
- Creates drifting movement to emphasise emotion, “signals” becoming simplified or lost  

---

## 🔧 Hardware

- OpenMV CAM 7 Plus  
- Arduino Mega 2560 Pro  
- 58mm thermal printers × 3  
- LM2596 buck converter (9V → 5V)  
- Relay module (fan control)  
- 9V power supply  
- Aluminium linear shafts + 3D printed brackets  
- PVC plates + iron net for airflow shaping  


---

## 💻 Code

### 📁 [OpenMV Code](Codes/OpenMV.py)
- Face detection  
- Emotion classification  
- Bitmap generation  
- Serial output  



### 📁 [Arduino Code](Codes/Arduino)
- Receives bitmap + emotion score  
- Chooses printer port  
- Sends bitmap to printer  
- Activates fan

### Logs
[Development Logs](Development_Log.md)
