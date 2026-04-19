import dis
import face_recognition_cv2
with open("dis_recognize.txt", "w", encoding="utf-8") as f:
    dis.dis(face_recognition_cv2.FaceRecognitionManager.recognize_face, file=f)
