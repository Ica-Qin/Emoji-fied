# This code run in OpenMV4 H7 Plus

import sensor, image, time, os, tf

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

labels = [line.rstrip() for line in open("labels.txt")]
class_num = len(labels)

clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    for obj in tf.classify("trained.tflite", img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        img.draw_rectangle(obj.rect())
        output = obj.output()
        for i in range(class_num):
            print("%s = %f" % (labels[i], output[i]))
    print(clock.fps(), "fps")
