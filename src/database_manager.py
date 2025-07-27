import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class SignatureDBManager:
    """Manage signature database storage and retrieval"""
    
    def __init__(self, db_path: str = "signature_database"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
    
    def save_library_signatures(self, library_name: str, signatures: Dict[str, Any]) -> str:
        """Save library signatures to JSON file"""
        file_path = os.path.join(self.db_path, f"{library_name}_signatures.json")
        
        # Create comprehensive signature data
        signature_data = {
            "library_name": library_name,
            "analysis_date": datetime.now().isoformat(),
            "total_versions": len(signatures),
            "versions": signatures
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(signature_data, f, indent=2, default=str)
            
            print(f"💾 Saved signatures to {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to save signatures for {library_name}: {e}")
            return None
    
    def load_library_signatures(self, library_name: str) -> Optional[Dict[str, Any]]:
        """Load library signatures from file"""
        file_path = os.path.join(self.db_path, f"{library_name}_signatures.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(f"❌ Failed to load signatures for {library_name}: {e}")
                return None
        else:
            return None
    
    def library_exists(self, library_name: str) -> bool:
        """Check if library signatures exist in database"""
        file_path = os.path.join(self.db_path, f"{library_name}_signatures.json")
        return os.path.exists(file_path)
    
    def list_analyzed_libraries(self) -> list:
        """List all libraries that have been analyzed"""
        libraries = []
        
        if not os.path.exists(self.db_path):
            return libraries
        
        for filename in os.listdir(self.db_path):
            if filename.endswith('_signatures.json'):
                library_name = filename.replace('_signatures.json', '')
                libraries.append(library_name)
        
        return sorted(libraries)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the signature database"""
        libraries = self.list_analyzed_libraries()
        
        total_versions = 0
        total_functions = 0
        
        for library in libraries:
            data = self.load_library_signatures(library)
            if data:
                total_versions += data.get("total_versions", 0)
                versions = data.get("versions", {})
                for version_sigs in versions.values():
                    total_functions += len(version_sigs)
        
        return {
            "total_libraries": len(libraries),
            "total_versions": total_versions,
            "total_functions": total_functions,
            "libraries": libraries
        }
    
    def delete_library_signatures(self, library_name: str) -> bool:
        """Delete library signatures from database"""
        file_path = os.path.join(self.db_path, f"{library_name}_signatures.json")
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️  Deleted signatures for {library_name}")
                return True
            except Exception as e:
                print(f"❌ Failed to delete signatures for {library_name}: {e}")
                return False
        else:
            print(f"⚠️  No signatures found for {library_name}")
            return False
    
    def update_library_signatures(self, library_name: str, signatures: Dict[str, Any]) -> str:
        """Update existing library signatures"""
        existing_data = self.load_library_signatures(library_name)
        
        if existing_data:
            # Merge with existing data
            existing_versions = existing_data.get("versions", {})
            existing_versions.update(signatures)
            
            # Update metadata
            existing_data["analysis_date"] = datetime.now().isoformat()
            existing_data["total_versions"] = len(existing_versions)
            existing_data["versions"] = existing_versions
            
            return self.save_library_signatures(library_name, existing_data["versions"])
        else:
            # Create new entry
            return self.save_library_signatures(library_name, signatures) 