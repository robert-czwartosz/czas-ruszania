
# import the necessary packages
import cv2
import numpy as np
import json
print("""
STEROWANIE
n - 1s do przodu
b - 1s do tyłu
m - 7.5min do przodu
v - 7.5min do tyłu
, - 15 min do przodu
c - 15 min do tyłu
. - 30 min do przodu
x - 30 min do tyłu
/ - 1h do przodu
z - 1h do tyłu

s - zapisz tło do katalogu backgrounds
q - zakończ
""")
with open("config.json", 'r') as f:
        params = json.load(f)


vs = cv2.VideoCapture(params["pathRoot"]+params["video"])
fps = vs.get(cv2.CAP_PROP_FPS)

vs.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
numFrames = vs.get(cv2.CAP_PROP_POS_FRAMES)
timeLength = numFrames/fps
vs.set(cv2.CAP_PROP_POS_AVI_RATIO,0)

print(fps)
print(numFrames)


# variables
tempo = 1000
step = fps
frameCounter = 0
idx = 0

# loop over the frames of the video
while True:
        # grab the current frame
        vs.set(cv2.CAP_PROP_POS_FRAMES, frameCounter)
        frame = vs.read()[1]

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
                break
        
        # show the frame
        cv2.imshow("Video", frame)
        key = cv2.waitKey(tempo) & 0xFF
        if key == ord("s"):
                cv2.imwrite(params["pathRoot"] + 'backgrounds\\'+str(round(frameCounter/fps/60))+".png", frame )
                idx += 1
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
                break
        if key == ord("n"):
                frameCounter += step
                frameCounter = min(int(numFrames/step)*step, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("b"):
                frameCounter -= step
                frameCounter = max(0, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("m"):
                frameCounter += int(3600*fps/step/8) * step
                frameCounter = min(int(numFrames/step)*step, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("v"):
                frameCounter -= int(3600*fps/step/8) * step
                frameCounter = max(0, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord(","):
                frameCounter += int(3600*fps/step/4) * step
                frameCounter = min(int(numFrames/step)*step, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("c"):
                frameCounter -= int(3600*fps/step/4) * step 
                frameCounter = max(0, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("."):
                frameCounter += int(3600*fps/step/2) * step
                frameCounter = min(int(numFrames/step)*step, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("x"):
                frameCounter -= int(3600*fps/step/2) * step
                frameCounter = max(0, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("/"):
                frameCounter += int(3600*fps/step) * step
                frameCounter = min(int(numFrames/step)*step, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        if key == ord("z"):
                frameCounter -= int(3600*fps/step) * step
                frameCounter = max(0, frameCounter)
                print(round(frameCounter/fps/3600 - 0.49),'h', round(frameCounter/fps/60), 'min')
        
        
                


# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
