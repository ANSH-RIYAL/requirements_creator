import inspect
import importlib
import subprocess
import sys
import os
import tempfile
import venv
from typing import Dict, Any, List, Optional
import ast
import json


class IsolatedEnvironment:
    """Context manager for isolated Python environment"""
    
    def __init__(self, temp_dir: str):
        self.temp_dir = temp_dir
        self.original_sys_path = sys.path.copy()
        self.original_modules = set(sys.modules.keys())
    
    def __enter__(self):
        # Add the site-packages to Python path
        site_packages = os.path.join(self.temp_dir, "lib", "python3.8", "site-packages")
        if os.path.exists(site_packages):
            sys.path.insert(0, site_packages)
        
        # Also check for other possible site-packages locations
        for root, dirs, files in os.walk(self.temp_dir):
            if "site-packages" in root:
                sys.path.insert(0, root)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original Python path
        sys.path = self.original_sys_path
        
        # Clean up imported modules
        new_modules = set(sys.modules.keys()) - self.original_modules
        for module_name in new_modules:
            if module_name in sys.modules:
                del sys.modules[module_name]


class SignatureExtractor:
    """Extract function signatures from Python libraries"""
    
    def __init__(self):
        self.temp_dir = None
    
    def create_isolated_environment(self, package_spec: str) -> IsolatedEnvironment:
        """Create isolated environment and install package"""
        import tempfile
        import subprocess
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="req_creator_")
        
        try:
            # Create virtual environment
            venv.create(self.temp_dir, with_pip=True)
            
            # Determine pip path
            if os.name == 'nt':  # Windows
                pip_path = os.path.join(self.temp_dir, "Scripts", "pip")
            else:  # Unix/Linux/macOS
                pip_path = os.path.join(self.temp_dir, "bin", "pip")
            
            # Install the package
            print(f"  📦 Installing {package_spec}...")
            result = subprocess.run(
                [pip_path, "install", package_spec],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                print(f"  ⚠️  Installation failed: {result.stderr}")
                return None
            
            return IsolatedEnvironment(self.temp_dir)
            
        except Exception as e:
            print(f"  ❌ Failed to create environment: {e}")
            return None
    
    def extract_version_signatures(self, library_name: str, version: str) -> Dict[str, Any]:
        """Extract all function signatures for a specific version"""
        package_spec = f"{library_name}=={version}"
        
        env = self.create_isolated_environment(package_spec)
        if not env:
            return {}
        
        try:
            with env:
                module = importlib.import_module(library_name)
                signatures = self.extract_all_signatures(module)
                return signatures
        except Exception as e:
            print(f"  ❌ Failed to analyze {package_spec}: {e}")
            return {}
        finally:
            # Clean up temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                try:
                    shutil.rmtree(self.temp_dir)
                except:
                    pass
    
    def extract_all_signatures(self, module) -> Dict[str, Any]:
        """Extract all public function signatures from a module"""
        signatures = {}
        
        try:
            # Get all public attributes
            for name, obj in inspect.getmembers(module):
                if self.is_public_api(name, obj):
                    try:
                        if inspect.isfunction(obj) or inspect.ismethod(obj):
                            sig = inspect.signature(obj)
                            signatures[name] = self.format_signature(sig)
                        elif inspect.isclass(obj):
                            # Extract class methods
                            class_methods = self.extract_class_methods(obj)
                            if class_methods:
                                signatures[name] = class_methods
                    except (ValueError, TypeError, AttributeError) as e:
                        # Skip functions with problematic signatures
                        continue
            
            # Also check for submodules
            for name, obj in inspect.getmembers(module):
                if inspect.ismodule(obj) and hasattr(obj, '__name__'):
                    if obj.__name__.startswith(module.__name__):
                        sub_signatures = self.extract_all_signatures(obj)
                        if sub_signatures:
                            signatures[f"{name}"] = sub_signatures
            
        except Exception as e:
            print(f"  ⚠️  Error extracting signatures: {e}")
        
        return signatures
    
    def extract_class_methods(self, cls) -> Dict[str, Any]:
        """Extract methods from a class"""
        methods = {}
        
        try:
            for name, method in inspect.getmembers(cls):
                if (inspect.isfunction(method) or inspect.ismethod(method)) and self.is_public_api(name, method):
                    try:
                        sig = inspect.signature(method)
                        methods[name] = self.format_signature(sig)
                    except (ValueError, TypeError, AttributeError):
                        continue
        except Exception:
            pass
        
        return methods
    
    def is_public_api(self, name: str, obj) -> bool:
        """Determine if something is part of the public API"""
        # Skip private attributes
        if name.startswith('_'):
            return False
        
        # Skip built-in attributes
        if name in ['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__']:
            return False
        
        # Skip imported modules that aren't part of the package
        if inspect.ismodule(obj):
            if hasattr(obj, '__name__') and not obj.__name__.startswith('__'):
                return True
            return False
        
        return True
    
    def format_signature(self, sig) -> Dict[str, Any]:
        """Format signature into a structured format"""
        parameters = {}
        required_params = []
        optional_params = []
        defaults = {}
        
        for name, param in sig.parameters.items():
            parameters[name] = str(param)
            
            if param.default is inspect.Parameter.empty:
                required_params.append(name)
            else:
                optional_params.append(name)
                # Convert default to string for JSON serialization
                try:
                    defaults[name] = str(param.default)
                except:
                    defaults[name] = "Unknown"
        
        return {
            "signature": str(sig),
            "parameters": list(parameters.keys()),
            "required_params": required_params,
            "optional_params": optional_params,
            "defaults": defaults
        } 