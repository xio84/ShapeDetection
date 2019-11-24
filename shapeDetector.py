import cv2
import numpy as np
import math
import clips
import logging
import os

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


            # Axises of vector's starting point
            xAxis = approx[i][0][0]
            yAxis = approx[i][0][1]
            # If points is in border, remove
            if ((xAxis == 0) or (yAxis == 0)):
                # print('deleting point...')
                approx = np.delete(approx, i, 0)
                invalidation = True
                break


            # Finding Euclidean distance
            distance = math.sqrt((lines[i][0] ** 2) + (lines[i][1] ** 2))
            # Only add if line is long enough
            if (distance > 5):
                aLines.append({'angle': int(round(angle)), 'distance': int(round(distance)), 'xAxis': int(round(xAxis)), 'yAxis': int(round(yAxis))})
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
        If 2 lines become 1 (a line is skipped) = make arcLengthPercentage higher
        If 1 line becomes 2 (a line is snapped) = make arcLengthPercentage lower
      

    Returns
    -------
    out : ndarray
        Array format: [numberOfShapes[, [[numberOfPoints, [[x1, y1], [x2, y2], ...,]], [list of description]], [numberOfPoints2, ...]]]

    Examples
    --------
    >>> arr = shapeDetection("img/shapes.jpg")

    """
    logging.basicConfig(level=loggingLevel)
    result = []
    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Starting clips
    env = clips.Environment()
    env.load(path = "shapeClassification.clp")
    shapes = []


    index = 0
    os.chdir('temp')
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


        # Assert facts
        avTemplate = env.find_template('av')
        i = 0
        while (i < lines[0]):
            newFact = avTemplate.new_fact()
            newFact['number'] = int(i + 1)
            newFact['angle'] = int(lines[1][i]['angle'])
            newFact['distance'] = int(lines[1][i]['distance'])
            newFact['xAxis'] = int(lines[1][i]['xAxis'])
            newFact.assertit()
            i+=1

        # Save activated rules
        activatedRules = []
        activatedRulesNum = 1
        logging.debug('Activated Rules:\n')
        while (activatedRulesNum):
            activatedRulesNum = 0
            for activated in env._agenda.activations():
                aR = activated.name
                logging.debug(aR + '\n')
                if not(activatedRules.count(aR)):
                    activatedRules.append(aR)
                activatedRulesNum += 1
            env.run(limit=1)

        # Save final facts
        desc = []
        for fact in env.facts():
            # print(fact)
            f = str(fact)
            # if f.find('result') != -1:
            desc.append(f)

        # Make image with descriptions
        cv2.drawContours(img, [approx], 0, (0), 5)
        # Writing descriptions (facts)
        # for d in desc:
        #     cv2.putText(img, d, (x, y), font, 1, (0))
        #     y += 30

        # Finding borders of shape
        i = 0
        maxX = lines[1][i]['xAxis']
        minX = lines[1][i]['xAxis']
        maxY = lines[1][i]['yAxis']
        minY = lines[1][i]['yAxis']
        i += 1
        while i<len(lines[1]):
            if (lines[1][i]['xAxis'] > maxX):
                maxX = lines[1][i]['xAxis']
            if (lines[1][i]['xAxis'] < minX):
                minX = lines[1][i]['xAxis']
            if (lines[1][i]['yAxis'] > maxY):
                maxY = lines[1][i]['yAxis']
            if (lines[1][i]['yAxis'] < minY):
                minY = lines[1][i]['yAxis']
            i += 1

        # Save shapes with facts
        if (len(desc) > 0):
            # Crop and save image
            index += 1
            filename = 'shape' + str(index) + ".jpg"
            crop_img = img[minY:maxY, minX:maxX]
            # cv2.imshow(filename, crop_img)
            cv2.imwrite(filename, crop_img)
            result.append({'numberOfVectors': lines[0], 'vectors': lines[1], 'facts': desc, 'rules': activatedRules, 'imgPath': 'temp/' + filename})

    # cv2.imshow("shapes", img)
    cv2.imwrite("Threshold.jpg", threshold)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    os.chdir('..')
    numberOfShapes = len(result)
    env.clear()
    result = {'numberOfShapes': numberOfShapes, 'shapesArray': result}
    return result


# Run example:
# print(shapeDetection("img/shapes.jpg", threshold=240))