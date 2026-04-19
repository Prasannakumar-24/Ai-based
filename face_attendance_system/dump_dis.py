import dis
import face_recognition_cv2
with open("dis.txt", "w", encoding="utf-8") as f:
    dis.dis(face_recognition_cv2.FaceRecognitionManager.start_attendance_monitoring, file=f)
