import requests
import json
from packaging import version
from typing import List, Dict, Optional
import time


class PyPIClient:
    """Client for fetching library information from PyPI"""
    
    def __init__(self):
        self.base_url = "https://pypi.org/pypi"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RequirementsCreator/1.0'
        })
    
    def get_all_versions(self, library_name: str) -> List[str]:
        """Fetch all available versions from PyPI"""
        url = f"{self.base_url}/{library_name}/json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            releases = response.json()["releases"]
            return list(releases.keys())
            
        except requests.RequestException as e:
            print(f"❌ Failed to fetch versions for {library_name}: {e}")
            return []
        except KeyError as e:
            print(f"❌ Invalid response format for {library_name}: {e}")
            return []
    
    def filter_stable_versions(self, versions: List[str], max_versions: int = 20) -> List[str]:
        """Filter to stable versions only and return latest N versions"""
        stable_versions = []
        
        for ver in versions:
            try:
                parsed_version = version.parse(ver)
                # Exclude pre-releases, post-releases, dev versions
                if not (parsed_version.is_prerelease or 
                       parsed_version.is_postrelease or 
                       parsed_version.is_devrelease):
                    stable_versions.append(ver)
            except Exception:
                continue
        
        # Sort and return latest versions
        sorted_versions = sorted(stable_versions, key=version.parse)
        return sorted_versions[-max_versions:] if len(sorted_versions) > max_versions else sorted_versions
    
    def get_latest_versions(self, library_name: str, count: int = 20) -> List[str]:
        """Get latest N stable versions of a library"""
        all_versions = self.get_all_versions(library_name)
        if not all_versions:
            return []
        
        return self.filter_stable_versions(all_versions, count)
    
    def get_package_info(self, library_name: str, version: str) -> Optional[Dict]:
        """Get detailed package information for a specific version"""
        url = f"{self.base_url}/{library_name}/{version}/json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None 