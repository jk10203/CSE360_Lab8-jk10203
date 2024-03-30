#Joy Kim -- green ball detection (LAB 8)

import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time



sensor.reset() #resets the sensor
sensor.set_pixformat(sensor.RGB565) #sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) #sets the resolution to 320x240 px
sensor.set_vflip(True) #flips the image vertically
sensor.set_hmirror(True) #mirrors the image horizontally
sensor.skip_frames(time = 2000) #skip some frames to let the image stabilize

#define the min/max LAB values we're looking for (GREEN BALL)
thresholdsGreenBall = (100, 0, -128, -17, -128, 127)
#(99, 0, -128, -15, -128, 34)
#(44, 0, -128, -23, -128, 44)
#(100, 0, -128, -22, -128, 44)
#(44, 0, -128, -23, -128, 44),
#(83, 0, -128, -15, -127, 51)

ledRed = pyb.LED(1) #initiates the red led
ledGreen = pyb.LED(2) #initiates the green led

clock = time.clock() #instantiates a clock object


distances = [13, 15, 18, 20, 10, 12, 22, 21, 24, 13]
inverse_s_b = [0.0001417434444, 0.0002014504432, 0.0002690341673, 0.000338066261,
0.00008056719304, 0.0001182033097, 0.0003770739065, 0.0003434065934,
0.0004830917874, 0.0001401738155]

#number of observations ^^^ (10)
N = len(distances)

#calculating sums and sum of products
sum_x = sum(inverse_s_b)
sum_y = sum(distances)
sum_xy = sum(x*y for x, y in zip(inverse_s_b, distances))
sum_x_squared = sum(x**2 for x in inverse_s_b)

#calculating slope (m) and intercept (b)
m = (N * sum_xy - sum_x * sum_y) / (N * sum_x_squared - sum_x**2)
b = (sum_y - m * sum_x) / N

def duck_location (inverse_s_b):
    return m * inverse_s_b + b #linear calculation

while(True):
    clock.tick() #advances the clock
    img = sensor.snapshot() #takes a snapshot and saves it in memory

    #find blobs with a minimal area of 50x50 = 2500 px
    #overlapping blobs will be merged
    blobs = img.find_blobs([ thresholdsGreenBall], merge=True)
    #area_threshold=2500

    #draw blobs
    for blob in blobs:
        #draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        #draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
        #center of blob
        print("center of the blob (u,v): ", "(", blob.cx(),"px ,", blob.cy(), "px)")

        #calculate area of blob detected
        area = blob.area()
        print("area: ", area)


    #turn on green LED if a blob was found
    if len(blobs) > 0:
        ledGreen.on()
        ledRed.off()
        location = duck_location(1 / (area)) #location based on 1/s_b
        print("location of duck / ball: ", location)

    else:
    #turn the red LED on if no blob was found
        ledGreen.off()
        ledRed.on()

    pyb.delay(50) #pauses for 50ms
    print(clock.fps()) #prints the fps to the serial console


    ##    The distance from the duck to the front of the robot, d.
    ##    The angle from the central axis to the camera to the duck \theta.
    ##    The size of the blob s_b.
    ##    The center of the blob in pixels, (u,v).

