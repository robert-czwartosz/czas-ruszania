
# import the necessary packages
import cv2
import numpy as np
import json
import random
import os

print("""
STEROWANIE

n - 1 klatka do przodu
b - 1 klatka do tyłu do tyłu

a - akceptacja pomiaru
p - odrzucenie pomiaru
o - odrzucenie pomiaru wraz z napisaniem uwagi dotyczącej pomiaru

q - zakończ
""")

def floor(num):
        return round(num - 0.5)

def fix(num):
        return num - floor(num)

with open("config.json", 'r') as f:
        params = json.load(f)
pathRoot = params["pathRoot"]

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

# get samples
samples = []
with open(params["pathRoot"] + "czasy_ext.txt", 'r') as f:
        line = f.readline().split(' ')
        while(len(line) > 1):
                samples.append( ( float(line[0]), float(line[1]) ) )
                line = f.readline().split(' ')
N = len(samples)

# get fps
vs = cv2.VideoCapture(params["pathRoot"]+params["video"])
fps = vs.get(cv2.CAP_PROP_FPS)


# variables
czasy = []
odrzucone = []

sample_idx = 0
sample = samples[sample_idx]
czas = sample[1] - sample[0]
idx_max = int(round(czas * fps))
print(sample_idx, str(czas) + 's', idx_max)

idx = 0

# initialize the background frames in the video stream
backgrounds = os.listdir(pathRoot+"backgrounds\\")
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
        backgroundFrame = cv2.imread(pathRoot+"backgrounds\\"+background)
        frame0 = backgroundFrame
        gray = cv2.cvtColor(backgroundFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        backgroundFrames.append(gray)

backgroundIdx = 0
backgroundFrame = backgroundFrames[0]


# loop over the frames of the video
while True:
        TimeSec = sample[0] + idx/fps
        frameIdx = int(round(TimeSec * fps))
        # grab frame
        vs.set(cv2.CAP_PROP_POS_FRAMES, frameIdx)
        frame = vs.read()[1]

        if backgroundIdx < len(switchTimestamps):
                if switchTimestamps[backgroundIdx] < TimeSec/60:
                        backgroundIdx += 1
                        backgroundFrame = backgroundFrames[backgroundIdx]
        
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
                break
        
        HH = str(floor(TimeSec/3600))
        MM = str(floor(TimeSec/60)%60)
        SS = str(floor(TimeSec)%60)
        MS = str(round(1000 * fix(TimeSec)))
        TimeStr = HH + ':' + MM + ':' + SS + ':' + MS
        cv2.putText(frame, str(TimeStr), (550, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 3)
        # FILTER
        # compute the absolute difference between the current frame and previous frame
        # convert to grayscale, and blur
        diff = cv2.absdiff(frame0, frame)
        
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
        threshDiff = cv2.dilate(threshDiff, None, iterations=1)
        
        # show the frame
        frame[y1:y1 + h1, x1:x1 + w1] = [255, 255, 255]
        frame[y2:y2 + h2, x2:x2 + w2] = [255, 255, 255]
        frame[y3:y3 + h3, x3:x3 + w3] = [255, 255, 255]
        cv2.imshow("frame", frame)
        cv2.imshow("thresh", thresh)
        cv2.imshow("threshDiff", threshDiff)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("a"):
                czasy.append((str(sample[0]), str(round(czas, 3))))
                sample_idx += 1
                if sample_idx >= N:
                        break
                sample = samples[sample_idx]
                czas = sample[1] - sample[0]
                idx_max = int(round(czas * fps))
                print(sample_idx, str(czas)+'s', idx_max)
                idx = 0
        if key == ord("p"):
                odrzucone.append((str(sample[0]), str(round(czas, 3)), '?'))
                sample_idx += 1
                if sample_idx >= N:
                        break
                sample = samples[sample_idx]
                czas = sample[1] - sample[0]
                idx_max = int(round(czas * fps))
                print(sample_idx, str(czas)+'s', idx_max)
                idx = 0
        if key == ord("o"):
                cv2.destroyAllWindows()
                notatka = input('Uwaga: ')
                odrzucone.append((str(sample[0]), str(round(czas, 3)), notatka))
                sample_idx += 1
                if sample_idx >= N:
                        break
                sample = samples[sample_idx]
                czas = sample[1] - sample[0]
                idx_max = int(round(czas * fps))
                print(sample_idx, str(czas)+'s', idx_max)
                idx = 0
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
                break
        if key == ord("n"):
                frame0 = cv2.absdiff(frame, cv2.absdiff(frame,frame))
                idx += 1
                idx = min(idx, idx_max)
        if key == ord("b"):
                frame0 = cv2.absdiff(frame, cv2.absdiff(frame,frame))
                idx -= 1
                idx = max(0, idx)

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()

with open(params["pathRoot"] + "czasy_ok_ext" + ".txt", 'w') as f:
        for tup in czasy:
                for item in tup:
                        f.write("%s " % item)
                f.write("\n")

with open(params["pathRoot"] + "czasy_ok" + ".txt", 'w') as f:
        for tup in czasy:
                f.write("%s \n" % tup[1])


with open(params["pathRoot"] + "czasy_odrzucone_ext" + ".txt", 'w') as f:
        for tup in odrzucone:
                for item in tup:
                        f.write("%s " % item)
                f.write("\n")

with open(params["pathRoot"] + "czasy_odrzucone" + ".txt", 'w') as f:
        for tup in odrzucone:
                f.write("%s \n" % tup[1])
