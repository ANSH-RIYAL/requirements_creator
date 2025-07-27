# Requirements Creator

**Automatically generate precise Python requirements.txt files by analyzing your codebase**

Stop guessing library versions. This tool analyzes your Python code, identifies exactly which functions you're using, and generates a `requirements.txt` with the exact compatible versions.

## 🚀 Quick Start

### Install
```bash
pip install -r requirements.txt
```

### Use
```bash
# Analyze your codebase and generate requirements.txt
python3 main.py analyze /path/to/your/project

# If you're missing libraries in the database, add them automatically
python3 main.py analyze /path/to/your/project --auto-add
```

## 💡 How It Works

1. **Scans your code** - Analyzes all Python files to find library imports and function calls
2. **Matches signatures** - Compares your code usage against a database of library function signatures
3. **Finds compatible versions** - Identifies the exact library versions that support your code
4. **Generates requirements.txt** - Creates a precise requirements file with pinned versions

## 📋 Example

**Your code:**
```python
import numpy as np
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/add')
def add_numbers():
    result = np.add(5, 3)
    response = requests.get('https://api.example.com', timeout=5)
    return str(result)
```

**Generated requirements.txt:**
```
flask==3.1.1
numpy==2.2.6
requests==2.32.4
```

## 🎯 Key Benefits

- **No more dependency conflicts** - Get exact versions that work together
- **Save hours of debugging** - No more "it works on my machine" issues
- **Production-ready** - Generate requirements for deployment immediately
- **Automatic updates** - Keep your dependency database current

## 📚 Supported Libraries

Currently supports 50+ popular Python libraries including:
- **Web Frameworks**: Flask, Django, FastAPI
- **Data Science**: NumPy, Pandas, Matplotlib, Scikit-learn
- **HTTP Clients**: Requests, httpx
- **Database**: SQLAlchemy, psycopg2
- **And many more...**

## 🔧 Advanced Usage

### Add new libraries to the database
```bash
python3 main.py add library_name
```

### Batch add multiple libraries
```bash
python3 main.py batch-add numpy pandas matplotlib
```

### View database statistics
```bash
python3 main.py stats
```

## 🏢 Enterprise Integration

This tool is designed for teams and organizations that need reliable dependency management. It can be integrated into CI/CD pipelines, development workflows, and automated deployment processes.

**For enterprise implementation inquiries:** anshriyal@gmail.com

## 🤝 Contributing

We welcome contributions! This tool is designed to grow with the Python ecosystem.

---

**Stop guessing. Start building.**
