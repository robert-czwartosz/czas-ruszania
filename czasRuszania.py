# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# https://gist.github.com/pknowledge/623515e8ab35f1771ca2186630a13d14
# https://github.com/spmallick/learnopencv/tree/master/BlobDetector

# import the necessary packages
import cv2
import numpy as np
import json
import keyboard
import time, os
import shutil

print("""STEROWANIE

z - tempo odtwarzania = 1
x - tempo odtwarzania = 10
c - tempo odtwarzania = 100
v - zatrzymanie nagrania(tempo odtwarzania = 0)

q - zakończ""")

def blobs(im):
        
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        # Set blob color
        params.filterByColor = True
        params.blobColor = 255

        # Change thresholds
        #params.minThreshold = 10
        #params.maxThreshold = 200


        # Filter by Area.
        params.filterByArea = True
        params.minArea = 2500

        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.87
            
        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.01
        params.maxInertiaRatio = 0.09

        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
                detector = cv2.SimpleBlobDetector(params)
        else : 
                detector = cv2.SimpleBlobDetector_create(params)


        # Detect blobs.
        keypoints = detector.detect(im)

        return keypoints


with open("config.json", 'r') as f:
        params = json.load(f)

vs = cv2.VideoCapture(params["pathRoot"]+params["video"])
pathRoot = params["pathRoot"]
# variables
tempo = 1
path = None
show = params["show"]
save = params["save"]

# params
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

threshJest = params["threshJest"]
threshRuch1 = params["threshRuch1"]
threshRuch2 = params["threshRuch2"]

frameCounter = 0
czySa = 0
start = 0
stop = 0
czasy = []
czyAutobus = False
fps = vs.get(cv2.CAP_PROP_FPS)
print(fps)

# initialize the background frames in the video stream
backgrounds = os.listdir(pathRoot + "backgrounds\\")
# background switch timestamps
switchTimestamps = [int(f[:-4]) for f in backgrounds]
# Bubble sort
for i in range(len(switchTimestamps)):
        for j in range(i+1, len(switchTimestamps)):
                if switchTimestamps[i] > switchTimestamps[j]:
                        pom = switchTimestamps[i]
                        switchTimestamps[i] = switchTimestamps[j]
                        switchTimestamps[j] = pom
                        pom = backgrounds[i]
                        backgrounds[i] = backgrounds[j]
                        backgrounds[j] = pom
switchTimestamps = switchTimestamps[1:]

backgroundFrames = []
for background in backgrounds:
        print(background)
        backgroundFrame = cv2.imread(pathRoot + "backgrounds\\" + background)
        frame0 = backgroundFrame
        gray = cv2.cvtColor(backgroundFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        backgroundFrames.append(gray)

backgroundIdx = 0
backgroundFrame = backgroundFrames[0]


# loop over the frames of the video
while True:
        # grab the current frame
        frame = vs.read()
        frame = frame[1]

        if backgroundIdx < len(switchTimestamps):
                if switchTimestamps[backgroundIdx] < frameCounter/fps/60:
                        backgroundIdx += 1
                        backgroundFrame = backgroundFrames[backgroundIdx]
                        
        
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
                break

        frame = frame[Y:Y + H, X:X + W]

        
        # compute the absolute difference between the current frame and previous frame
        # convert to grayscale, and blur
        diff = cv2.absdiff(frame0, frame)
        frame0 = cv2.absdiff(frame, cv2.absdiff(frame,frame))
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.GaussianBlur(diff, (5,5), 0)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # compute the absolute difference between the current frame and
        # background frame
        frameDelta = cv2.absdiff(backgroundFrame, gray)

        # threshold result images
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        threshDiff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes
        threshDiff2 = cv2.dilate(threshDiff, None, iterations=1)

        
        ### compute statistics czyJest1, czyJest2, czyRuch1, czyRuch2, czyPrzejezdne, czyAutobus
        czyJest1 = np.mean(np.mean(thresh[y1:y1 + h1, x1:x1 + w1], 0), 0) > threshJest
        czyJest2 = np.mean(np.mean(thresh[y2:y2 + h2, x2:x2 + w2], 0), 0) > threshJest
        czyPrzejezdne = np.mean(np.mean(thresh[y3:y3 + h3, x3:x3 + w3], 0), 0) < 10
        if czyPrzejezdne:
                cv2.putText(frame, "Przejezdne", (350, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 255), 3)
        
        czyRuch1 = np.mean(np.mean(threshDiff2[y1:y1 + h1, x1:x1 + w1], 0), 0) > threshRuch1
        czyRuch2 = np.mean(np.mean(threshDiff2[y2:y2 + h2, x2:x2 + w2], 0), 0) > threshRuch2
        czyAutobus = len(blobs(thresh[100:, :400])) > 0
        if czyAutobus:
                cv2.putText(frame, "Autobus", (550, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 255), 3)
        
        if czyRuch1:
                cv2.putText(frame, "Status: {}".format('Movement1'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3)
        if czyRuch2:
                cv2.putText(frame, "Status: {}".format('Movement2'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 3)


        ### check conditions
        if (frameCounter - start)/fps > 5 and start!=0: # reset
                start = 0
                czySa = 61
        if czySa/fps > 2 and czyRuch1:
                start = frameCounter
                czySa = 0
                czyKorek = (czyPrzejezdne == False)
        if start != 0 and czyRuch2:
                stop = frameCounter
                czas = (stop - start) / fps
                path = None
                if czyKorek == False and czyAutobus == False and czas > 0.14:        
                        czasy.append((round(float(start)/fps,3), round(float(stop)/fps,3), round(czas,3)))
                start = 0
                stop = 0
                print(round(start/fps/60,2), round(stop/fps/60,2), czas, czyKorek)
        if czyJest1 and czyJest2 and czyRuch1 == False and start == 0 and czyAutobus == False and czyPrzejezdne:
                czySa += 1
        else:
                czySa = 0
        if tempo==0:
                print(np.mean(np.mean(threshDiff2[y2:y2 + h2, x2:x2 + w2], 0)))
        # show the frame
        if show:
                frame[y1:y1 + h1, x1:x1 + w1] = [255, 255, 255]
                frame[y2:y2 + h2, x2:x2 + w2] = [255, 255, 255]
                frame[y3:y3 + h3, x3:x3 + w3] = [255, 255, 255]
                cv2.imshow("Video", frame)
                cv2.imshow("Diff", thresh)
                cv2.imshow("Delta", threshDiff2)
                key = cv2.waitKey(tempo) & 0xFF
                # if the `q` key is pressed, break from the lop
                if key == ord("q"):
                        break
                if key == ord("z"):
                        tempo = 1
                if key == ord("x"):
                        tempo = 10
                if key == ord("c"):
                        tempo = 100
                if key == ord("v"):
                        tempo = 0
        else:
                if keyboard.is_pressed('q'):
                        break
        if frameCounter%15==0:
                time.sleep(0.00000001)
        frameCounter += 1
        if frameCounter%int(fps*600)==0:
                print(str(round(frameCounter/fps/3600 - 0.5)), "h", str(round(frameCounter/fps/60)%60), "min")

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()

if save:
        with open(pathRoot + "czasy_ext.txt", 'w') as f:
                for tup in czasy:
                        for item in tup:
                                f.write("%s " % item)
                        f.write("\n")
        with open(pathRoot + "czasy.txt", 'w') as f:
                for tup in czasy:
                        f.write("%s \n" % tup[2])
