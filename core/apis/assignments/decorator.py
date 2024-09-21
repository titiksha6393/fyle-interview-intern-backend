from flask import Flask, jsonify
from core.apis.decorators import authenticate_principal

# Create a simple Flask app for testing
app = Flask(__name__)

@app.route('/test', methods=['POST'])
@authenticate_principal
def test_endpoint(principal, incoming_payload):
    return jsonify(success=True)