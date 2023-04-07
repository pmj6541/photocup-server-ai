import cv2
import numpy as np
import sys

def classify(imgShapeList, detectedInfos) :
    mains = []
    for img_index in range(len(detectedInfos)) :
        # 객체 인식 정보 저장
        class_ids, confidence, boxes, indexes, classes = detectedInfos[img_index]
        # 표시할 색, 폰트 설정
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        font = cv2.FONT_HERSHEY_PLAIN
        height, width, channels = imgShapeList[img_index]
        main = []
        centerness = []
        main_label = "none"
        main_x = 0
        main_y = 0
        main_w = 0
        main_h = 0
        main_color = 0
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                center_x = int(x+w/2)
                center_y = int(y+h/2)
                now_centerness = (min(center_x,width-center_x)*min(center_y,height-center_y)/(max(center_x,width-center_x)*max(center_y,width-center_x)))**(1/2)
                centerness.append(now_centerness)
                label = str(classes[class_ids[i]])
                if max(centerness) == now_centerness :
                    main_label = label 
                    main_x = x   
                    main_y = y        
                    main_w = w          
                    main_h = h
                    main_color = colors[i]           
                color = colors[i]
                

        main.append(main_label)
        main.append(main_x)
        main.append(main_y)
        main.append(main_w)
        main.append(main_h)
        main.append(main_color)
        mains.append(main)
    return mains
