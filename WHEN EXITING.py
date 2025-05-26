from PIL import Image
import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;
from datetime import datetime, timedelta

cam = cv2.VideoCapture(0)
x = open('weLiveInASociety', 'a')
set


num = 0
searching = True
'final'

while True:
    
    check, frame = cam.read()
   
    img = cv2.resize(frame,(320, 240))
    img_empty = np.zeros((img.shape[0], img.shape[1]))
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img3 = cv2.threshold(img2, 165, 255, cv2.THRESH_BINARY)[1]
    img4 = cv2.normalize(img3, img_empty,255, 0, cv2.NORM_MINMAX)
    img5= cv2.GaussianBlur(img4, (5, 5), 0)
    text = pytesseract.image_to_string(img5)

    # cv2.imshow("Original", img)
    # cv2.imshow("Normalized", img2)
    # cv2.imshow("Threshold", img3) 
    cv2.imshow("FINAL", img5)    
    
   # if text /= " ":
    filter = ''.join(char for char in text if char.isalnum()).upper()
# x.write("\n" + text)

    y = datetime.now().time().isoformat('seconds')

    #x.write("\n " + str(y) + " " + filter)
    print("\n " + filter + " " + str(y))  


    if filter != "":
        if num == 0:
            chk1 = filter
            num += 1
        elif num == 1:
            chk2 = filter
            num += 1
        elif num == 2:
            chk3 = filter
            num += 1

            if chk1 == chk2 == chk3:
                final = chk3
                searching = False
                print("final plate")
                print(final)               

    

    if num == 3 and searching:
        num = 0

    if searching == False:
        file_path = "weLiveInASociety"
        search_word = final

        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if search_word in line:
                    print(f"Found '{search_word}' on line {line_number}: {line.strip()}")
    
        
        enter = line.strip(final)
        # totalTime = datetime.datetime.combine(datetime.date.today(), enter) - datetime.combine(datetime.date.today(), y)    
        
        def time_difference_minutes(enter, y):
            fmt = "%H:%M:%S"

            # Convert time strings to datetime objects
            t1 = datetime.strptime(enter, fmt)
            t2 = datetime.strptime(y, fmt)

            # Calculate difference in seconds
            diff_seconds = (t2 - t1).total_seconds()

            # If the difference is negative (crossing midnight), add 24 hours in seconds
            if diff_seconds < 0:
                diff_seconds += 24 * 3600  # 24 hours in seconds

            # Convert seconds to minutes
            return int(diff_seconds // 60)

   
        minutes = time_difference_minutes(enter, y)
        print(f"Time difference: {minutes - 1200} minutes")


        





    key = cv2.waitKey(1)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()
 