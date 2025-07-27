# Requirements Creator

**Automatically generate requirements.txt from code analysis**

A powerful tool that analyzes your Python codebase, extracts function calls, and automatically generates a `requirements.txt` file with the exact library versions that support your code.

## 🎯 What it does

- **Analyzes your code**: Extracts all function calls and their arguments from your Python codebase
- **Matches to versions**: Finds library versions that support your exact function usage
- **Generates requirements.txt**: Creates a precise requirements file with compatible versions
- **Fully automated**: No manual intervention needed - just provide the library name

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd requirements_creator

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Add a library to the database (fully automated)
python main.py add pandas

# Analyze a codebase and generate requirements.txt
python main.py analyze /path/to/your/code

# Add multiple libraries at once
python main.py batch-add pandas numpy matplotlib requests
```

### Programmatic Usage

```python
from src.requirements_creator import RequirementsCreator

# Initialize
creator = RequirementsCreator()

# Add a library to database
creator.add_library_to_database("pandas")

# Analyze codebase
requirements = creator.analyze_codebase("/path/to/your/code")
print(requirements)
# Output: {'pandas': '==2.0.0', 'numpy': '==1.24.0'}
```

## 🔧 How it Works

### 1. **Signature Database Construction**
- Automatically fetches latest versions from PyPI
- Creates isolated environments for each version
- Extracts all public function signatures
- Stores in JSON format for fast lookup

### 2. **Code Analysis**
- Parses your Python code using AST
- Extracts all import statements and function calls
- Maps function calls to their source libraries
- Identifies which arguments are used

### 3. **Version Matching**
- Compares your function calls against version signatures
- Finds all versions that support your exact usage
- Resolves to optimal version constraints
- Generates precise requirements.txt

## 📋 CLI Commands

### `analyze` - Analyze codebase
```bash
python main.py analyze /path/to/code [-o requirements.txt]
```

### `add` - Add library to database
```bash
python main.py add pandas [-v 20]
```

### `batch-add` - Add multiple libraries
```bash
python main.py batch-add pandas numpy matplotlib
```

### `list` - List analyzed libraries
```bash
python main.py list
```

### `stats` - Database statistics
```bash
python main.py stats
```

### `delete` - Remove library from database
```bash
python main.py delete pandas
```

### `update` - Update library in database
```bash
python main.py update pandas
```

## 🏗️ Architecture

```
src/
├── pypi_client.py          # PyPI API client
├── signature_extractor.py  # Function signature extraction
├── code_analyzer.py        # Code analysis and AST parsing
├── version_matcher.py      # Version compatibility matching
├── database_manager.py     # Signature database management
└── requirements_creator.py # Main orchestration class
```

## 📊 Supported Libraries

The system supports 50+ popular Python libraries including:

**Data Science:**
- pandas, numpy, matplotlib, seaborn, scikit-learn
- scipy, jupyter, plotly, bokeh, statsmodels

**Web & API:**
- requests, flask, django, fastapi, aiohttp
- beautifulsoup4, selenium, httpx, websockets

**Database & Storage:**
- sqlalchemy, psycopg2, pymongo, redis
- pandas-profiling, h5py, pyarrow

**Utilities:**
- click, argparse, tqdm, python-dotenv, pyyaml
- jinja2, markdown, lxml, python-dateutil

**Specialized:**
- tensorflow, pytorch, transformers, openai, langchain

## 🔍 Example Output

### Input Code
```python
import pandas as pd
import numpy as np

# Use pandas with specific arguments
df = pd.read_csv('data.csv', sep=',', header=0, engine='python')

# Use numpy
arr = np.array([1, 2, 3])
mean = np.mean(arr)
```

### Generated requirements.txt
```
pandas==2.0.0
numpy==1.24.0
```

## 🎯 Key Features

- **Deterministic**: No LLM guessing, pure algorithmic matching
- **Accurate**: Based on actual function signatures, not heuristics
- **Fast**: Once database is built, analysis is instant
- **Comprehensive**: Covers 50+ popular libraries
- **Automated**: Zero manual intervention required
- **Extensible**: Easy to add new libraries

## 🚨 Limitations

- Only analyzes static function calls (no dynamic imports)
- Focuses on keyword arguments (positional args harder to match)
- Requires internet connection for PyPI access
- May miss complex inheritance patterns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

If you encounter issues:

1. Check the database exists: `python main.py list`
2. Try updating a library: `python main.py update pandas`
3. Check database stats: `python main.py stats`
4. Open an issue with your code and error message

---

**Made with ❤️ for the Python community**
