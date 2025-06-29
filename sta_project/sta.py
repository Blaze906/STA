# Main script for STA (System Task Automator)

import argparse

def main():
    parser = argparse.ArgumentParser(description="STA - System Task Automator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Text Analyzer subcommand
    text_analyzer_parser = subparsers.add_parser('text_analyzer', help='Analyze text files')
    text_analyzer_parser.add_argument('file_path', type=str, help='Path to the text file')

    # Cleaner subcommand
    cleaner_parser = subparsers.add_parser('clean', help='Smart clean-up utilities')
    cleaner_parser.add_argument('directories', nargs='*', default=['.'], help='Directories to scan (default: current directory)')
    cleaner_parser.add_argument('--dupes', action='store_true', help='Find and remove/merge duplicate files')
    cleaner_parser.add_argument('--tmp', action='store_true', help='Remove temporary files and folders')
    cleaner_parser.add_argument('--empty', action='store_true', help='Remove empty directories after cleaning')
    cleaner_parser.add_argument('--dry-run', action='store_true', help='Show what would be done without actually deleting files')

    args = parser.parse_args()

    if args.command == 'text_analyzer':
        from modules.text_analyzer import analyze_text
        analyze_text(args.file_path)
    elif args.command == 'clean':
        from modules.cleaner import run_cleaner
        run_cleaner(
            paths=args.directories,
            find_dupes=args.dupes,
            remove_tmp=args.tmp,
            remove_empty=args.empty,
            dry_run=args.dry_run
        )
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
