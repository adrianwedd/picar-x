from picarx import Picarx
from time import sleep
import readchar

from gpt_examples.friendly_logger import friendly_log

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    i: Head up
    k: Head down
    j: Turn head left
    l: Turn head right
    ctrl+c: Press twice to exit the program
'''

def show_info():
    print("\033[H\033[J", end="")  # clear terminal window
    print(manual)


if __name__ == "__main__":
    try:
        pan_angle = 0
        tilt_angle = 0
        friendly_log("info", "Warming up the PiCar-X!", color="cyan")
        px = Picarx()
        show_info()
        friendly_log("info", "Use W A S D to drive. Keep the path clear!", color="green")
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjl'): 
                if 'w' == key:
                    px.set_dir_servo_angle(0)
                    px.forward(80)
                    friendly_log("move", "Zoom! Driving forward.", color="green", extra="forward(80)")
                elif 's' == key:
                    px.set_dir_servo_angle(0)
                    px.backward(80)
                    friendly_log("move", "Backing up carefully.", color="yellow", extra="backward(80)")
                elif 'a' == key:
                    px.set_dir_servo_angle(-30)
                    px.forward(80)
                    friendly_log("move", "Turning left like a pro!", color="magenta", extra="steer=-30")
                elif 'd' == key:
                    px.set_dir_servo_angle(30)
                    px.forward(80)
                    friendly_log("move", "Swinging right!", color="magenta", extra="steer=30")
                elif 'i' == key:
                    tilt_angle+=5
                    if tilt_angle>30:
                        tilt_angle=30
                    friendly_log("sensor", "Camera looking up.", color="blue", extra=f"tilt={tilt_angle}")
                elif 'k' == key:
                    tilt_angle-=5
                    if tilt_angle<-30:
                        tilt_angle=-30
                    friendly_log("sensor", "Camera looking down.", color="blue", extra=f"tilt={tilt_angle}")
                elif 'l' == key:
                    pan_angle+=5
                    if pan_angle>30:
                        pan_angle=30
                    friendly_log("sensor", "Camera peeking right.", color="blue", extra=f"pan={pan_angle}")
                elif 'j' == key:
                    pan_angle-=5
                    if pan_angle<-30:
                        pan_angle=-30
                    friendly_log("sensor", "Camera peeking left.", color="blue", extra=f"pan={pan_angle}")                 

                px.set_cam_tilt_angle(tilt_angle)
                px.set_cam_pan_angle(pan_angle)      
                show_info()                     
                sleep(0.5)
                px.forward(0)
          
            elif key == readchar.key.CTRL_C:
                friendly_log("warning", "Stopping the adventure. Bye!", color="yellow")
                break

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)  
        px.set_dir_servo_angle(0)  
        px.stop()
        sleep(.2)
        friendly_log("success", "PiCar-X is calm and ready for next time!", color="green")

