from typing import Dict, List, Any, Optional
import os
import time

from .pypi_client import PyPIClient
from .signature_extractor import SignatureExtractor
from .database_manager import SignatureDBManager
from .version_matcher import VersionMatcher
from .code_analyzer import CodeAnalyzer


class RequirementsCreator:
    """Main class for creating requirements.txt from code analysis"""
    
    def __init__(self, db_path: str = "signature_database"):
        self.pypi_client = PyPIClient()
        self.signature_extractor = SignatureExtractor()
        self.db_manager = SignatureDBManager(db_path)
        self.version_matcher = VersionMatcher(db_path)
        self.code_analyzer = CodeAnalyzer()
    
    def add_library_to_database(self, library_name: str, max_versions: int = 10) -> Dict[str, Any]:
        """Add a library to the signature database (fully automated)"""
        print(f"🔍 Starting automatic analysis of {library_name}")
        
        # Check if already analyzed
        existing_data = self.db_manager.load_library_signatures(library_name)
        if existing_data:
            print(f"📋 {library_name} already analyzed. Re-analyzing...")
        
        # Get latest versions from PyPI
        print(f"📦 Fetching versions for {library_name}...")
        versions = self.pypi_client.get_latest_versions(library_name, max_versions)
        
        if not versions:
            print(f"❌ No versions found for {library_name}")
            return {}
        
        print(f"📊 Found {len(versions)} versions: {', '.join(versions[-5:])}...")
        
        # Extract signatures for each version
        all_signatures = {}
        successful_versions = 0
        
        for version in versions:
            print(f"  🔧 Analyzing {library_name}=={version}...")
            try:
                signatures = self.signature_extractor.extract_version_signatures(library_name, version)
                if signatures:
                    all_signatures[version] = signatures
                    successful_versions += 1
                    print(f"    ✅ Extracted {len(signatures)} functions")
                else:
                    print(f"    ⚠️  No signatures extracted")
            except Exception as e:
                print(f"    ❌ Failed: {e}")
            
            # Small delay to be nice to PyPI
            time.sleep(0.1)
        
        # Save to database
        if all_signatures:
            self.db_manager.save_library_signatures(library_name, all_signatures)
            print(f"🎉 {library_name} successfully added to database! ({successful_versions}/{len(versions)} versions)")
        else:
            print(f"❌ Failed to extract any signatures for {library_name}")
        
        return all_signatures
    
    def analyze_codebase(self, code_path: str, output_path: str = "requirements.txt", auto_add_missing: bool = False) -> Dict[str, str]:
        """Analyze codebase and generate requirements.txt"""
        print(f"📁 Analyzing codebase at: {code_path}")
        
        # Extract function calls from codebase
        function_calls = self.code_analyzer.analyze_codebase(code_path)
        
        if not function_calls:
            print("❌ No function calls found in codebase")
            return {}
        
        print(f"📊 Found function calls for {len(function_calls)} libraries:")
        for library, calls in function_calls.items():
            print(f"  📦 {library}: {len(calls)} functions")
        
        # Check which libraries need to be added to database
        missing_libraries = []
        for library_name in function_calls.keys():
            if not self.db_manager.library_exists(library_name):
                missing_libraries.append(library_name)
        
        # Handle missing libraries
        if missing_libraries:
            print(f"\n⚠️  Found {len(missing_libraries)} libraries not in signature database:")
            for library in missing_libraries:
                print(f"  📦 {library}")
            
            if auto_add_missing:
                print(f"\n🔧 Auto-adding {len(missing_libraries)} libraries to database...")
                for library in missing_libraries:
                    self.add_library_to_database(library)
            else:
                print(f"\n❓ Would you like to add these libraries to the signature database?")
                print("   This will allow for accurate version matching.")
                print("   Libraries to add:", ", ".join(missing_libraries))
                
                while True:
                    response = input("   Add libraries? (y/n): ").lower().strip()
                    if response in ['y', 'yes']:
                        print(f"\n🔧 Adding {len(missing_libraries)} libraries to database...")
                        for library in missing_libraries:
                            self.add_library_to_database(library)
                        break
                    elif response in ['n', 'no']:
                        print("⚠️  Skipping missing libraries. Version matching may be incomplete.")
                        break
                    else:
                        print("   Please enter 'y' or 'n'")
        
        # Match function calls to versions
        requirements = self.version_matcher.match_codebase_requirements(function_calls)
        
        # Generate requirements.txt
        if requirements:
            self.version_matcher.generate_requirements_txt(requirements, output_path)
            print(f"✅ Generated requirements.txt with {len(requirements)} libraries")
        else:
            print("❌ No compatible versions found for any libraries")
        
        return requirements
    
    def list_analyzed_libraries(self) -> List[str]:
        """List all libraries in the database"""
        return self.db_manager.list_analyzed_libraries()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the signature database"""
        return self.db_manager.get_database_stats()
    
    def delete_library(self, library_name: str) -> bool:
        """Delete a library from the database"""
        return self.db_manager.delete_library_signatures(library_name)
    
    def update_library(self, library_name: str) -> Dict[str, Any]:
        """Update a library in the database"""
        print(f"🔄 Updating {library_name}...")
        return self.add_library_to_database(library_name)
    
    def quick_analyze(self, code_path: str, libraries: List[str] = None) -> Dict[str, str]:
        """Quick analysis with pre-specified libraries"""
        print(f"⚡ Quick analysis of {code_path}")
        
        # Add specified libraries to database if needed
        if libraries:
            for library in libraries:
                if not self.db_manager.library_exists(library):
                    print(f"📦 Adding {library} to database...")
                    self.add_library_to_database(library)
        
        # Analyze codebase
        return self.analyze_codebase(code_path)
    
    def batch_add_libraries(self, libraries: List[str]) -> Dict[str, bool]:
        """Add multiple libraries to database"""
        results = {}
        
        print(f"📦 Batch adding {len(libraries)} libraries...")
        for i, library in enumerate(libraries, 1):
            print(f"[{i}/{len(libraries)}] Processing {library}...")
            try:
                signatures = self.add_library_to_database(library)
                results[library] = bool(signatures)
            except Exception as e:
                print(f"❌ Failed to add {library}: {e}")
                results[library] = False
        
        successful = sum(results.values())
        print(f"✅ Batch complete: {successful}/{len(libraries)} libraries added successfully")
        
        return results
    
    def analyze_code_string(self, code_string: str, auto_add_missing: bool = False) -> Dict[str, str]:
        """Analyze code from a string and generate requirements"""
        print(f"📝 Analyzing code string...")
        
        # Extract function calls from code string
        function_calls = self.code_analyzer.analyze_code_string(code_string)
        
        if not function_calls:
            print("❌ No function calls found in code")
            return {}
        
        print(f"📊 Found function calls for {len(function_calls)} libraries:")
        for library, calls in function_calls.items():
            print(f"  📦 {library}: {len(calls)} functions")
        
        # Check which libraries need to be added to database
        missing_libraries = []
        for library_name in function_calls.keys():
            if not self.db_manager.library_exists(library_name):
                missing_libraries.append(library_name)
        
        # Handle missing libraries
        if missing_libraries:
            print(f"\n⚠️  Found {len(missing_libraries)} libraries not in signature database:")
            for library in missing_libraries:
                print(f"  📦 {library}")
            
            if auto_add_missing:
                print(f"\n🔧 Auto-adding {len(missing_libraries)} libraries to database...")
                for library in missing_libraries:
                    self.add_library_to_database(library)
            else:
                print(f"\n⚠️  Missing libraries: {', '.join(missing_libraries)}")
                print("   Some version matching may be incomplete.")
        
        # Match function calls to versions
        requirements = self.version_matcher.match_codebase_requirements(function_calls)
        
        if requirements:
            print(f"✅ Found compatible versions for {len(requirements)} libraries")
        else:
            print("❌ No compatible versions found for any libraries")
        
        return requirements 