# STRUCTURE_MAP

## Directory Layout
```
/
├── app.py                     # Flask web application
├── main.py                    # CLI interface
├── requirements.txt           # Python dependencies
├── src/                       # Core logic modules
│   ├── __init__.py
│   ├── code_analyzer.py       # Python code analysis
│   ├── database_manager.py    # Signature database operations
│   ├── pypi_client.py         # PyPI API integration
│   ├── requirements_creator.py # Main orchestration class
│   ├── signature_extractor.py # Library signature extraction
│   └── version_matcher.py     # Version compatibility matching
├── templates/                 # Flask templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   └── demo.html             # Interactive demo
├── static/                   # Static assets
│   └── css/
│       └── style.css         # Web styles
├── signature_database/       # Library signature storage
│   ├── flask_signatures.json
│   ├── numpy_signatures.json
│   └── requests_signatures.json
├── knowledge_docs/           # Documentation templates
└── test_flask_app/          # Test application
```

## Layer Responsibilities
- **/src:** Core business logic, code analysis, signature matching, PyPI integration
- **/templates:** Flask HTML templates for web interface
- **/static:** CSS styles and static assets
- **/signature_database:** JSON files containing library function signatures
- **/knowledge_docs:** Project documentation templates
- **app.py:** Flask web application entry point
- **main.py:** CLI interface entry point

## API Integration Rules
- Web interface uses form-based submissions to `/process-code`
- CLI interface uses command-line arguments and subcommands
- No REST API endpoints - direct form processing and CLI commands
- JSON responses for internal data structures (signature database)
- Error handling through Flask flash messages and CLI error output

## Cursor/Replit Constraints
- **Cursor:** Backend logic in `/src`, Flask routes in `app.py`, CLI in `main.py`
- **Replit:** Frontend templates in `/templates`, CSS in `/static/css`
- **Fixed Structure:** Maintain existing directory structure and file naming
- **Integration:** Flask templates connect to backend logic through form submissions

## External Service Integration
- **PyPI API:** Integrated through `pypi_client.py` for library metadata
- **Error Handling:** Graceful fallback when PyPI unavailable, local database backup
- **Performance:** Efficient caching in signature database to minimize API calls
- **Fallback Strategies:** Local signature database provides offline functionality

## Project Setup Tips
- Install dependencies: `pip install -r requirements.txt`
- Run web interface: `python app.py`
- Run CLI: `python main.py [command]`
- Development server runs on `http://localhost:5000`
- No complex configuration required - self-contained application 