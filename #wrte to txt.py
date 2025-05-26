#wrte to txt
import datetime
import cv2
import os, sys, inspect #For dynamic filepaths
import time

 
x = open('WORKplz', 'a')
# open('textLog', 'r')
i = 1

#for y in range(4):


i=i+1
if(i < 8):
    y = datetime.datetime.now().time().isoformat('seconds')
    x.write("\n " + str(y) + " HEEELLO WORLD")
    print(str(y))
    

# Define the file and the word you're looking for
file_path = "WORKplz"
search_word = "EEE"

# Open the file and search
with open(file_path, "r") as file:
    for line_number, line in enumerate(file, start=1):
        if search_word in line:
            print(f"Found '{search_word}' on line {line_number}: {line.strip()}")




# searching = True
# while(searching):


#  #   if(chk1 == chk2 == chk3):
#  #       searching = False
#     seaching = False

#  g = open('textLog', 'r').readlines()
#  n = open('textLog', 'r').readline()
#  t = open('textLog', 'r').read()
#  print(g + "done")
#  print(n + "done")
#  print(t + "done")

# now = datetime.datetime.now()

# now.time()
# datetime.time
# print((datetime.timedelta(y)))

# a = datetime.datetime.now().time()
# b = a - y

exit()