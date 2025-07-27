#!/usr/bin/env python3
"""
Requirements Creator - CLI Interface
Automatically generate requirements.txt from code analysis
"""

import argparse
import sys
import os
from src.requirements_creator import RequirementsCreator


def main():
    parser = argparse.ArgumentParser(
        description="Automatically generate requirements.txt from code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a codebase and generate requirements.txt
  python main.py analyze /path/to/your/code

  # Add a library to the signature database
  python main.py add pandas

  # Add multiple libraries to the database
  python main.py batch-add pandas numpy matplotlib

  # List all analyzed libraries
  python main.py list

  # Get database statistics
  python main.py stats

  # Delete a library from database
  python main.py delete pandas
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze codebase and generate requirements.txt')
    analyze_parser.add_argument('code_path', help='Path to the codebase to analyze')
    analyze_parser.add_argument('-o', '--output', default='requirements.txt', help='Output file path (default: requirements.txt)')
    analyze_parser.add_argument('--auto-add', action='store_true', help='Automatically add missing libraries to database without asking')
    
    # Add library command
    add_parser = subparsers.add_parser('add', help='Add a library to the signature database')
    add_parser.add_argument('library', help='Library name to add')
    add_parser.add_argument('-v', '--versions', type=int, default=20, help='Number of versions to analyze (default: 20)')
    
    # Batch add command
    batch_parser = subparsers.add_parser('batch-add', help='Add multiple libraries to the database')
    batch_parser.add_argument('libraries', nargs='+', help='Library names to add')
    
    # List command
    subparsers.add_parser('list', help='List all analyzed libraries')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a library from the database')
    delete_parser.add_argument('library', help='Library name to delete')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a library in the database')
    update_parser.add_argument('library', help='Library name to update')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize RequirementsCreator
    creator = RequirementsCreator()
    
    try:
        if args.command == 'analyze':
            if not os.path.exists(args.code_path):
                print(f"❌ Code path does not exist: {args.code_path}")
                sys.exit(1)
            
            print(f"🔍 Analyzing codebase: {args.code_path}")
            requirements = creator.analyze_codebase(args.code_path, args.output, args.auto_add)
            
            if requirements:
                print(f"\n📋 Generated requirements:")
                for library, version in requirements.items():
                    print(f"  {library}{version}")
            else:
                print("❌ No requirements generated")
        
        elif args.command == 'add':
            print(f"📦 Adding library: {args.library}")
            signatures = creator.add_library_to_database(args.library, args.versions)
            
            if signatures:
                print(f"✅ Successfully added {args.library} with {len(signatures)} versions")
            else:
                print(f"❌ Failed to add {args.library}")
                sys.exit(1)
        
        elif args.command == 'batch-add':
            print(f"📦 Adding {len(args.libraries)} libraries...")
            results = creator.batch_add_libraries(args.libraries)
            
            print("\n📊 Results:")
            for library, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {library}")
        
        elif args.command == 'list':
            libraries = creator.list_analyzed_libraries()
            
            if libraries:
                print("📚 Analyzed libraries:")
                for library in libraries:
                    print(f"  📦 {library}")
            else:
                print("📚 No libraries in database")
        
        elif args.command == 'stats':
            stats = creator.get_database_stats()
            
            print("📊 Database Statistics:")
            print(f"  📚 Total libraries: {stats['total_libraries']}")
            print(f"  🔢 Total versions: {stats['total_versions']}")
            print(f"  ⚙️  Total functions: {stats['total_functions']}")
            
            if stats['libraries']:
                print(f"\n📦 Libraries: {', '.join(stats['libraries'])}")
        
        elif args.command == 'delete':
            print(f"🗑️  Deleting library: {args.library}")
            success = creator.delete_library(args.library)
            
            if success:
                print(f"✅ Successfully deleted {args.library}")
            else:
                print(f"❌ Failed to delete {args.library}")
                sys.exit(1)
        
        elif args.command == 'update':
            print(f"🔄 Updating library: {args.library}")
            signatures = creator.update_library(args.library)
            
            if signatures:
                print(f"✅ Successfully updated {args.library}")
            else:
                print(f"❌ Failed to update {args.library}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 