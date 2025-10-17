# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

@app.route('/collect', methods=['POST'])
def collect_data():
    """
    This endpoint receives behavioral data from the frontend,
    prints it to the console, and sends back a success message.
    """
    # Get the JSON data sent from the browser
    session_data = request.get_json()

    # For now, we'll just print it to see if it's working
    print("✅ Data received from frontend:")
    print(session_data)

    # Send a response back to the browser
    return jsonify({"status": "success", "message": "Data received"}), 201

# This allows you to run the app directly from the command line
if __name__ == '__main__':
    app.run(debug=True, port=5000)