import cv2
from tracker import *
from fluxo import *

# Criar objeto
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("novoVia5.mkv")

fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count/fps
minuto = duration/60

# Detecção de objetos da câmera Stable
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

ret, frame = cap.read()
r = cv2.selectROI(frame)

count = 0
# print(r)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        height, width, _ = frame.shape

        # Extract Region of interest
        # (176, 525, 790, 188)
        # Pegar o frame automático selecionar com o mouse e Enter pra salvar
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        # 1. Deteccao de objetos
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculo da area e remocao dos elementos pequenos
            area = cv2.contourArea(cnt)
            # Tamanho da area branca do objeto
            if area > 2000:
                cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if count < id:
                count = id

        # cv2.rectangle(frame, (0, 0), (x + w, y + h), (0, 255, 0), 3)
        cv2.imshow("roi", roi)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(30)
        if key == 27:
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

print("O número de carros foi " + str(count) + " em " + str(round(minuto, 3)) + " minutos.")

fluxohora = (count * 60)/minuto
print("O fluxo de tráfego de veículos por hora é de " + str(round(fluxohora)) + ".")
print("FPS: "+ str(round(fps, 3)))