#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def birthday_banner():
    clear_screen()
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Fore.CYAN}██████╗ ██╗██████╗ ████████╗██╗  ██╗██████╗  █████╗ ██╗   ██╗{Fore.MAGENTA}  ║
║  {Fore.CYAN}██╔══██╗██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝{Fore.MAGENTA}  ║
║  {Fore.CYAN}██████╔╝██║██████╔╝   ██║   ███████║██║  ██║███████║ ╚████╔╝{Fore.MAGENTA}   ║
║  {Fore.CYAN}██╔══██╗██║██╔══██╗   ██║   ██╔══██║██║  ██║██╔══██║  ╚██╔╝{Fore.MAGENTA}    ║
║  {Fore.CYAN}██████╔╝██║██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║{Fore.MAGENTA}     ║
║  {Fore.CYAN}╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝{Fore.MAGENTA}     ║
║                                                          ║
║  {Fore.YELLOW}███████╗██╗   ██╗██████╗ ██████╗ ██████╗ ██╗███████╗███████╗{Fore.MAGENTA}  ║
║  {Fore.YELLOW}██╔════╝██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██╔════╝{Fore.MAGENTA}  ║
║  {Fore.YELLOW}███████╗██║   ██║██████╔╝██████╔╝██████╔╝██║███████╗█████╗{Fore.MAGENTA}    ║
║  {Fore.YELLOW}╚════██║██║   ██║██╔══██╗██╔═══╝ ██╔══██╗██║╚════██║██╔══╝{Fore.MAGENTA}    ║
║  {Fore.YELLOW}███████║╚██████╔╝██║  ██║██║     ██║  ██║██║███████║███████╗{Fore.MAGENTA}  ║
║  {Fore.YELLOW}╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝{Fore.MAGENTA}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def run_script(script_path):
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}An error occurred while running the script.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}The script {script_path} was not found.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Script interrupted.{Style.RESET_ALL}")

def birthday_message():
    clear_screen()
    print(f"\n{Fore.MAGENTA}♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥{Style.RESET_ALL}")
    slow_print(f"{Fore.CYAN}Happy Birthday to my amazing girlfriend!{Style.RESET_ALL}", 0.05)
    slow_print(f"{Fore.YELLOW}I created this special cybersecurity-themed birthday surprise just for you.{Style.RESET_ALL}", 0.05)
    slow_print(f"{Fore.GREEN}Because I know how much you love cybersecurity and encryption.{Style.RESET_ALL}", 0.05)
    slow_print(f"{Fore.MAGENTA}I hope these little tools bring a smile to your face.{Style.RESET_ALL}", 0.05)
    slow_print(f"{Fore.CYAN}Enjoy exploring the world of cryptography and steganography!{Style.RESET_ALL}", 0.05)
    slow_print(f"{Fore.YELLOW}I love you!{Style.RESET_ALL}", 0.05)
    print(f"\n{Fore.MAGENTA}♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥{Style.RESET_ALL}")
    input(f"\n{Fore.WHITE}Press Enter to continue...{Style.RESET_ALL}")

def main():
    try:
        birthday_message()
        
        while True:
            birthday_banner()
            
            print(f"\n{Fore.CYAN}Welcome to the Cybersecurity Birthday Surprise!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Choose a tool to explore:{Style.RESET_ALL}\n")
            
            print(f"{Fore.GREEN}1. {Fore.WHITE}Encryption Challenge (Caesar, Vigenère, Fernet)")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Steganography Tool (Hide Messages in Images)")
            print(f"{Fore.GREEN}3. {Fore.WHITE}Customize Birthday Messages")
            print(f"{Fore.GREEN}4. {Fore.RED}Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}")
            
            if choice == '1':
                run_script("birthday_crypto.py")
            elif choice == '2':
                run_script("stego_birthday.py")
            elif choice == '3':
                run_script("customize_message.py")
            elif choice == '4':
                print(f"\n{Fore.MAGENTA}Thank you for exploring the Birthday Cybersecurity Surprise! Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                input(f"{Fore.RED}Invalid choice. Press Enter to try again...{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program interrupted. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main() 