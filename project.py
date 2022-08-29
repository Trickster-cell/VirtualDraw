import cv2
import numpy as np

cap = cv2.VideoCapture(2)
# capturing real time image from the camera
cap.set(3, 1440)
cap.set(4, 960)
cap.set(10, 150)
# resizing the application window 

Colors = [
    [91, 95, 103, 179, 222, 255],  # blue
    [35, 79, 65, 78, 255, 255],  # Light green
     [149, 50, 140, 179, 255, 255],  # pink
    [0, 67, 141, 30, 255, 253],  # orange
]
# HSV values of preset colors in the application

color_values = [[204, 102, 0], [0, 255, 0], [255, 0, 255], [0, 165, 255]]  # , [0, 0, 0]]

points = []  # [x, y, colorID]


def getContours(img):
#     finding contours for the tracer
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def findColor(img, Colors, colorvals):
#     finding specific colors
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in Colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, colorvals[count], cv2.FILLED)
        if x != 0 and y != 0:
            newpoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[1]), mask)
    return newpoints


def drawOnCanvas(points, colorvals):
#     drawing on the application canvas
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 10, colorvals[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = findColor(img, Colors, color_values)
    if len(newpoints) != 0:
        for newP in newpoints:
            points.append(newP)
    if len(points) != 0:
        drawOnCanvas(points, color_values)
    cv2.putText(imgResult, " press 'Q' to Quit ", (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
