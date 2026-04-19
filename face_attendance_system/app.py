
from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
from database import DatabaseManager
from face_recognition_cv2 import FaceRecognitionManager
import os
from datetime import datetime

app = Flask(__name__)

# Managers will be set by main.py
db = None
face_manager = None

def set_managers(db_mgr, fm_mgr):
    global db, face_manager
    db = db_mgr
    face_manager = fm_mgr

camera = None
monitoring_active = False

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def release_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    global monitoring_active
    cam = get_camera()
    while monitoring_active:
        success, frame = cam.read()
        if not success:
            break
        else:
            try:
                user_id, name, confidence, face_box = face_manager.recognize_face(frame)
                if face_box is not None:
                    x, y, w, h = face_box
                    if user_id and name and confidence >= 55.0:
                        db.mark_attendance(user_id, name)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name} Present", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        db.mark_attendance("unknown", "Unknown")
            except Exception as e:
                print(f"Error in recognition loop: {e}")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if not monitoring_active:
        # Return empty/black image if not active
        return Response(b'', mimetype='image/jpeg')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/toggle_monitoring', methods=['POST'])
def toggle_monitoring():
    global monitoring_active
    monitoring_active = not monitoring_active
    if not monitoring_active:
        release_camera()
    return jsonify({"active": monitoring_active})

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    records = db.get_attendance_records()
    for r in records:
        if isinstance(r['check_in_time'], datetime):
            r['check_in_time'] = r['check_in_time'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(records)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    registered = face_manager.get_registered_users_count()
    today_records = db.get_today_attendance()
    return jsonify({
        "registered": registered,
        "today": len(today_records)
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    
    if not user_id or not name:
        return jsonify({"success": False, "message": "Missing fields"}), 400
        
    existing = db.get_user_by_id(user_id)
    if existing:
        return jsonify({"success": False, "message": "User ID already exists"}), 400

    # For capturing faces, we need the camera.
    # We will temporarily stop monitoring if it is active.
    global monitoring_active
    was_active = monitoring_active
    if monitoring_active:
        monitoring_active = False
        release_camera()

    # capture_face_images uses its own camera logic internally.
    try:
        success = face_manager.capture_face_images(user_id, name)
    except Exception as e:
        print(f"Error capturing: {e}")
        success = False

    if was_active:
        monitoring_active = True

    if success:
        return jsonify({"success": True, "message": "User registered successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to register user"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
