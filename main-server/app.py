from flask import Flask, render_template, Response, jsonify, request
from flask_socketio import SocketIO, emit
import cv2
import os
import base64
import numpy as np
import time
from threading import Thread
# import telegram
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
@socketio.on('connect')
def handle_connect():
    print("✅ A client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("⚠️ A client disconnected")

# TELEGRAM_BOT_TOKEN  = "7654914375:AAEjH7rlhcXXb3NuL_ZBCV4291_9hqkZL1c"
# TELEGRAM_CHAT_ID  = "6120861716"

cameras_info = {
    "secondary": {
        "cctv_id": "K12TJHV647BB",
        "address": "C2, Government Arts College Rd, Coimbatore, TN",
        "officer_id": "9861341",
        "Station": "C1",
        "officer_name": "Charles M S",
        "officer_post": "Senior Constable",
        "officer_phone": "+91 1234567890",
        "object": "Fire",
        "channel": "4.2GHz",
        "url": "http://192.168.55.1:5002/video_feed"                                    
    },
    "third": {
        "cctv_id": "X67PQRW892XZ",
        "address": "Police Station Sector 12, Noida, Uttar Pradesh",
        "officer_id": "7654321",
        "Station": "C2",
        "officer_name": "Ravi Prakash Singh",
        "officer_post": "Inspector",
        "officer_phone": "+91 9876543210",
        "object": "none",
        "channel": "5GHz",
        "url": "http://192.168.251.216:5004/video_feed"
    },
    "fourth": {
        "cctv_id": "F456745GHK09",
        "address": "Test Fire Station",
        "officer_id": "12345",
        "Station": "C3",
        "officer_name": "Arshad Ahmed",
        "officer_post": "Inspector",
        "officer_phone": "+91 9876543210",
        "object": "none",
        "channel": "5GHz",
        "url": "http://192.168.251.223:5005/video_feed"
    },
    # Add other cameras here...
}

# Global variable to store the latest detection info
latest_detection = None

@app.route('/')
def index():
    return render_template('index.html', cameras_info=cameras_info)

@app.route('/get_camera_info/<cctv_id>', methods=['GET'])
def get_camera_info(cctv_id):
    if cctv_id in cameras_info:
        return jsonify(cameras_info[cctv_id])
    return jsonify({"error": "Camera not found"}), 404

@app.route('/camera_feed/<camera_id>')
def camera_feed(camera_id):
    if camera_id not in cameras_info:
        return jsonify({"error": "Camera not found"}), 404

    camera_url = cameras_info[camera_id]["url"]

    def generate_frames():
        cap = cv2.VideoCapture(camera_url)
        if not cap.isOpened():
            print(f"❌ Error: Could not open processed feed for camera {camera_id}")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"⚠️ Warning: No frame from {camera_id}")
                break

            
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
            time.sleep(0.05)

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def process_alert(data):
    try:
        # Decode the base64 image data back into binary form
        image_data = base64.b64decode(data['image'])
        
        # Convert the binary data into a NumPy array (image format)
        np_img = np.frombuffer(image_data, dtype=np.uint8)
        
        # Decode the NumPy array into an OpenCV image (BGR format)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        
        # Check if the image is properly decoded
        if img is None:
            print("❌ Image decoding failed.")
            return
        else:
            print("✅ Image decoded successfully.")

        # Check image size
        if img is None or img.size == 0:
            print("❌ Image is empty or not valid.")
            return
        else:
            print(f"✅ Image size: {img.shape}")

        # Get the absolute path for saving images
        static_folder_path = os.path.join(os.getcwd(), 'static', 'alerts')

        # Ensure the 'static/alerts' directory exists
        if not os.path.exists(static_folder_path):
            os.makedirs(static_folder_path)
            print(f"✅ Created directory {static_folder_path}")
        else:
            print(f"✅ Directory {static_folder_path} already exists.")
        
        # Create the image path with timestamp
        timestamp = data['date'] + "_" + data['time'].replace(":", "-")
        image_path = os.path.join(static_folder_path, f"alert_{timestamp}.jpg")

        # Save the image and log success/failure
        success = cv2.imwrite(image_path, img)
        if success:
            print(f"✅ Image saved as {image_path}")
        else:
            print(f"❌ Failed to save image at {image_path}")

        # Process further (e.g., logging, additional analysis)
        print(f"Alert received from Camera ID: {data['camera_id']}")
        print(f"Location: {data['location']}")
        print(f"Police Station: {data['police_station']}")
        print(f"Object Detected: {data['object_detected']}")
        print(f"Date: {data['date']} Time: {data['time']}")
    
    except Exception as e:
        print(f"⚠️ Error while processing the alert: {e}")

# Route to receive the alert POST request
@app.route('/alert', methods=['POST'])
def alert():
    try:
        # Get the incoming JSON data
        data = request.get_json()
        
        # Process the alert data (image decoding and handling)
        process_alert(data)
        
        # Send a response back to acknowledge receipt
        return jsonify({"status": "success", "message": "Alert received and processed."}), 200
    
    except Exception as e:
        # If there's an error, return an error response
        print(f"⚠️ Error receiving alert: {e}")
        return jsonify({"status": "error", "message": "Failed to process the alert."}), 500
@app.route('/update_feed', methods=['POST'])
def update_feed():
    global latest_detection  # Use the global variable for latest detection  

    try:
        data = request.get_json()
        camera_id = data.get('camera_id')
        new_url = data.get('url')
        object1 = data.get('object')
        if camera_id in cameras_info and new_url:
            cameras_info[camera_id]["url"] = new_url
            cameras_info[camera_id]["object"] = object1
            latest_detection = cameras_info[camera_id]

            print(f"✅ Successfully updated feed for camera {camera_id}: {new_url}")
            return jsonify({"message": "Feed updated successfully", **cameras_info[camera_id]}), 200
        else:
            return jsonify({"error": "Invalid camera_id or URL"}), 400

    except Exception as e:
        print(f"⚠️ Error while updating feed: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
# 🔹 API: Receive detection alerts
@app.route('/send_alert', methods=['POST'])
def send_alert():
    global latest_detection
    data = request.get_json()

    camera_id = data.get("camera_id")
    location = data.get("location")
    image_url = data.get("image_url")
    object1=data.get("object")

    if camera_id and location and image_url:
        latest_detection = {
            "cctv_id": camera_id,   
            "address": location,
            "url": image_url,
            "object": object1
        }
        socketio.emit('new_alert', latest_detection, broadcast=True)
        return jsonify({"message": "Alert sent successfully"}), 200
    else:
        return jsonify({"error": "Missing required data"}), 400

@app.route('/latest_detection', methods=['GET'])
def latest_detection_info():
    if latest_detection:
        return jsonify(latest_detection)
    return jsonify({"error": "No camera detected"}), 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

