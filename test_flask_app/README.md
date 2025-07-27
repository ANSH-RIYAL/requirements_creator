# Test Flask App

A simple Flask application for testing the Requirements Creator system.

## Features

- **Addition API**: POST endpoint that adds two numbers using numpy
- **Health Check**: GET endpoint that tests requests library
- **Simple Structure**: Minimal dependencies for testing

## Dependencies

- Flask
- numpy  
- requests

## Usage

### Run the app
```bash
python app.py
```

### Test endpoints

1. **Home page**
```bash
curl http://localhost:5000/
```

2. **Add numbers**
```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"num1": 5, "num2": 3}'
```

3. **Health check**
```bash
curl http://localhost:5000/health
```

## Expected Output

The Requirements Creator should detect:
- `flask` (for Flask, request, jsonify)
- `numpy` (for np.add, np.__version__)
- `requests` (for requests.get)

And generate a requirements.txt with compatible versions. 