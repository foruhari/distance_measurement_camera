import cv2
import numpy as np
CONFIDENCE = 0.1
SCORE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.1
font_scale = 1
thickness = 2
box = ()

config_path = "siamFC_method_test/yolov4-tiny.cfg"
weights_path = "siamFC_method_test/yolov4-tiny.weights"
labels = open("siamFC_method_test/coco.names").read().strip().split("\n")
colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")


net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#
# posList = []
#
# def position(event,x,y,flags,param):
#     global posList
#     if event == cv2.EVENT_RBUTTONUP:
#         posList.append((x, y))
#         # print (x, y)
#     # else:
#     #     posList=[]

def yolo(image):
    # image =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = image.shape[:2]
    # create 4D blob
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608), swapRB=True, crop=False)
    # sets the blob as the input of the network
    net.setInput(blob)
    # get all the layer names
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    layer_outputs = net.forward(ln)
    # feed forward (inference) and get the network output
    boxes, confidences, class_ids = [], [], []
    BB = ()
    new_box = []
    # loop over each of the layer outputs
    for output in layer_outputs:
        # loop over each of the object detections
        for detection in output:
            # extract the class id (label) and confidence (as a probability) of the current object detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == 0 or class_id == 2 or class_id == 3 or class_id == 4 or class_id == 5:
                # discard out weak predictions by ensuring the detected probability is greater than the minimum probability
                if confidence > CONFIDENCE:
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
    # perform the non maximum suppression given the scores defined before
    # idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences,score_threshold=0.4,nms_threshold=0.4)
    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]
            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in colors[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=thickness)
            new_box.append([x, y, w, h])
            # print(f"X1={X1, Y1}")
    # cv2.imshow('test', image)
    cv2.imwrite('detected with yolo2.jpg', image)
    # cv2.setMouseCallback('test', position)
    # key = cv2.waitKey(5000)
    #boxes : list of boxes in the image
    # cv2.setMouseCallback('test', position)
    # print(boxes)
    # if posList !=[]:
    #     for j in range(len(new_box)):
    #         x_min, y_min = new_box[j][0], new_box[j][1]
    #         w, h = new_box[j][2], new_box[j][3]
    #         x_max = x_min +w
    #         y_max = y_min +h
    #         if (posList[0][0]>x_min) and (posList[0][0]<x_max) and (posList[0][1]>y_min) and (posList[0][1]<y_max):
    #             BB=(x_min,y_min,w,h)
    #             X1 = x_min + int(w / 2)
    #             Y1 = y_min + int(h / 2)
    #             print(f"X''1={X1 - int(w / 4), Y1}")
    #             print(f"X1={X1,Y1}")
    #             print(f"X'1={X1+int(w / 4), Y1}")
    #             ######## break
    #             # posList.clear()
    #     cv2.destroyAllWindows()
    # print(f"X1={X1, Y1}")
    print(new_box)
    return new_box,image