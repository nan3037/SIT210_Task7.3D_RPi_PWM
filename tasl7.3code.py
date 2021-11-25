import RPi.GPIO as GPIO
import time

led1 = 12
led2 = 32
led3 = 35
trig = 33
echo = 31
#speed of sound/2 for calculations
constant = 17150

#         range of ultrasonic sensor is 4m hence
#            duty cycle is in range of 100
#     hence to add variations in the PWM a unit of 4 is selected

GPIO.setmode(GPIO.BOARD)

leds = [led1, led2, led3]
for led in leds:
    GPIO.setup(led, GPIO.OUT)
  
L1_pwm = GPIO.PWM(led1,1000)
L2_pwm = GPIO.PWM(led2,1000)
L3_pwm = GPIO.PWM(led3,1000)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

pwm_list = [L1_pwm, L2_pwm, L3_pwm]
for L_pwm in pwm_list:
    L_pwm.start(0)
    
def measure_distance():

    GPIO.output(trig, True)
    time.sleep(0.00001)
    
    GPIO.output(trig, False)
    sent = time.time()
    recieved = time.time()

    while GPIO.input(echo) == 0:
        sent = time.time()

    while GPIO.input(echo) == 1:
        recieved = time.time()

    time_taken = recieved - sent
    
    distance = (time_taken * constant)
    return distance


while True:
    dis = measure_distance()
    print(dis)
    val = int(dis/4)
    if val > 7:
        for L_pwm in pwm_list:
            L_pwm.ChangeDutyCycle(val)
    else:
        for L_pwm in pwm_list:
            L_pwm.ChangeDutyCycle(0)
            
        
