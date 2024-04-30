import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import argparse

from ultralytics import YOLO
import cv2
import time


from helpers import most_intersections,point_inside_rectangle,rectangle_intersection



parser = argparse.ArgumentParser(description='YOLOV8 PPE Detection')

# Add arguments
parser.add_argument('--input', help='Input File ("filepath"/"") Empty for using webcam',default="")
parser.add_argument('--conf', help='Detection Confidence (float)',default=0.5)
parser.add_argument('--save', help='Save Detection Result (True/False)',default=False)
parser.add_argument('--show', help='Show Detection Result (True/False)',default=False)

# Parse the command-line arguments
args = parser.parse_args()

# Access the arguments
input_frame = args.input
conf = float(args.conf)
isSave = True if args.save=="True" else False
isShow = True if args.show=="True" else False

results = {}

# load models
coco_model = YOLO('best.pt')

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

cap = None
result = None
# load video

if input_frame!= "":
    cap = cv2.VideoCapture(input_frame) # using camera/webcam
    videoWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    videoHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    result = cv2.VideoWriter('filename.mp4',  
                         fourcc, 
                         10, (videoWidth,videoHeight)) 

else:
    cap = cv2.VideoCapture(1) # using camera/webcam






# read frames
frame_nmr = -1
ret = True
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 255, 255)
thickness = 6


# if input_frame!=""

while ret:
    frame_nmr += 1
    ret, frame = cap.read()

    start_time = time.time()
    if ret :
        results[frame_nmr] = {}

        # use track() to identify instances and track them frame by frame, take only with conf> 0.5
        detections = coco_model.predict(frame, conf=conf,imgsz=2048)[0]
        # save cropped detections
        # detections.save_crop('outputs')

        workers = []
        ppe = []
        wh=0
        wv=0
        whv=0

        for detection in detections.boxes.data.tolist():
            # if len(detection) ==7:
            #     x1, y1, x2, y2, track_id, score, class_id = detection
            # else: # assign track_id = -1 if track id not presence
            person_id = 0
            x1, y1, x2, y2, score, class_id = detection
            if class_id==0:
                workers.append([x1,y1,x2,y2,score,class_id,person_id])
                person_id+=1
            else:
                if class_id !=1:
                    class_id=2
                ppe.append([x1,y1,x2,y2,score,class_id])

        workers_ppe =[[]]*(len(workers))

        for eq in ppe:
            x1,y1,x2,y2,score,class_id = eq
            area = 0
            idx= -1
            center = [abs(x2-x1)//2,abs(y2-y1)//2]
            for person in workers:
                x1p,y1p,x2p,y2p,_,_,person_id = person
                inside = point_inside_rectangle(center,(x1p,y1p,x2p,y2p))
                intersect_area= rectangle_intersection((x1,y1,x2,y2),(x1p,y1p,x2p,y2p))
                if area<intersect_area:
                    area = intersect_area
                    idx= person_id
            if area>0:
                workers_ppe[idx].append(class_id)

        for bbox in workers:
            org = [int(x1), int(y1)]
            
            x1p,y1p,x2p,y2p,_,_,person_id = bbox

            text = "W"
            for e in workers_ppe[person_id]:
                if text=="WHV":
                    break
                if e==1:
                    if text =="WH":
                        text="WHV"
                    else:
                        text="WV"
                else:
                    if text=="WV":
                        text="WHV"
                    else:
                        text="WH"

            if text=="WH":
                wh+=1
            elif text=="WV":
                wv+=1
            elif text=="WHV":
                whv+=1

            cv2.rectangle(frame, (int(x1p), int(y1p)), (int(x2p), int(y2p)), (255, 0, 255), 3)
            cv2.putText(frame, text, org, font, fontScale, color, thickness)

        cv2.putText(frame, "W   :" + str(len(workers)), [1700,30], font, fontScale, color, thickness)
        cv2.putText(frame, "WV  :"+str(wv), [1700,60], font, fontScale, color, thickness)
        cv2.putText(frame, "WH  :" + str(wh), [1700,90], font, fontScale, color, thickness)
        cv2.putText(frame, "WHV :" + str(whv), [1700,120], font, fontScale, color, thickness)

        print("W ",len(workers))
        print("WH ",wh)
        print("WV ",wv)
        print("WHV ",whv)


        end_time = time.time()                        
        elapsed_time =  end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds for frame number: {frame_nmr} ")  
        cv2.putText(frame, "FPS :" + "{:.2f}".format(1/elapsed_time), [1500,30], font, fontScale, color, thickness)
        if input_frame!="" and isSave:
            result.write(frame)
    
    if isShow:
        cv2.imshow('Webcam', cv2.resize(frame,(800,600)))
    name = f"./output_frame/frame_{frame_nmr}.jpg"
    #cv2.imwrite(name, frame)     # uncomment this to save frame
    if cv2.waitKey(1) == ord('q'):
        break
# write_csv(results, './results.csv')
cap.release()
if input_frame!="":
    result.release()
