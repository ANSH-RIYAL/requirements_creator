#!/usr/bin/env python3
"""
Example usage of RequirementsCreator
Demonstrates how to use the library programmatically
"""

from src.requirements_creator import RequirementsCreator


def example_add_library():
    """Example: Add a library to the database"""
    print("=== Example: Adding a library to database ===")
    
    creator = RequirementsCreator()
    
    # Add pandas to the database (fully automated)
    signatures = creator.add_library_to_database("pandas")
    
    if signatures:
        print(f"✅ Successfully added pandas with {len(signatures)} versions")
        print(f"📊 Versions: {list(signatures.keys())}")
    else:
        print("❌ Failed to add pandas")


def example_analyze_codebase():
    """Example: Analyze a codebase and generate requirements.txt"""
    print("\n=== Example: Analyzing a codebase ===")
    
    creator = RequirementsCreator()
    
    # Create a simple test file
    test_code = '''
import pandas as pd
import numpy as np
import requests

# Use pandas
df = pd.read_csv('data.csv', sep=',', header=0)
df.head()

# Use numpy
arr = np.array([1, 2, 3, 4, 5])
mean = np.mean(arr)

# Use requests
response = requests.get('https://api.example.com', timeout=30)
data = response.json()
'''
    
    # Write test file
    with open('test_code.py', 'w') as f:
        f.write(test_code)
    
    try:
        # Analyze the codebase
        requirements = creator.analyze_codebase('.')
        
        if requirements:
            print("📋 Generated requirements:")
            for library, version in requirements.items():
                print(f"  {library}{version}")
        else:
            print("❌ No requirements generated")
    
    finally:
        # Clean up
        import os
        if os.path.exists('test_code.py'):
            os.remove('test_code.py')


def example_batch_add():
    """Example: Add multiple libraries at once"""
    print("\n=== Example: Batch adding libraries ===")
    
    creator = RequirementsCreator()
    
    # Add multiple popular libraries
    libraries = ["pandas", "numpy", "matplotlib", "requests"]
    results = creator.batch_add_libraries(libraries)
    
    print("📊 Results:")
    for library, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {library}")


def example_database_management():
    """Example: Database management operations"""
    print("\n=== Example: Database management ===")
    
    creator = RequirementsCreator()
    
    # List all analyzed libraries
    libraries = creator.list_analyzed_libraries()
    print(f"📚 Libraries in database: {libraries}")
    
    # Get database statistics
    stats = creator.get_database_stats()
    print(f"📊 Database stats: {stats['total_libraries']} libraries, {stats['total_versions']} versions")


def example_quick_analyze():
    """Example: Quick analysis with pre-specified libraries"""
    print("\n=== Example: Quick analysis ===")
    
    creator = RequirementsCreator()
    
    # Create test code
    test_code = '''
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
arr = np.array([1, 2, 3])
'''
    
    with open('quick_test.py', 'w') as f:
        f.write(test_code)
    
    try:
        # Quick analysis with specific libraries
        requirements = creator.quick_analyze('.', libraries=["pandas", "numpy"])
        
        if requirements:
            print("📋 Quick analysis results:")
            for library, version in requirements.items():
                print(f"  {library}{version}")
    
    finally:
        import os
        if os.path.exists('quick_test.py'):
            os.remove('quick_test.py')


if __name__ == '__main__':
    print("🚀 RequirementsCreator Examples")
    print("=" * 50)
    
    # Run examples
    example_add_library()
    example_analyze_codebase()
    example_batch_add()
    example_database_management()
    example_quick_analyze()
    
    print("\n✅ All examples completed!") 