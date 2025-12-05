import cv2  # best avaliable library for camera operations

# import serial  # library to read the motion detector input
import time  # for managing the buffer time
from collections import deque  # a list that allows for deletion after a specific time
import os  # for saving files

#  blah blah blah
port = "COM3"  # moeeedddd edit tis  #port for arduino
baud = 9600  # match to the arduino code (we are using arduino right??!)
buffer_seconds = 15  # time recorded before the event
post_seconds = 15  # time recorded after the event
vid_location = "events"  # folder to save the video files of the events

if not os.path.exists(vid_location):  # check if folder exists
    os.makedirs(vid_location)


# now we setup the cameraaaaa and seriaaaaal
ser = serial.Serial(port, baud, timeout=1)  # connection to sensor
cap = cv2.VideoCapture(0)  # starts the camera capturing

fps = 20
buffer = deque(maxlen=FPS * buffer_seconds)  # how much time we want in the buffer
state = "idle"  # when nothing happening
post_timer = 0  # timer for post motion caputuring
event_number = 1  # will number each event
motion_writer = None  # main thingy used for motion recording
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # save the file as mp4


# creating VIDEO WRITER nooww
def new_writer(folder, prefix, number, ext=".mp4"):
    filename = os.path.join(folder, f"{prefix}_{number}{ext}")
    return cv2.VideoWriter(
        filename, fourcc, FPS, (640, 480)
    )  # setting resolution of vid


# now da main loopy doopy
try:  # for handling errors and making sure Python dont crash out
    while True:
        ret, frame = cap.read()  # basically reads frame and gives false if smth wrong
        if not ret:
            print("frame ni read ho ri Saaar")
            break

    motion = 0  # idle state, no motion
    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()  # basically read info from arduino
        if line in ["0", "1"]:
            motion = int(line)  # converting into integer

    if state == "idle":  # no action
        buffer.append(frame)  # keep only 15 seconds in memory
        if motion == 1:
            print(
                f"EVENT {event_number}: Motion detected"
            )  # savin the buffer with the number
        # now we need to clip the buffer and the video togethaa
        motion_writer = new_writer(vid_location, "event", event_number, ".mp4")
        for f in buffer:
            motion_writer.write(f)
        state = "recording"
        post_timer = 0
        writer.release()  # closing da file

        # starting motion recording
        motion_writer = new_writer(vid_location, "event", event_number, ".mp4")
        motion_write4r.write(frame)
        state = "recording"  # switching state
        post_timer = 0  # reset post timer

    # recording mode (motion is happening)
    elif state == "recording":
        motion_writer.write(frame)  # saves current frame
        if motion == 0:
            print(f"EVENT {event_number}: Motion ended -> start post recording")
            state = "postrecord"  # switch to post recording
            post_timer = time.time()  # record sstart time

    # now the post recording after the event
    elif state == "postrecord":
        motion_writer.writer(frame)  # saving the post recording frames

        # first check if 15 seconds have passed
        if time.time() - post_timer >= post_seconds:
            print(f"EVENT {event_number}: Post recording done, returning to idle")
            motion_writer, release()  # closing the video file
            motion_writer = None  # reset writer
            event_number += 1  # increasing the number of event
            state = "idle"  # return to normal state
            buffer.clear()  # emptying buffer for next event

finally:
    cap.release()  # camera released
    cv2.destroyAllWindows()  # xclose da cv windows
    if motion_writer:
        motion_writer.release()  # close open vid files
    ser.close()  # close serial port
    print("pRoGrAm TeRmInAtEd")
