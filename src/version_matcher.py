import json
import os
from typing import Dict, List, Set, Optional, Any
from packaging import version as pkg_version


class VersionMatcher:
    """Match function calls to compatible library versions"""
    
    def __init__(self, signature_db_path: str = "signature_database"):
        self.signature_db_path = signature_db_path
        self.signature_db = self.load_signature_database()
    
    def load_signature_database(self) -> Dict[str, Dict[str, Any]]:
        """Load the signature database from files"""
        db = {}
        
        if not os.path.exists(self.signature_db_path):
            return db
        
        for filename in os.listdir(self.signature_db_path):
            if filename.endswith('_signatures.json'):
                library_name = filename.replace('_signatures.json', '')
                file_path = os.path.join(self.signature_db_path, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        db[library_name] = data
                except Exception as e:
                    print(f"⚠️  Error loading {filename}: {e}")
        
        return db
    
    def find_compatible_versions(self, library_name: str, function_calls: Dict[str, Any]) -> List[str]:
        """Find all versions that support the observed function calls"""
        if library_name not in self.signature_db:
            print(f"⚠️  No signature data found for {library_name}")
            return []
        
        library_data = self.signature_db[library_name]
        versions = library_data.get("versions", {})
        
        compatible_versions = []
        
        for version_str, version_signatures in versions.items():
            if self.version_supports_calls(version_str, version_signatures, function_calls):
                compatible_versions.append(version_str)
        
        return compatible_versions
    
    def version_supports_calls(self, version_str: str, signatures: Dict[str, Any], function_calls: Dict[str, Any]) -> bool:
        """Check if a specific version supports all observed function calls"""
        for func_name, call_info in function_calls.items():
            if not self.function_compatible_in_version(func_name, call_info, signatures):
                return False
        
        return True
    
    def function_compatible_in_version(self, func_name: str, call_info: Dict[str, Any], signatures: Dict[str, Any]) -> bool:
        """Check if a specific function call is compatible with a version"""
        # Check if function exists in this version
        if func_name not in signatures:
            return False
        
        func_sig = signatures[func_name]
        called_args = set(call_info.get("arguments", []))
        
        # If no arguments were called, just check if function exists
        if not called_args:
            return True
        
        # Check if all called arguments exist in this version
        available_args = set(func_sig.get("parameters", []))
        
        # Check if function accepts **kwargs (any keyword arguments)
        accepts_kwargs = "kwargs" in available_args
        
        for arg in called_args:
            if arg not in available_args and not accepts_kwargs:
                return False
        
        return True
    
    def resolve_version_constraints(self, library_name: str, compatible_versions: List[str]) -> str:
        """Convert compatible versions to version constraint string"""
        if not compatible_versions:
            return None
        
        # Sort versions
        sorted_versions = sorted(compatible_versions, key=pkg_version.parse)
        
        # Choose the most recent stable version
        latest_version = sorted_versions[-1]
        
        # For now, return exact version
        # In a more sophisticated implementation, you could return ranges
        return f"=={latest_version}"
    
    def match_codebase_requirements(self, function_calls_by_library: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """Match function calls to version requirements for entire codebase"""
        requirements = {}
        
        for library_name, function_calls in function_calls_by_library.items():
            print(f"🔍 Analyzing {library_name}...")
            
            # Find compatible versions
            compatible_versions = self.find_compatible_versions(library_name, function_calls)
            
            if compatible_versions:
                # Resolve to version constraint
                version_constraint = self.resolve_version_constraints(library_name, compatible_versions)
                requirements[library_name] = version_constraint
                print(f"  ✅ {library_name}: {version_constraint} (from {len(compatible_versions)} compatible versions)")
            else:
                print(f"  ❌ {library_name}: No compatible versions found")
        
        return requirements
    
    def generate_requirements_txt(self, requirements: Dict[str, str], output_path: str = "requirements.txt") -> str:
        """Generate requirements.txt file"""
        with open(output_path, 'w') as f:
            for library, version_constraint in requirements.items():
                f.write(f"{library}{version_constraint}\n")
        
        print(f"📄 Generated requirements.txt at {output_path}")
        return output_path
    
    def analyze_and_generate_requirements(self, code_path: str, output_path: str = "requirements.txt") -> Dict[str, str]:
        """Complete pipeline: analyze code and generate requirements.txt"""
        from .code_analyzer import CodeAnalyzer
        
        # Analyze codebase
        analyzer = CodeAnalyzer()
        function_calls = analyzer.analyze_codebase(code_path)
        
        print(f"📊 Found function calls for {len(function_calls)} libraries:")
        for library, calls in function_calls.items():
            print(f"  📦 {library}: {len(calls)} functions")
        
        # Match to versions
        requirements = self.match_codebase_requirements(function_calls)
        
        # Generate requirements.txt
        if requirements:
            self.generate_requirements_txt(requirements, output_path)
        
        return requirements 