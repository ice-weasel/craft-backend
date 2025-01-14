from flask import Flask, request, jsonify, send_file
import subprocess
import os
import signal
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import json
import os
from flow import create_flow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],  # Your React frontend URL
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
}) 

# Create a directory for storing received data
DATA_DIR = "received_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received",
                "message": "Request must contain JSON data"
            }), 400

        print("Received data:", data)
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save the received data to a file
        filename = f"data_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        create_flow(filepath)
        return jsonify({"message": "Data received successfully", "status": "success"}), 200
    
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500
    

@app.route('/download-sample', methods=['GET'])
def download_sample():
    try:
        # Path to the Python file you want to send
        file_path = './output_files/sample.py'
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='sample.py', mimetype='text/python')
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
   