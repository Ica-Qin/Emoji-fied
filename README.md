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


https://git.arts.ac.uk/user-attachments/assets/a3e518bf-7788-4e66-b4e5-65b59470e052




---

## 🖼 Showcase Photo

![showcase01](https://git.arts.ac.uk/user-attachments/assets/907e2f7f-581b-467b-9700-ac9d90b4ad55)
![showcase02](https://git.arts.ac.uk/user-attachments/assets/74d2261e-e6e3-464a-aff5-18ed1bb578ee)
![showcase03](https://git.arts.ac.uk/user-attachments/assets/6532023b-0624-42a9-8d4d-ad042552fc31)
![image](https://git.arts.ac.uk/user-attachments/assets/84ce491b-43be-44bd-9389-81e625251740)
![image](https://git.arts.ac.uk/user-attachments/assets/909a4773-1867-4bd7-aafb-bb56bc7f28c9)
![image](https://git.arts.ac.uk/user-attachments/assets/25f3c791-832a-4f00-92ad-ab263a4cf2ef)


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

[ChatGPT Dialogues Link](https://chatgpt.com/g/g-p-6845f17f205c81919e92aff9cfe2bbe1-fianl-project/project)
