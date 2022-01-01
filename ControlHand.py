import cv2
import mediapipe as mp
import math
import serial
ser=serial.Serial("COM3",9600)



class vector:# used to calculate angles finger is rotated from coordinates.
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __str__(self) -> str:
        return str(self.x)+" "+str(self.y)+" "+str(self.z)
def cross(a,b):
    return vector(a.y*b.z-b.y*a.z,-(a.x*b.z-b.x*a.z),a.x*b.y-b.x*a.y)
def mag(v):
    return math.sqrt(v.x**2+v.y**2+v.z**2)
def dot(v1,v2):
    return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z
def angle(v1,v2):
    return math.acos(dot(v1,v2)/   (mag(v1)*mag(v2))  )
def subt(t1,t2):
    return vector(t2[0]-t1[0],t2[1]-t1[1],t2[2]-t1[2])







mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_styles = mp.solutions.drawing_styles
cap = cv2.VideoCapture(0)#video feed
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)


    #Capture specific coordinates that I am going to use from Mediapipe
    ct=0
    points = {}

    image.flags.writeable = False
    results = hands.process(image)
    imageHeight, imageWidth, _ = image.shape

    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in mp_hands.HandLandmark:
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                if(ct==0 or ct==2 or ct==4 or ct==5 or ct==7 or ct==9 or ct==11 or ct==13 or ct==15 or ct==17 or ct==19):#specific coordinates that I used
                    points[ct]=(normalizedLandmark.x,normalizedLandmark.y,normalizedLandmark.z)
                ct+=1


    #find angles of finger using Vector class and coordinates
    if(len(points)):

      #orientate palm
      v5=subt(points[0],points[5])
      v17=subt(points[0],points[17])
      palm=cross(v17,v5)


      #Find vector(direction) of fingers
      vt=subt(points[2],points[4])#vector thumb
      vi=subt(points[7],points[5])#vector index
      vm=subt(points[11],points[9])#vector middle
      vr=subt(points[15],points[13])#vector ring
      vp=subt(points[19],points[17])#vector pinky

      #find angles of fingers
      at=math.degrees(angle(vt,palm))#angle thumb
      ai=180-math.degrees(angle(vi,palm))+20#angle index
      am=180-math.degrees(angle(vm,palm))#angle middle
      ar=180-math.degrees(angle(vr,palm))+10#angle ring
      ap=180-math.degrees(angle(vp,palm))+15#angle pinky


    else:###Open hand if no hand is detected
      at=90
      ai=90
      am=90
      ar=90
      ap=90


    command=str(at)+" " +str(ai)+" " +str(am)+" " +str(ar)+" " +str(ap)+" "
    # print(command)      #testing
    ser.write(str.encode(command))###tell arduino how much to move each finger



    # Draw the hand annotations on the image. Mediapipe Documentation
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            drawing_styles.get_default_hand_landmark_style(),
            drawing_styles.get_default_hand_connection_style())
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()