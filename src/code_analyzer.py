import ast
import os
from typing import Dict, List, Set, Any
from collections import defaultdict


class FunctionCall:
    """Represents a function call found in code"""
    
    def __init__(self, function_name: str, module_name: str, arguments: Set[str], line_number: int):
        self.function_name = function_name
        self.module_name = module_name
        self.arguments = arguments
        self.line_number = line_number
    
    def __repr__(self):
        return f"FunctionCall({self.module_name}.{self.function_name}, args={self.arguments})"


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to extract import statements"""
    
    def __init__(self):
        self.imports = {}  # alias -> full_name
        self.from_imports = {}  # alias -> (module, name)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports[alias.asname or alias.name] = alias.name
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        module_name = node.module or ""
        for alias in node.names:
            full_name = f"{module_name}.{alias.name}" if module_name else alias.name
            self.from_imports[alias.asname or alias.name] = (module_name, alias.name)
        self.generic_visit(node)


class FunctionCallVisitor(ast.NodeVisitor):
    """AST visitor to extract function calls"""
    
    def __init__(self, imports: Dict[str, str], from_imports: Dict[str, tuple]):
        self.imports = imports
        self.from_imports = from_imports
        self.calls = []
        self.current_imports = set()
    
    def visit_Call(self, node):
        # Extract function name and arguments
        func_name, module_name = self.resolve_function_call(node.func)
        
        if func_name and module_name:
            arguments = self.extract_arguments(node)
            call = FunctionCall(
                function_name=func_name,
                module_name=module_name,
                arguments=arguments,
                line_number=getattr(node, 'lineno', 0)
            )
            self.calls.append(call)
        
        self.generic_visit(node)
    
    def resolve_function_call(self, node) -> tuple:
        """Resolve function name and module from AST node"""
        if isinstance(node, ast.Name):
            # Direct function call (e.g., func())
            func_name = node.id
            # Check if it's from an import
            if func_name in self.imports:
                return func_name, self.imports[func_name]
            elif func_name in self.from_imports:
                module, name = self.from_imports[func_name]
                return name, module
            else:
                # Could be built-in or local function
                return func_name, None
        
        elif isinstance(node, ast.Attribute):
            # Attribute access (e.g., module.func())
            if isinstance(node.value, ast.Name):
                # Check if the base is an import
                base_name = node.value.id
                attr_name = node.attr
                
                if base_name in self.imports:
                    return attr_name, self.imports[base_name]
                elif base_name in self.from_imports:
                    module, name = self.from_imports[base_name]
                    return attr_name, module
                else:
                    # Could be a module import
                    return attr_name, base_name
        
        return None, None
    
    def extract_arguments(self, node) -> Set[str]:
        """Extract argument names from function call"""
        arguments = set()
        
        # Positional arguments (we can't easily determine names)
        # So we'll focus on keyword arguments
        
        # Keyword arguments
        for kw in node.keywords:
            if kw.arg:
                arguments.add(kw.arg)
        
        return arguments


class CodeAnalyzer:
    """Analyze Python code to extract function calls"""
    
    def __init__(self):
        self.import_patterns = {
            "pandas": ["pandas", "pd"],
            "numpy": ["numpy", "np"],
            "matplotlib": ["matplotlib", "plt", "mpl"],
            "seaborn": ["seaborn", "sns"],
            "scikit-learn": ["sklearn"],
            "requests": ["requests"],
            "flask": ["flask"],
            "django": ["django"],
            "fastapi": ["fastapi"],
            "aiohttp": ["aiohttp"],
            "beautifulsoup4": ["bs4", "beautifulsoup"],
            "selenium": ["selenium"],
            "sqlalchemy": ["sqlalchemy"],
            "psycopg2": ["psycopg2"],
            "pymongo": ["pymongo"],
            "redis": ["redis"],
            "click": ["click"],
            "argparse": ["argparse"],
            "tqdm": ["tqdm"],
            "python-dotenv": ["dotenv"],
            "pyyaml": ["yaml"],
            "jinja2": ["jinja2"],
            "markdown": ["markdown"],
            "lxml": ["lxml"],
            "python-dateutil": ["dateutil"],
            "pytz": ["pytz"],
            "watchdog": ["watchdog"],
            "pathlib": ["pathlib"],
            "pillow": ["PIL"],
            "opencv-python": ["cv2"],
            "plotly": ["plotly"],
            "bokeh": ["bokeh"],
            "statsmodels": ["statsmodels"],
            "sympy": ["sympy"],
            "networkx": ["networkx"],
            "scipy": ["scipy"],
            "jupyter": ["jupyter"],
            "ipython": ["IPython"],
            "tensorflow": ["tensorflow", "tf"],
            "torch": ["torch"],
            "transformers": ["transformers"],
            "openai": ["openai"],
            "langchain": ["langchain"],
            "pandas-profiling": ["pandas_profiling"],
            "h5py": ["h5py"],
            "pyarrow": ["pyarrow"],
            "urllib3": ["urllib3"],
            "httpx": ["httpx"],
            "websockets": ["websockets"],
            "sqlite3": ["sqlite3"]
        }
    
    def analyze_codebase(self, code_path: str) -> Dict[str, Dict[str, Any]]:
        """Analyze entire codebase and extract function calls by library"""
        function_calls_by_library = defaultdict(lambda: defaultdict(lambda: {"arguments": set(), "calls": []}))
        
        for file_path in self.get_python_files(code_path):
            try:
                file_calls = self.analyze_file(file_path)
                for call in file_calls:
                    library_name = self.resolve_library_name(call.module_name)
                    if library_name:
                        function_calls_by_library[library_name][call.function_name]["arguments"].update(call.arguments)
                        function_calls_by_library[library_name][call.function_name]["calls"].append(call)
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
        
        # Convert sets to lists for JSON serialization
        result = {}
        for library, functions in function_calls_by_library.items():
            result[library] = {}
            for func_name, func_data in functions.items():
                result[library][func_name] = {
                    "arguments": list(func_data["arguments"]),
                    "calls": len(func_data["calls"])
                }
        
        return result
    
    def analyze_file(self, file_path: str) -> List[FunctionCall]:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Extract imports
            import_visitor = ImportVisitor()
            import_visitor.visit(tree)
            
            # Extract function calls
            call_visitor = FunctionCallVisitor(import_visitor.imports, import_visitor.from_imports)
            call_visitor.visit(tree)
            
            return call_visitor.calls
            
        except Exception as e:
            print(f"⚠️  Error parsing {file_path}: {e}")
            return []
    
    def get_python_files(self, path: str) -> List[str]:
        """Get all Python files in a directory recursively"""
        python_files = []
        
        if os.path.isfile(path) and path.endswith('.py'):
            return [path]
        
        for root, dirs, files in os.walk(path):
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files
    
    def resolve_library_name(self, module_name: str) -> str:
        """Resolve module name to library name"""
        if not module_name:
            return None
        
        # Direct mapping
        for library, patterns in self.import_patterns.items():
            if module_name in patterns:
                return library
        
        # Handle submodules
        for library, patterns in self.import_patterns.items():
            for pattern in patterns:
                if module_name.startswith(pattern + '.'):
                    return library
        
        return None
    
    def analyze_code_string(self, code_string: str) -> Dict[str, Dict[str, Any]]:
        """Analyze code from a string and extract function calls by library"""
        function_calls_by_library = defaultdict(lambda: defaultdict(lambda: {"arguments": set(), "calls": []}))
        
        try:
            tree = ast.parse(code_string)
            
            # Extract imports
            import_visitor = ImportVisitor()
            import_visitor.visit(tree)
            
            # Extract function calls
            call_visitor = FunctionCallVisitor(import_visitor.imports, import_visitor.from_imports)
            call_visitor.visit(tree)
            
            # Process function calls
            for call in call_visitor.calls:
                library_name = self.resolve_library_name(call.module_name)
                if library_name:
                    function_calls_by_library[library_name][call.function_name]["arguments"].update(call.arguments)
                    function_calls_by_library[library_name][call.function_name]["calls"].append(call)
            
            # Also include imported libraries that don't have function calls
            # This ensures they get added to the database for version matching
            for alias, full_name in import_visitor.imports.items():
                library_name = self.resolve_library_name(full_name)
                if library_name and library_name not in function_calls_by_library:
                    function_calls_by_library[library_name] = {}
            
            for alias, (module, name) in import_visitor.from_imports.items():
                library_name = self.resolve_library_name(module)
                if library_name and library_name not in function_calls_by_library:
                    function_calls_by_library[library_name] = {}
            
            # Convert sets to lists for JSON serialization
            result = {}
            for library, functions in function_calls_by_library.items():
                result[library] = {}
                for func_name, func_data in functions.items():
                    result[library][func_name] = {
                        "arguments": list(func_data["arguments"]),
                        "calls": len(func_data["calls"])
                    }
            
            return result
            
        except Exception as e:
            print(f"⚠️  Error parsing code string: {e}")
            return {} 