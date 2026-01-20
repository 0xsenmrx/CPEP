import platform
import os
import sys

def get_system_info():
    # Detect OS 
    os_type = platform.system().lower()
    arch = platform.machine()
    arch_type = 'x64' if '64' in arch else 'x86'
    
    return os_type, arch_type

def manual_override():
    print("\n[!] Entering Manual Configuration")
    
    # Select OS
    print("\nSelect Target OS:")
    print("\t1. Windows")
    print("\t2. Linux")
    os_choice = input("\nChoice [1-2]: ")
    os_type = "windows" if os_choice == "1" else "linux"
    
    # Select Arch
    print("\nSelect Target Architecture:")
    print("\t1. x64")
    print("\t2. x86")
    arch_choice = input("\nChoice [1-2]: ")
    arch_type = "x64" if arch_choice == "1" else "x86"
    
    return os_type, arch_type

def main():
    print("######################################################################")
    print("###                             CPEP                               ###")
    print("### Cross-Platform Enumeration, Privilege Escalation & Persistence ###")
    print("######################################################################")
    
    print("\n----------------------------------------------------------------------")


    os_type, arch_type = get_system_info()
    print(f"\n[*] Detected System: {os_type.upper()} ({arch_type})")
    
    # Ask for confirmation
    confirm = input("[?] Is this correct? (Y/n): ").lower()
    
    if confirm == 'n':
        os_type, arch_type = manual_override()
        print(f"\n[+] Switched to: {os_type.upper()} ({arch_type})")
    else:
        print(f"\n[+] System Chosen : {os_type.upper()} ({arch_type})")
    
    print("\n----------------------------------------------------------------------")
    # Next: Plugin loading logic goes here...

if __name__ == "__main__":
    main()
