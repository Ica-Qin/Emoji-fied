# ========== main.py  OpenMV：等待 'S' → 人脸 + 表情识别 → 浅色 Polaroid 风格打印 ==========

import sensor, image, time, ml
from pyb import UART, LED

# ---------- 0. LED ----------
led_red   = LED(1)
led_green = LED(2)
led_blue  = LED(3)

def blue_blink_idle(now_ms, last_blink_ms, interval_ms=5000):
    if time.ticks_diff(now_ms, last_blink_ms) >= interval_ms:
        led_blue.toggle()
        return now_ms
    return last_blink_ms

# ---------- 1. 摄像头 ----------
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # 320x240
sensor.skip_frames(time=2000)

clock = time.clock()

# ---------- 2. 人脸检测模型 ----------
face_cascade = image.HaarCascade("/rom/haarcascade_frontalface.cascade", stages=25)

# ---------- 3. 表情识别模型 ----------
model  = ml.Model("trained.tflite", load_to_fb=True)
labels = [line.rstrip("\n") for line in open("labels.txt")]

# ---------- 4. UART ----------
uart = UART(1, 9600, timeout_char=100)

# ---------- 5. 状态机 ----------
INFER_INTERVAL = 2000
active         = False
last_infer     = 0
last_blink     = time.ticks_ms()

# ---------- 发送表情 ----------
def send_expression(label, score):
    msg = "EMO,%s,%.3f\n" % (label, score)
    uart.write(msg)
    print("[OpenMV] Sent:", msg.strip())


# ========== 🌟最终版：Polaroid / 浅色风格 send_image ==========
def send_image(src_img, label, score):
    # ------- 复制原图 -------
    out = src_img.copy()

    # ------- 1. 柔化图像（降噪） -------
    out.gaussian(1)

    # ------- 2. 降对比度（偏浅） -------
    out.gamma_corr(gamma=0.80)

    # ------- 3. 提亮（让整体更白） -------
    out.midpoint(1, bias=0.55)

    # ------- 4. 素描强化（轻微锐化） -------
    try:
        out.laplacian(1, sharpen=True)
    except:
        pass

    # ------- 5. 在底部加白条 + 表情文字 -------
    bar_h = 25
    out.draw_rectangle(0, out.height()-bar_h, out.width(), bar_h,
                       color=255, fill=True)
    text = "%s (%.2f)" % (label, score)
    out.draw_string(5, out.height()-22, text, color=0)

    # ------- 6. 打印前：轻量去噪 -------
    out.mean(1)

    # ------- 7. 伪灰度阈值（关键：偏浅） -------
    TH = 60  # 150~170 更浅更白，也不会白纸

    # ------- 发送头部 -------
    w = out.width()
    h = out.height()
    uart.write("IMG,%d,%d\n" % (w, h))
    print("[OpenMV] Sent header: IMG,%d,%d" % (w, h))

    led_red.on()

    # ------- 8. 按行发送位图 -------
    for y in range(h):
        row = []
        for x in range(w):
            p = out.get_pixel(x, y)
            row.append("1" if p < TH else "0")
        uart.write("".join(row) + "\n")

    led_red.off()
    print("[OpenMV] Image sent (Polaroid浅色风).")


# ========== 主循环 ==========
print("[OpenMV] Ready. Waiting for 'S' from Arduino...")

while True:
    clock.tick()
    img = sensor.snapshot()
    now = time.ticks_ms()

    # ===== IDLE：等待 S =====
    if not active:
        last_blink = blue_blink_idle(now, last_blink)
        if uart.any():
            ch = uart.read(1)
            if ch == b'S':
                led_blue.off()
                led_green.on()
                print("[OpenMV] Got 'S' — start session")
                time.sleep_ms(150)
                led_green.off()
                active     = True
                last_infer = 0
        continue

    # ===== ACTIVE：检测阶段 =====
    faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)
    if not faces:
        continue

    # 最大面积人脸
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    img.draw_rectangle(x, y, w, h, color=255)

    # 表情推理节流
    now = time.ticks_ms()
    if time.ticks_diff(now, last_infer) < INFER_INTERVAL:
        continue
    last_infer = now

    # 裁剪为 48x48（你的模型必须这样处理）
    face_img = img.copy()
    s = min(48.0/w, 48.0/h)
    face_img.crop(x_scale=s, y_scale=s, roi=(x, y, w, h))

    scores = model.predict([face_img])[0].flatten().tolist()
    idx    = scores.index(max(scores))
    label  = labels[idx]
    score  = scores[idx]

    print("Expression:", label, "Score:", score)

    # ===== 发送表情 + Polaroid风整图 =====
    send_expression(label, score)
    send_image(img, label, score)

    # 回到空闲
    active      = False
    last_blink  = time.ticks_ms()
    led_blue.off()
    led_green.off()
    led_red.off()
    print("[OpenMV] Session done.\n")
