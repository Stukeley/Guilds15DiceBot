import cv2
import pytesseract
import fnmatch
import platform
import numpy as np


# Funkcja zwraca 1, jeśli gracz wygrał w kości, 0 jeśli przegrał
def DetectDiceState(img):
    lost_text = "zaginiony"
    won_text = "wygrał"

    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    elif platform.system() == "Darwin":
        pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    img_cropped = img[200:350, 150:700]

    # Grayscale
    img_gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)

    # Threshold
    _, thresholded_image = cv2.threshold(img_gray, 164, 255, cv2.THRESH_BINARY)

    # Morphological operations
    kernel = np.ones((1, 1), np.uint8)
    thresholded_image = cv2.erode(thresholded_image, kernel, iterations=1)
    thresholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)

    text = pytesseract.image_to_string(thresholded_image, lang="pol")
    text = str(text).lower().strip()

    # Match text against *(n-2)* strings
    if fnmatch.fnmatch(text, "*" + won_text.lower()[1:-1] + "*"):
        result = 1
    else:
        result = 0

    return result
