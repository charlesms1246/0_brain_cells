import os
import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
import telebot
from telebot.handler_backends import SkipHandler as Skip
from telebot.types import InputFile
bot=telebot.TeleBot("7388798451:AAHAw644qjICpCAzfmNFCyQcW0zMXriT4mI")

app = Flask(__name__)
datum = { "primary" : {"CCTV_ID":"284619","Station":"C1","Zone":"Central Zone","Location-lat":13.059217,"Location-long": 80.233750},
"F456745GHK09" : {"CCTV_ID":"986821","Station":"B6","Zone":"East Zone","Location-lat":11.024802,"Location-long": 77.010389},
"third" : {"CCTV_ID":"728177","Station":"C2","Zone":"Central Zone","Location-lat":11.001057,"Location-long": 76.973492},
"fourth": {"CCTV_ID":"754446","Station":"B1","Zone":"South Zone","Location-lat":10.993843,"Location-long": 76.959645}}
# Function to process and save the received image
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
        imagepath=f"alert_{timestamp}.jpg"
        image_path = os.path.join(static_folder_path,imagepath) 

        # Save the image and log success/failure
        success = cv2.imwrite(image_path, img)
        if success:
            print(f"✅ Image saved as {image_path}")
            #bot.send_message(1286616647,"hi")
        else:
            print(f"❌ Failed to save image at {image_path}")

        # Process further (e.g., logging, additional analysis)
        print(f"Alert received from Camera ID: {data['camera_id']}")
        print(f"Location: {data['location']}")
        print(f"Police Station: {data['police_station']}")
        print(f"Object Detected: {data['object_detected']}")
        print(f"Date: {data['date']} Time: {data['time']}")
        moqe=data['camera_id']
        bot.send_photo(6241400372,photo=InputFile(f"D:/ARCS/static/alerts/{imagepath}"),caption=str("CCTV ID: "+datum[moqe]['CCTV_ID']+"\nStation: "+datum[moqe]['Station']+"\nZone: "+datum[moqe]['Zone']))
        bot.send_location(6241400372,latitude=datum[data['camera_id']]["Location-lat"],longitude=datum[data['camera_id']]["Location-long"],disable_notification=True,horizontal_accuracy=3)
    
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

# Main block to run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
