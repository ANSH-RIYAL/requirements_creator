#!/usr/bin/env python3
"""
Simple Flask App for Testing Requirements Creator
"""

from flask import Flask, request, jsonify
import numpy as np
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "message": "Simple Calculator API",
        "endpoints": {
            "/add": "POST - Add two numbers",
            "/health": "GET - Health check"
        }
    })

@app.route('/add', methods=['POST'])
def add_numbers():
    """Add two numbers using numpy"""
    try:
        data = request.json
        
        if not data or 'num1' not in data or 'num2' not in data:
            return jsonify({"error": "Please provide num1 and num2"}), 400
        
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        
        # Use numpy to add the numbers
        result = np.add(num1, num2)
        
        return jsonify({
            "num1": num1,
            "num2": num2,
            "result": float(result),
            "operation": "addition"
        })
        
    except ValueError:
        return jsonify({"error": "Invalid numbers provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Make a simple request to test requests library
        response = requests.get('https://httpbin.org/get', timeout=5)
        
        return jsonify({
            "status": "healthy",
            "numpy_version": np.__version__,
            "requests_status": response.status_code
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 