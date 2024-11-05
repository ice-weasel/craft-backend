from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
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
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data received",
                "message": "Request must contain JSON data"
            }), 400

        # Log the received data
        logger.info(f"Received data: {json.dumps(data)[:200]}...")  # Log first 200 chars

        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save the received data to a file
        filename = f"data_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        # Return success response
        return jsonify({
            "message": "Data received and saved successfully",
            "filename": filename,
            "timestamp": timestamp,
            "size": len(json.dumps(data))
        }), 200

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return jsonify({
            "error": "Invalid JSON format",
            "message": str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Server error",
            "message": "An error occurred while processing the request"
        }), 500

# Optional: Add an endpoint to list all received files
@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        files = []
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(DATA_DIR, filename)
                file_stat = os.stat(filepath)
                files.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })
        
        return jsonify({
            "message": "Files retrieved successfully",
            "files": files
        }), 200
    
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return jsonify({
            "error": "Server error",
            "message": "An error occurred while listing files"
        }), 500

# Optional: Add an endpoint to retrieve a specific file
@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    try:
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                "error": "File not found",
                "message": f"File {filename} does not exist"
            }), 404
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        return jsonify({
            "message": "File retrieved successfully",
            "filename": filename,
            "data": data
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving file: {str(e)}")
        return jsonify({
            "error": "Server error",
            "message": "An error occurred while retrieving the file"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)