# FOUNDATION_KNOWLEDGE

## Build Philosophy
- **Core Values**: Precision, Automation, Reliability, User Experience
- **Primary Focus**: Technical excellence in dependency management and code analysis
- **Development Priority**: Balance between code quality and practical utility for Python developers
- **Simplicity First**: Complex problems solved with elegant, maintainable solutions

## AI Agent Roles & Division of Labor
- **Cursor Role:** Backend logic, Flask routes, code analysis algorithms, signature extraction, version matching
- **Replit Role:** Frontend components (HTML/CSS/JS), user interface design, responsive web design
- **ChatGPT Role:** Project scoping, documentation refinement, prompt creation, API integration patterns

## Development Rules & Constraints
- **Project Structure:** Fixed structure with `src/` for core logic, `templates/` for web UI, `signature_database/` for library data
- **Stack Limitations:** Flask backend, HTML/CSS/JS frontend, no complex frameworks or databases
- **Code Organization:** Modular design with separate analyzers, extractors, and matchers
- **Integration Patterns:** RESTful API endpoints with JSON responses, form-based web interface
- **AI Service Integration:** Minimal external dependencies, focus on local code analysis
- **Context Management:** Stateless analysis, no persistent user sessions required

## External Dependencies
- **Primary Services:** PyPI API for library metadata and version information
- **Secondary Services:** None - designed to be self-contained with local signature database
- **Rate Limits & Costs:** Free PyPI API usage with rate limiting considerations
- **Fallback Strategies:** Local signature database provides offline functionality, graceful degradation when PyPI unavailable

## Quality Assurance Guidelines
- **Testing Strategy:** Unit tests for core analysis functions, integration tests for web interface
- **Error Handling:** Comprehensive error handling for malformed code, network issues, API failures
- **Performance Requirements:** Sub-second analysis for typical codebases, responsive web interface
- **User Experience:** Clear error messages, helpful feedback, intuitive web interface
- **AI Service Reliability:** Robust fallback mechanisms when external services fail

## What We're NOT Doing
- Complex user authentication or session management
- Real-time collaborative features or WebSocket connections
- Advanced code parsing beyond import and function call detection
- Integration with version control systems or CI/CD platforms
- Complex dependency resolution algorithms (focus on exact version matching)

## Output Goals
- **Core Functionality:** Generate accurate requirements.txt files from code analysis
- **Web Interface:** Provide intuitive demo and landing page for easy testing
- **CLI Interface:** Full-featured command line tool for automation and scripting
- **Performance:** Fast analysis of typical Python projects (under 5 seconds)
- **Reliability:** Consistent results across different codebases and environments 