import cv2
import numpy as np
import math
import clips
import logging

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
    # While vectors made is invalid, try again
    invalid = True
    while(invalid and len(approx)>1):
        invalidation = False
        # Creating vectors based on point->nextPoint
        lines = []
        i = 0
        while (i < len(approx)):
            vector = [approx[(i + 1) % len(approx)][0][0] - approx[i][0][0], approx[(i + 1) % len(approx)][0][1] - approx[i][0][1]]
            lines.append(vector)
            i+=1
        i=0
        aLines=[]
        while (i < len(lines)):
            # Finding the angle of each vector, based on previous vector
            angle = findAngle(lines[i], lines[(i - 1) % len(lines)])
            # If angle is too obtuse, remove
            if ((angle > 170) and (angle < 190)):
                # print('deleting point...')
                approx = np.delete(approx, i, 0)
                invalidation = True
                break
            # Finding Euclidean distance
            distance = math.sqrt((lines[i][0] ** 2) + (lines[i][1] ** 2))
            # Axises of vector's starting point
            xAxis = approx[i][0][0]
            yAxis = approx[i][0][1]
            
            # Onnly add if line is long enough
            if (distance > 5):
                aLines.append([int(round(angle)), int(round(distance)), int(round(xAxis)), int(round(yAxis))])
            i+=1
        invalid = invalidation
        # if (invalid):
            # print('Retrying...')
            # print(approx)
    return [len(aLines), aLines]

def shapeDetection(path, threshold=230, arcLengthPercentage=0.005, loggingLevel=logging.WARN):
    """
    Return an array with description of every shape in an image.

    Parameters
    ----------
    path : string
      Path to image file (relative to this file), e.g. "img.shapes.jpg".
    threshold : int, optional
      The maximum contrast needed to detect a shape.
      Higher value = More shapes, but increases noise (tiny shapes that don't matter)
      Lower value = Decreases noise, but shapes are less likely to be detected
    arcLengthPercentage : int, optional
      

    Returns
    -------
    out : ndarray
        Array format: [numberOfShapes[, [[numberOfPoints, [[x1, y1], [x2, y2], ...,]], [list of description]], [numberOfPoints2, ...]]]

    Examples
    --------
    >>> arr = shapeDetection("img/shapes.jpg")

    """
    logging.basicConfig(loggingLevel)
    result = []
    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Starting clips
    env = clips.Environment()
    env.load(path = "shapeClassification.clp")
    shapes = []


    for cnt in contours:
        env.reset()
        approx = cv2.approxPolyDP(cnt, arcLengthPercentage*cv2.arcLength(cnt, True), True)
        # cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        logging.debug("lines:" + str(len(approx)) + "\n")
        lines = apxToVector(approx)
        shapes.append(lines)
        logging.debug(lines)
        logging.debug("approx:" + str(len(approx)) + "\n")
        logging.debug(approx)

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
            i+=1

        env.run()
        desc = []
        for fact in env.facts():
            # print(fact)
            f = str(fact)
            if f.find('result') != -1:
                desc.append(f[7:-1])

        cv2.drawContours(img, [approx], 0, (0), 5)
        for d in desc:
            cv2.putText(img, d, (x, y), font, 1, (0))
            y += 30

        result.append([lines, desc])        

    cv2.imshow("shapes", img)
    cv2.imshow("Threshold", threshold)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result = [len(result), result]
    return result


# Run example:
# print(shapeDetection("img/shapes.jpg", threshold=240))