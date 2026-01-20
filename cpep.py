#!/usr/bin/env python3
"""
CPEP: Cross-Platform Enumeration, PrivEsc & Persistence
Phase One: Finalized Engine
---------------------------------------------------------
Author: 0xsenmrx (senmrx)
Description: A dynamic, post-explitation plugin execution engine.
"""

import platform
import os
import sys
import subprocess
import argparse
import shutil

# --- Terminal Color Palette ---
R = "\033[91m"  # Red (Error/Critical)
G = "\033[92m"  # Green (Success/Finding)
Y = "\033[93m"  # Yellow (Warning/Note)
B = "\033[94m"  # Blue (Framework UI)
C = "\033[96m"  # Cyan (Sub-Headers)
BOLD = "\033[1m"
END = "\033[0m"

def get_system_info():
    """Detects current host OS and architecture."""
    os_type = platform.system().lower()
    arch = platform.machine()
    arch_type = 'x64' if '64' in arch else 'x86'
    return os_type, arch_type

def execute_plugin(path):
    """Executes a single plugin with terminal-aware formatting."""
    width = shutil.get_terminal_size((80, 20)).columns
    if not path.lower().endswith('.py'):
        path += ".py"
    
    plugin_name = os.path.basename(path)
    if not os.path.exists(path):
        print(f"{R}[!] Error: Plugin not found at {path}{END}")
        return

    print(f"\n{'=' * width}")
    print(f"{BOLD}{C}[ EXE ]:{END} {plugin_name}")
    print(f"{'-' * width}")

    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=300)
        if result.stdout:
            stdout_content = result.stdout.strip()
            stdout_content = stdout_content.replace("[+]", f"{G}[+]{END}").replace("[!]", f"{Y}[!]{END}")
            print(stdout_content)
        
        if result.stderr:
            print(f"\n{R}[ SCRIPT ERROR ]:{END}\n{result.stderr.strip()}")
        print(f"{'=' * width}")
        
    except subprocess.TimeoutExpired:
        print(f"{R}[!] Timeout: {plugin_name} exceeded 300s limit.{END}")
    except Exception as e:
        print(f"{R}[!] Execution Failure for {plugin_name}: {str(e)}{END}")

def run_dir_recursive(target_path):
    """Recursively executes all .py files in a directory tree."""
    if not os.path.isdir(target_path):
        print(f"{Y}[-] Path skipped (not a directory): {target_path}{END}")
        return

    found_any = False
    for root, dirs, files in os.walk(target_path):
        for f in sorted(files):
            if f.endswith('.py'):
                found_any = True
                execute_plugin(os.path.join(root, f))
    if not found_any:
        print(f"{Y}[-] No plugins found in: {target_path}{END}")

def main():
    parser = argparse.ArgumentParser(description="CPEP: Cross-Platform Enumeration, PrivEsc & Persistence")
    parser.add_argument("-c", "--category", help="Category name(s), comma-separated")
    parser.add_argument("-ca", "--category-all", action="store_true", help="Run all categories")
    parser.add_argument("-sc", "--subcategory", help="Subcategory name(s), comma-separated")
    parser.add_argument("-sca", "--subcategory-all", action="store_true", help="Run all subcategories")
    parser.add_argument("-p", "--plugins", help="Plugin name(s), comma-separated")
    parser.add_argument("-pa", "--plugins-all", action="store_true", help="Run all plugins")
    parser.add_argument("-mo", "--manual-os", help="Override OS")
    parser.add_argument("-ma", "--manual-arch", help="Override Arch")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    width = shutil.get_terminal_size((80, 20)).columns

    try:
        # 1. Identity Setup
        os_detected, arch_detected = get_system_info()
        target_os = args.manual_os.lower() if args.manual_os else os_detected
        target_arch = args.manual_arch.lower() if args.manual_arch else arch_detected
        base_path = os.path.join("plugins", target_os, target_arch)

        # 2. Dynamic Banner
        banner_text = f"CPEP Initialized | Target: {target_os.upper()} {target_arch}"
        print(f"\n{'#' * width}")
        print(f"### {banner_text.center(width - 8)} ###")
        print(f"{'#' * width}\n")
        
        if not os.path.exists(base_path):
            print(f"{R}[!] Error: Target directory {base_path} not found.{END}")
            sys.exit(1)

        # 3. Strict Execution Logic
        # LEVEL 1: CATEGORY
        if args.category_all:
            run_dir_recursive(base_path)
            sys.exit(0)
        elif not args.category:
            print(f"{R}[!] Error: Category (-c) or Category-All (-ca) required.{END}")
            sys.exit(1)

        categories = [c.strip() for c in args.category.split(",")]
        if len(categories) > 1:
            print(f"{C}[*] Multiple categories: Escalating to recursive sweep.{END}")
            for cat in categories:
                run_dir_recursive(os.path.join(base_path, cat))
            sys.exit(0)

        # LEVEL 2: SUBCATEGORY
        cat_path = os.path.join(base_path, categories[0])
        if args.subcategory_all:
            run_dir_recursive(cat_path)
            sys.exit(0)
        elif not args.subcategory:
            print(f"{R}[!] Error: Subcategory (-sc) or Subcategory-All (-sca) required.{END}")
            sys.exit(1)

        subcategories = [s.strip() for s in args.subcategory.split(",")]
        if len(subcategories) > 1:
            print(f"{C}[*] Multiple subcategories: Escalating to recursive sweep.{END}")
            for sub in subcategories:
                run_dir_recursive(os.path.join(cat_path, sub))
            sys.exit(0)

        # LEVEL 3: PLUGINS
        sub_path = os.path.join(cat_path, subcategories[0])
        if args.plugins_all:
            run_dir_recursive(sub_path)
        elif not args.plugins:
            print(f"{R}[!] Error: Plugin (-p) or Plugins-All (-pa) required.{END}")
            sys.exit(1)
        else:
            plugin_list = [p.strip() for p in args.plugins.split(",")]
            for p in plugin_list:
                execute_plugin(os.path.join(sub_path, p))

        # 4. Finalization
        print(f"\n{'*' * width}")
        print(f"{BOLD}{G}[*] CPEP execution complete.{END}")
        print(f"{'*' * width}\n")

    except KeyboardInterrupt:
        print(f"\n{Y}[!] User interrupted. Exiting...{END}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
