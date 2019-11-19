import cv2
import numpy as np
import math
import clips

def findAngle(vector1, vector2):
    # Dot Product
    dp = (vector1[0] * vector2[0] * -1) + (vector1[1] * vector2[1] * -1)
    # Euclidean distance
    ed1 = math.sqrt((vector1[0] ** 2) + (vector1[1] ** 2))
    ed2 = math.sqrt((vector2[0] ** 2) + (vector2[1] ** 2))
    # Degrees
    deg = math.degrees(math.acos(dp / float(ed1 * ed2)))
    return deg


def apxToVector(approx):
    lines = []
    i = 0
    while (i < len(approx)):
        vector = [approx[(i + 1) % len(approx)][0][0] - approx[i][0][0], approx[(i + 1) % len(approx)][0][1] - approx[i][0][1]]
        lines.append(np.array(vector))
        i+=1
    # for v in lines:
    #     if v[0] <= 5 and v[0] >= -5:
    #         v[0] = 0
    #     if v[1] <= 5 and v[1] >= -5:
    #         v[1] = 0
    i=0
    aLines=[]
    while (i < len(lines)):
        angle = findAngle(lines[i], lines[(i - 1) % len(lines)])
        distance = math.sqrt((lines[i][0] ** 2) + (lines[i][1] ** 2))
        xAxis = approx[i][0][0]
        yAxis = approx[i][0][1]
        if (distance > 5):
            aLines.append(np.array([int(round(angle)), int(round(distance)), int(round(xAxis)), int(round(yAxis))]))
        i+=1
    return np.array([len(aLines), aLines])

font = cv2.FONT_HERSHEY_COMPLEX
img = cv2.imread("img/shapes.jpg", cv2.IMREAD_GRAYSCALE)
_, threshold = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Starting clips
env = clips.Environment()
env.load(path = "shapeClassification.clp")
shapes = []


for cnt in contours:
    env.reset()
    approx = cv2.approxPolyDP(cnt, 0.005*cv2.arcLength(cnt, True), True)
    # cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    print("lines:", len(approx))
    lines = apxToVector(approx)
    shapes.append(lines)
    print(lines)
    # print(approx)
    # print(list(map(lambda x:print(type(x)),approx)))
    # print(type(lines))

    env.assert_string("(vertexNum " + str(lines[0]) + ")")



    avTemplate = env.find_template('av')
    i = 0
    while (i < lines[0]):
        newFact = avTemplate.new_fact()
        newFact['number'] = int(i + 1)
        newFact['angle'] = int(lines[1][i][0])
        newFact['distance'] = int(lines[1][i][1])
        newFact['xAxis'] = int(lines[1][i][2])
        newFact.assertit()
        # newFact = "(av (number " + str(i) + ") (angle " + str(lines[1][i][0]) + ") (distance " + str(lines[1][i][1]) + ") (xAxis " + str(lines[1][i][2]) + "))"
        # print(newFact)
        # env.assert_string(newFact)
        i+=1

    env.run()
    desc = []
    for fact in env.facts():
        print(fact)
        f = str(fact)
        if f.find('result') != -1:
            desc.append(f[7:-1])

    cv2.drawContours(img, [approx], 0, (0), 5)
    # if len(approx) == 3:
    #     cv2.putText(img, "Triangle", (x, y), font, 1, (0))
    # elif len(approx) == 4:
    #     cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
    # elif len(approx) == 5:
    #     cv2.putText(img, "Pentagon", (x, y), font, 1, (0))
    # elif 6 < len(approx) < 15:
    #     cv2.putText(img, "Ellipse", (x, y), font, 1, (0))
    # else:
    for d in desc:
        cv2.putText(img, d, (x, y), font, 1, (0))
        y += 30

cv2.imshow("shapes", img)
cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()