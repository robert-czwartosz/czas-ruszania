
# import the necessary packages
import cv2
import numpy as np
import json

print("""STEROWANIE

a - pole nr 1 - pojazd 1
b - pole nr 2 - pojazd 2
c - pole nr 3 - przejezdność skrzyżowania
x - okno

w - zmiana szerokości
h - zmiana wysokości

+/- - zwiększanie/zmniejszanie szerokości lub wysokości pola/okna

2, 8, 4, 6 - sterowanie pozycją

s - zapisz
q - zakończ""")

with open("config.json", 'r') as f:
        params = json.load(f)

vs = cv2.VideoCapture(params["pathRoot"]+params["video"])

# variables
tempo = 1

X = params["X"]
Y = params["Y"]
W = params["W"]
H = params["H"]

x1 = params["x1"]
y1 = params["y1"]
w1 = params["w1"]
h1 = params["h1"]

x2 = params["x2"]
y2 = params["y2"]
w2 = params["w2"]
h2 = params["h2"]

x3 = params["x3"]
y3 = params["y3"]
w3 = params["w3"]
h3 = params["h3"]

changeW = False
changeH = False
changeXY = True
changeXY1 = False
changeXY2 = False
changeXY3 = False


frameCounter = 0

fps = vs.get(cv2.CAP_PROP_FPS)
print(fps)
width = int( vs.get(cv2.CAP_PROP_FRAME_WIDTH) ) 
height = int( vs.get(cv2.CAP_PROP_FRAME_HEIGHT) )

# loop over the frames of the video
while True:
        # grab the current frame
        frame = vs.read()
        frame = frame[1]

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
                break
        
        # cut frame
        frame = frame[Y:Y + H, X:X + W]
        
        # draw squares
        frame[y1:y1 + h1, x1:x1 + w1] = [255, 255, 255]
        frame[y2:y2 + h2, x2:x2 + w2] = [255, 255, 255]
        frame[y3:y3 + h3, x3:x3 + w3] = [255, 255, 255]
        
        # show the frame
        cv2.imshow("Video", frame)
        key = cv2.waitKey(tempo) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("h"):
                show = 0
        if key == ord("q"):
                break
        if key == ord("s"):
                params["X"] = X
                params["Y"] = Y
                params["W"] = W
                params["H"] = H
                
                params["x1"] = x1
                params["y1"] = y1
                params["w1"] = w1
                params["h1"] = h1
                
                params["x2"] = x2
                params["y2"] = y2
                params["w2"] = w2
                params["h2"] = h2
                
                params["x3"] = x3
                params["y3"] = y3
                params["w3"] = w3
                params["h3"] = h3
                
                with open('config.json', 'w') as outfile:
                        json.dump(params, outfile, separators=(', \n', ': '))

        if key == ord("a"):
                changeXY1 = True
                changeXY2 = False
                changeXY = False
                changeXY3 = False
        if key == ord("b"):
                changeXY1 = False
                changeXY2 = True
                changeXY = False
                changeXY3 = False
        if key == ord("c"):
                changeXY1 = False
                changeXY2 = False
                changeXY = False
                changeXY3 = True
        if key == ord("x"):
                changeXY1 = False
                changeXY2 = False
                changeXY = True
                changeXY3 = False
        
        if key == ord("6"):
                if changeXY1:
                        x1 += 1
                        x1 = min(W-w1, x1)
                if changeXY2:
                        x2 += 1
                        x2 = min(W-w2, x2)
                if changeXY3:
                        x3 += 1
                        x3 = min(W-w3, x3)
                if changeXY:
                        X += 10
                        X = min(width-W, X)
        if key == ord("4"):
                if changeXY1:
                        x1 -= 1
                        x1 = max(0, x1)
                if changeXY2:
                        x2 -= 1
                        x2 = max(0, x2)
                if changeXY3:
                        x3 -= 1
                        x3 = max(0, x3)
                if changeXY:
                        X -= 10
                        X = max(0, X)
        if key == ord("2"):
                if changeXY1:
                        y1 += 1
                        y1 = min(H-h1, y1)
                if changeXY2:
                        y2 += 1
                        y2 = min(H-h2, y2)
                if changeXY3:
                        y3 += 1
                        y3 = min(H-h3, y3)
                if changeXY:
                        Y += 10
                        Y = min(height-H, Y)
        if key == ord("8"):
                if changeXY1:
                        y1 -= 1
                        y1 = max(0, y1)
                if changeXY2:
                        y2 -= 1
                        y2 = max(0, y2)
                if changeXY3:
                        y3 -= 1
                        y3 = max(0, y3)
                if changeXY:
                        Y -= 10
                        Y = max(0, Y)


        if key == ord("w"):
                changeW = True
                changeH = False
        if key == ord("h"):
                changeW = False
                changeH = True
        if key == ord("+"):
                if changeW and changeXY:
                        W += 10
                        W = min(width-X, W)
                if changeH and changeXY:
                        H += 10
                        H = min(height-Y, H)
                
                if changeXY1 and changeH:
                        h1 += 1
                        h1 = min(H-y1, h1)
                if changeXY1 and changeW:
                        w1 += 1
                        w1 = min(W-x1, w1)
                
                if changeXY2 and changeH:
                        h2 += 1
                        h2 = min(H-y2, h2)
                if changeXY2 and changeW:
                        w2 += 1
                        w2 = min(W-x2, w2)

                if changeXY3 and changeH:
                        h3 += 1
                        h3 = min(H-y3, h3)
                if changeXY3 and changeW:
                        w3 += 1
                        w3 = min(W-x3, w3)
        if key == ord("-"):
                if changeW and changeXY:
                        W -= 10
                        W = max(100, W)
                if changeH and changeXY:
                        H -= 10
                        H = max(100, H)

                if changeXY1 and changeH:
                        h1 -= 1
                        h1 = max(5, h1)
                if changeXY1 and changeW:
                        w1 -= 1
                        w1 = max(5, w1)
                
                if changeXY2 and changeH:
                        h2 -= 1
                        h2 = max(5, h2)
                if changeXY2 and changeW:
                        w2 -= 1
                        w2 = max(5, w2)

                if changeXY3 and changeH:
                        h3 -= 1
                        h3 = max(5, h3)
                if changeXY3 and changeW:
                        w3 -= 1
                        w3 = max(5, w3)
        
        frameCounter += 1
        if frameCounter%int(fps*600)==0:
                print(str(round(frameCounter/fps/60)), "min")

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
