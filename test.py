import cv2
import numpy as np

for i in range(10):
    filename = f"0{i}.jpg"
    print(filename)
    

    if(len(sys.argv)>1 and sys.argv[1] == "--all") :
                    cv2.rectangle(imgList[img_index], (x, y), (x + w, y +h), color, 2)
                    cv2.putText(imgList[img_index],label, (x, y + 30), font, 3, color, 3)