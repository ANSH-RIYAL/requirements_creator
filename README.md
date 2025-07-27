# Requirements Creator

**Automatically generate precise Python requirements.txt files by analyzing your codebase**

Stop guessing library versions. This tool analyzes your Python code, identifies exactly which functions you're using, and generates a `requirements.txt` with the exact compatible versions.

## 🌐 Live Demo

**Try it online!** Visit the interactive web demo to see Requirements Creator in action:
- **Demo URL**: Run `python3 app.py` and visit `http://localhost:5000/demo`
- **Landing Page**: Run `python3 app.py` and visit `http://localhost:5000`

The web interface provides:
- Interactive code input with syntax highlighting
- Sample code examples (Flask, Data Science, ML, API)
- Real-time dependency analysis
- Copy-to-clipboard functionality
- Professional landing page with feature showcase

## 🚀 Quick Start

### Install
```bash
pip install -r requirements.txt
```

### Use (Command Line)
```bash
# Analyze your codebase and generate requirements.txt
python3 main.py analyze /path/to/your/project

# If you're missing libraries in the database, add them automatically
python3 main.py analyze /path/to/your/project --auto-add
```

### Use (Web Interface)
```bash
# Start the web server
python3 app.py

# Open your browser to:
# - Landing page: http://localhost:5000
# - Interactive demo: http://localhost:5000/demo
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
- **Web interface** - Easy-to-use demo for quick testing
- **Command line** - Full-featured CLI for automation and CI/CD

## 📚 Supported Libraries

Currently supports 50+ popular Python libraries including:
- **Web Frameworks**: Flask, Django, FastAPI
- **Data Science**: NumPy, Pandas, Matplotlib, Scikit-learn
- **HTTP Clients**: Requests, httpx
- **Database**: SQLAlchemy, psycopg2
- **And many more...**

## 🔧 Advanced Usage

### Command Line Interface

#### Add new libraries to the database
```bash
python3 main.py add library_name
```

#### Batch add multiple libraries
```bash
python3 main.py batch-add numpy pandas matplotlib
```

#### View database statistics
```bash
python3 main.py stats
```

#### List all analyzed libraries
```bash
python3 main.py list
```

#### Update a library in the database
```bash
python3 main.py update library_name
```

#### Delete a library from database
```bash
python3 main.py delete library_name
```

### Web Interface Features

- **Interactive Demo**: Paste your Python code and get instant results
- **Sample Examples**: Pre-loaded examples for common use cases
- **Real-time Analysis**: See exactly which functions are detected
- **Copy Results**: One-click copying of generated requirements.txt
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🏗️ Project Structure

```
├── main.py                    # CLI interface
├── app.py                     # Web interface (Flask)
├── requirements.txt           # Python dependencies
├── src/                       # Core logic
│   ├── requirements_creator.py
│   ├── code_analyzer.py
│   ├── database_manager.py
│   ├── pypi_client.py
│   ├── signature_extractor.py
│   └── version_matcher.py
├── templates/                 # Web templates
│   ├── base.html
│   ├── index.html
│   └── demo.html
├── static/css/               # Web styles
│   └── style.css
└── signature_database/       # Library signatures
    ├── flask_signatures.json
    ├── numpy_signatures.json
    └── requests_signatures.json
```

## 🏢 Enterprise Integration

This tool is designed for teams and organizations that need reliable dependency management. It can be integrated into CI/CD pipelines, development workflows, and automated deployment processes.

**For enterprise implementation inquiries:** anshriyal@gmail.com

## 🤝 Contributing

We welcome contributions! This tool is designed to grow with the Python ecosystem.

---

**Stop guessing. Start building.**

## 📈 Recent Progress & Updates

### ✅ **Latest Features (July 2025)**

**🌐 Web Interface Integration**
- **Interactive Demo**: Live web demo at `/demo` with real-time code analysis
- **Auto-Add Libraries**: New libraries encountered in demo are automatically added to database
- **Complete Requirements.txt**: Always generates full requirements.txt even when version matching fails
- **Covered Libraries Display**: Real-time view of libraries in signature database
- **Responsive Design**: Professional landing page with Bootstrap 5.3.0

**🔧 Enhanced Backend**
- **String Analysis**: Added `analyze_code_string()` method for web demo
- **Import Detection**: Recognizes all imported libraries, not just function calls
- **Fallback Generation**: Includes libraries without versions when exact matching fails
- **Unified Logic**: Same backend powers both CLI and web interfaces

**📊 Database Coverage**
- **Current Libraries**: flask, numpy, requests (with function signatures)
- **Auto-Expansion**: Database grows automatically as users try new libraries
- **Manual Addition**: Reliable CLI commands for adding specific libraries

### ⚠️ **Important Notes**

**Auto-Add Reliability**: While the web demo automatically attempts to add new libraries, this process can sometimes fail for complex libraries (like pandas, matplotlib) due to signature extraction challenges. For reliable library addition, use the CLI commands:

```bash
# Reliable manual addition
python3 main.py add library_name
python3 main.py batch-add pandas matplotlib seaborn
```

**Best Practices**:
- Use the web demo for quick testing and exploration
- Use CLI commands for reliable library database expansion
- The system gracefully handles failures and always provides useful output
