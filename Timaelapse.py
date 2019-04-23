import cv2
import datetime
import time
import os
import numpy
import glob


Webcam = cv2.VideoCapture(0)
Width = int(Webcam.get(3))
Height = int(Webcam.get(4))
SavePath = 'Timelapse Video/Timelapse.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
Out = cv2.VideoWriter(SavePath ,cv2.VideoWriter_fourcc(*'XVID'), 20, (Width ,Height))

TimeLapseImageDirectory = 'TimeLapseImages/'
SecondsDuration = 30
SecondsPerShots = .50
Now = datetime.datetime.now()
EndTime = Now + datetime.timedelta(seconds=SecondsDuration)
Flag = 1

if not os.path.exists(TimeLapseImageDirectory):
    os.mkdir(TimeLapseImageDirectory)


while datetime.datetime.now() < EndTime:
    _ , Frame = Webcam.read()
    Frame = cv2.flip(Frame , 1)
    FileName = f"{TimeLapseImageDirectory}/{Flag}.jpg"
    Flag +=1 
    
    cv2.imwrite(FileName , Frame)
    time.sleep(SecondsPerShots)
    if cv2.waitKey(1) == ord('q'):
        break

def ImagesToVideoConversion(Out, ImageDirectory , clearImages = True):
    ImageList = glob.glob(f"{TimeLapseImageDirectory}/*.jpg")
    SortedImages = sorted(ImageList , key = os.path.getmtime)
    for file in SortedImages:
        image = cv2.imread(file)
        Out.write(image)    
    if clearImages:
        for file in ImageList:
            os.remove(file)
ImagesToVideoConversion(Out , TimeLapseImageDirectory ) 

Webcam.release()
Out.release()
cv2.destroyAllWindows()