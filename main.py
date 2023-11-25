from time import sleep
import cv2
import os
import numpy as np
import mysql.connector
import imutils
import pytesseract
from PIL import Image
from threading import Thread

from database import insertImageIntoDatabase, getStealEngines

lsEngin = []
Exited = False


def readEngines():
    global lsEngin
    while not Exited:
        lsEngin = getStealEngines()
        sleep(5)


def analyse(img):
    # The following two lines are for tests in local
    # img = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
    # img = cv2.resize(img, (620, 480))

    # Convert to grey scale, then blur to remove noise (usless informations)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # Edge detection
    edged = cv2.Canny(gray, 30, 200)

    # Find the contours in the edged image, keep only the largest ones
    # And initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # Loop through the contours
    for c in cnts:
        # Countour approximation
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # If the approximated contour has four points, then
        # Assume that a screen is found
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
        return
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    # Read the plate number
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    for engin in lsEngin:
        if engin["numeroSerie"] == text:
            insertImageIntoDatabase(engin["id"])
    print("Detected Number is:", text)

    # For tests in local
    # cv2.imshow('image', img)
    # cv2.imshow('Cropped', Cropped)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# Register the video flux as images
def main():
    lsEngin = getStealEngines()
    thEngine = Thread(target=readEngines)
    thEngine.start()
    # Connect to the Rasberry-Pi webcam
    cap = cv2.VideoCapture("http://192.168.1.60:8081")
    # Connect to default webcam
    # cap.open(0)

    # Check if the webcam is successfully opened
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        exit()

    # Create a directory to save the images
    output_directory = "images"
    os.makedirs(output_directory, exist_ok=True)

    # Counter (images)
    count = 0

    while True:
        # Read image per image
        ret, img = cap.read()

        if not ret:
            print("Erreur: Impossible de lire la trame.")
            break

        # Stream the image
        cv2.imshow('frame', img)
        th = Thread(target=analyse, args=[img])
        th.start()
        # Display and wait for an input from std
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
