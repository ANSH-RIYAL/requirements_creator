# AGENT_PROMPT_MAP

## ChatGPT Prompt Templates
- "Help me define the phases for a Python dependency analysis tool that generates requirements.txt"
- "Convert this user story into a SCOPE_DOC Phase plan for code analysis features"
- "Generate realistic JSON payload for a library signature database entry"
- "Design integration patterns for PyPI API and signature matching"
- "Create testing strategies for code analysis and version matching"

## Cursor Prompts

### Backend Development
- "Add a new route in `app.py` for receiving code analysis form submission"
- "Implement logic in `/src` to process Python code analysis"
- "Update `requirements_creator.py` to include new analysis method"
- "Create PyPI API integration in `/src/pypi_client.py`"
- "Implement error handling for malformed Python code"

### Core Logic Implementation
- "Create a code analyzer that handles Python import detection"
- "Implement signature matching with proper error handling"
- "Build version compatibility checking with validation and sanitization"
- "Add library signature extraction with appropriate logging"
- "Create database manager with fallback mechanisms"

### CLI Development
- "Create CLI commands for analyzing codebases"
- "Implement request/response validation for CLI arguments"
- "Add error handling and status codes for CLI operations"
- "Create help documentation for CLI commands"
- "Implement batch operations for multiple libraries"

## Replit Prompts

### Frontend Components
- "Create a clean HTML form to input Python code"
- "Generate `demo.html` template to display analysis results"
- "Build a table UI that displays generated requirements.txt"
- "Create a responsive interface for code input and results"
- "Build real-time status indicators for analysis progress"

### User Interface
- "Design a user-friendly interface for code analysis demo"
- "Create loading states for code processing"
- "Build error display for analysis failures"
- "Implement responsive design for mobile devices"
- "Add accessibility features for form inputs"

### Integration
- "Connect frontend form to Flask backend processing"
- "Implement real-time updates for analysis results"
- "Create user feedback mechanisms for form submission"
- "Build progress indicators for code analysis"
- "Add retry mechanisms for failed analysis"

## Integration Prompts

### Backend-Frontend Integration
- "Wire up `demo.html` form to Flask route `/process-code`"
- "Ensure error messages from analysis are displayed under form"
- "Connect frontend results display to backend analysis output"
- "Implement form validation between frontend and backend"

### Data Flow Integration
- "Connect code analyzer to signature database with proper error handling"
- "Integrate PyPI client with version matcher"
- "Link frontend form submission to backend analysis pipeline"
- "Create data validation between analysis components"

### Error Handling Integration
- "Implement comprehensive error handling across all analysis steps"
- "Add validation for Python code input"
- "Create fallback mechanisms for PyPI API failures"
- "Ensure graceful degradation when signature matching fails"

## Override Flags
- `#COMMERCIAL_FEATURE` → allow use of advanced code parsing libraries
- `#ALLOW_AUTH` → enable user session management or project storage
- `#IGNORE_STRUCTURE_CONSTRAINTS` → allow folder creation (use sparingly)
- `#COMPLEX_INTEGRATION` → allow advanced PyPI or external service integration
- `#REAL_TIME_FEATURES` → enable WebSocket or complex real-time updates
- `#ENTERPRISE_FEATURES` → enable advanced features and compliance

## Specific Implementation Prompts

### For Backend Services
```
"Implement [service name] that:
1. Handles Python code analysis and signature matching
2. Integrates with PyPI API for library metadata
3. Provides proper error handling for malformed code
4. Includes logging and monitoring for analysis steps
5. Follows the established patterns in /src/
Use the existing structure and maintain consistency."
```

### For Frontend Components
```
"Build a [component type] that:
1. Accepts Python code input from users
2. Displays analysis results and requirements.txt clearly
3. Handles analysis errors gracefully
4. Provides good user feedback during processing
5. Integrates with Flask backend routes
Use modern HTML/CSS and maintain responsive design."
```

### For Integration
```
"Connect [component A] to [component B] by:
1. Establishing proper data flow for code analysis
2. Implementing error handling for analysis failures
3. Adding validation for Python code input
4. Ensuring good user experience during processing
5. Following established Flask and CLI patterns
Maintain simplicity and avoid over-engineering."
``` 