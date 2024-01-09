import pyautogui
import time
from datetime import datetime
import pytesseract
import cv2
import pandas as pd

# Enables a failsafe - terminates the script if the mouse cursor is moved to top left corner of the monitor
pyautogui.FAILSAFE= True
pyautogui.PAUSE = 0.5
absorbances = []

time.sleep(3)

# Automatically moves the mouse cursor to pre-determined positions on the screen, i.e. clicking through menus to save data
while(True):

    clock = datetime.now()
    
    # Screen coordinates and click positions
    pyautogui.moveTo(x=1151, y=160)
    pyautogui.click()
    pyautogui.moveTo(x=794, y=521)
    pyautogui.click()
    pyautogui.typewrite("UV-Vis experiment - " + str((clock.strftime("%d %b %Y %H %M"))) )
    pyautogui.moveTo(x=1084, y=664)
    pyautogui.click()
    pyautogui.moveTo(x=1012, y=633)
    pyautogui.click()
    pyautogui.moveTo(x=1069, y=628)
    pyautogui.click()

    # Take a screenshot and modify the image so the absorbance value can be read with computer vision
    screenshot = pyautogui.screenshot(region=((1154, 956, 36, 20)))
    screenshot.save(r"C:\Users\thebonlab\Documents\UV-Vis data\Josh Ryan\Temp screenshot\screenshot171820.png")

    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(r"C:\Users\thebonlab\Documents\UV-Vis data\Josh Ryan\Temp screenshot\screenshot171820.png")
    image = cv2.resize(image,(0,0),fx=7,fy=7)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    inverted = cv2.bitwise_not(thresh)

    # Read the text on the modified image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\thebonlab\AppData\Local\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(inverted, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    
    # Export the absorbance readout to a CSV file.
    text = float(str(text[0]) + "." + str(text[1]) + str(text[2]) + str(text[3]))
    absorbancelist = absorbances.append(text)

    df = pd.DataFrame(absorbances)
    df.to_csv(r"C:\Users\thebonlab\Documents\UV-Vis data\Josh Ryan\Absorbances\absorbances170820.csv", index=False)

    # Used for debugging/visualisation of manipulated images
    #cv2.imshow('thresh', thresh)
    #cv2.imshow("inverted", inverted)
    #cv2.waitKey()

    time.sleep(61)
