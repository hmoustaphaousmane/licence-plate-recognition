from time import sleep

import cv2
import os
import numpy as np
from datetime import datetime
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
    # img = cv2.imread('4.jpg', cv2.IMREAD_COLOR)

    # img = cv2.resize(img, (620, 480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
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

    # Read the number plate
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    for engin in lsEngin:
        if engin["numeroSerie"] == text:
            insertImageIntoDatabase(engin["id"])
    print("Detected Number is:", text)

    # cv2.imshow('image', img)
    # cv2.imshow('Cropped', Cropped)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# Enregistrement du flux de vidéo comme images
def main():
    lsEngin = getStealEngines()
    thEngine = Thread(target=readEngines)
    thEngine.start()
    # Ouvrir la connexion à la caméra. 0 correspond à la caméra par défaut.
    cap = cv2.VideoCapture(0)
    # cap.open("http://192.168.1.60:8088")
    # cv2.VideoCapture("http://192.168.1.60:8081")

    # Vérifier si la caméra est ouverte correctement
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        exit()

    # Créer un répertoire pour enregistrer les images
    output_directory = "images"
    os.makedirs(output_directory, exist_ok=True)

    count = 0  # Compteur pour numéroter les images

    while True:
        # Capture image par image
        ret, img = cap.read()

        if not ret:
            print("Erreur: Impossible de lire la trame.")
            break

        # Afficher l'image en direct
        cv2.imshow('frame', img)
        th = Thread(target=analyse, args=[img])
        th.start()
        # Enregistrement de l'image dans le répertoire de sortie
        # image_path = os.path.join(output_directory, f'image_{count}.jpg')
        # cv2.imwrite(image_path, img)
        # count += 1  # Incrémenter le compteur
        # Affichage et saisie d'un code clavier
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fermer la fenêtre OpenCV
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
