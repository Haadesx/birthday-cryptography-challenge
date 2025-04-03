import os
import sys
import time
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def generate_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_message(message, password):
    key, salt = generate_key(password)
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message, salt

def decrypt_message(encrypted_message, password, salt):
    key, _ = generate_key(password, salt)
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

def caesar_cipher(text, shift, decrypt=False):
    result = ""
    if decrypt:
        shift = -shift
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def vigenere_cipher(text, key, decrypt=False):
    result = ""
    key = key.lower()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Calculate shift based on key character
            key_char = key[key_index % len(key)]
            key_index += 1
            shift = ord(key_char) - ord('a')
            
            if decrypt:
                shift = -shift
                
            # Apply shift
            if char.islower():
                result += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            result += char
    return result

def birthday_banner():
    clear_screen()
    banner = f"""
{Fore.MAGENTA}╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  {Fore.CYAN}██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗   ██╗{Fore.MAGENTA}                     ║
║  {Fore.CYAN}██║  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝{Fore.MAGENTA}                     ║
║  {Fore.CYAN}███████║███████║██████╔╝██████╔╝ ╚████╔╝{Fore.MAGENTA}                      ║
║  {Fore.CYAN}██╔══██║██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝{Fore.MAGENTA}                       ║
║  {Fore.CYAN}██║  ██║██║  ██║██║     ██║        ██║{Fore.MAGENTA}                        ║
║  {Fore.CYAN}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝{Fore.MAGENTA}                        ║
║                                                                ║
║  {Fore.YELLOW}██████╗ ██╗██████╗ ████████╗██╗  ██╗██████╗  █████╗ ██╗   ██╗{Fore.MAGENTA} ║
║  {Fore.YELLOW}██╔══██╗██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝{Fore.MAGENTA} ║
║  {Fore.YELLOW}██████╔╝██║██████╔╝   ██║   ███████║██║  ██║███████║ ╚████╔╝{Fore.MAGENTA}  ║
║  {Fore.YELLOW}██╔══██╗██║██╔══██╗   ██║   ██╔══██║██║  ██║██╔══██║  ╚██╔╝{Fore.MAGENTA}   ║
║  {Fore.YELLOW}██████╔╝██║██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║{Fore.MAGENTA}    ║
║  {Fore.YELLOW}╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝{Fore.MAGENTA}    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def main_menu():
    while True:
        birthday_banner()
        
        slow_print(f"\n{Fore.CYAN}Welcome to the Cybersecurity Birthday Challenge!{Style.RESET_ALL}")
        slow_print(f"{Fore.YELLOW}Choose your encryption adventure:{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}1. {Fore.WHITE}Encrypt a secret birthday message")
        print(f"{Fore.GREEN}2. {Fore.WHITE}Decrypt a message")
        print(f"{Fore.GREEN}3. {Fore.WHITE}Caesar Cipher")
        print(f"{Fore.GREEN}4. {Fore.WHITE}Vigenère Cipher")
        print(f"{Fore.GREEN}5. {Fore.WHITE}Hash a message")
        print(f"{Fore.GREEN}6. {Fore.WHITE}Birthday Challenge")
        print(f"{Fore.GREEN}7. {Fore.RED}Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Enter your choice (1-7): {Style.RESET_ALL}")
        
        if choice == '1':
            encrypt_message_menu()
        elif choice == '2':
            decrypt_message_menu()
        elif choice == '3':
            caesar_cipher_menu()
        elif choice == '4':
            vigenere_cipher_menu()
        elif choice == '5':
            hash_message_menu()
        elif choice == '6':
            birthday_challenge()
        elif choice == '7':
            print(f"\n{Fore.MAGENTA}Thanks for celebrating with cryptography! Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            input(f"{Fore.RED}Invalid choice. Press Enter to try again...{Style.RESET_ALL}")

def encrypt_message_menu():
    clear_screen()
    print(f"{Fore.GREEN}=== Encrypt a Secret Birthday Message ==={Style.RESET_ALL}\n")
    
    message = input(f"{Fore.YELLOW}Enter your message: {Style.RESET_ALL}")
    password = input(f"{Fore.YELLOW}Enter a password (needed for decryption): {Style.RESET_ALL}")
    
    encrypted_message, salt = encrypt_message(message, password)
    
    print(f"\n{Fore.GREEN}Encrypted message:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{encrypted_message.decode()}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Salt (needed for decryption):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{base64.urlsafe_b64encode(salt).decode()}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Keep the encrypted message and salt safe!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}You'll need both, along with the password, to decrypt the message.{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

def decrypt_message_menu():
    clear_screen()
    print(f"{Fore.GREEN}=== Decrypt a Message ==={Style.RESET_ALL}\n")
    
    try:
        encrypted_message = input(f"{Fore.YELLOW}Enter the encrypted message: {Style.RESET_ALL}")
        encrypted_message = encrypted_message.encode()
        
        salt_b64 = input(f"{Fore.YELLOW}Enter the salt: {Style.RESET_ALL}")
        salt = base64.urlsafe_b64decode(salt_b64)
        
        password = input(f"{Fore.YELLOW}Enter the password: {Style.RESET_ALL}")
        
        decrypted_message = decrypt_message(encrypted_message, password, salt)
        
        print(f"\n{Fore.GREEN}Decrypted message:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{decrypted_message}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error decrypting message: {e}{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

def caesar_cipher_menu():
    clear_screen()
    print(f"{Fore.GREEN}=== Caesar Cipher ==={Style.RESET_ALL}\n")
    
    operation = input(f"{Fore.YELLOW}Do you want to encrypt or decrypt? (e/d): {Style.RESET_ALL}").lower()
    text = input(f"{Fore.YELLOW}Enter the text: {Style.RESET_ALL}")
    
    try:
        shift = int(input(f"{Fore.YELLOW}Enter the shift value (1-25): {Style.RESET_ALL}"))
        if shift < 1 or shift > 25:
            print(f"{Fore.RED}Shift value must be between 1 and 25.{Style.RESET_ALL}")
            input("\nPress Enter to return to the main menu...")
            return
    except ValueError:
        print(f"{Fore.RED}Invalid shift value. Must be a number.{Style.RESET_ALL}")
        input("\nPress Enter to return to the main menu...")
        return
    
    decrypt = operation == 'd'
    result = caesar_cipher(text, shift, decrypt)
    
    print(f"\n{Fore.GREEN}{'Decrypted' if decrypt else 'Encrypted'} text:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

def vigenere_cipher_menu():
    clear_screen()
    print(f"{Fore.GREEN}=== Vigenère Cipher ==={Style.RESET_ALL}\n")
    
    operation = input(f"{Fore.YELLOW}Do you want to encrypt or decrypt? (e/d): {Style.RESET_ALL}").lower()
    text = input(f"{Fore.YELLOW}Enter the text: {Style.RESET_ALL}")
    key = input(f"{Fore.YELLOW}Enter the key (letters only): {Style.RESET_ALL}")
    
    if not key.isalpha():
        print(f"{Fore.RED}Key must contain only letters.{Style.RESET_ALL}")
        input("\nPress Enter to return to the main menu...")
        return
    
    decrypt = operation == 'd'
    result = vigenere_cipher(text, key, decrypt)
    
    print(f"\n{Fore.GREEN}{'Decrypted' if decrypt else 'Encrypted'} text:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

def hash_message_menu():
    clear_screen()
    print(f"{Fore.GREEN}=== Hash a Message ==={Style.RESET_ALL}\n")
    
    message = input(f"{Fore.YELLOW}Enter the message to hash: {Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}Hash algorithms:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MD5:      {hashlib.md5(message.encode()).hexdigest()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SHA-1:    {hashlib.sha1(message.encode()).hexdigest()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SHA-256:  {hashlib.sha256(message.encode()).hexdigest()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SHA-512:  {hashlib.sha512(message.encode()).hexdigest()}{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

def birthday_challenge():
    clear_screen()
    print(f"{Fore.MAGENTA}=== Birthday Cybersecurity Challenge ==={Style.RESET_ALL}\n")
    
    slow_print(f"{Fore.YELLOW}Welcome to your special birthday crypto challenge!{Style.RESET_ALL}")
    slow_print(f"{Fore.YELLOW}Can you solve these puzzles to unlock a special birthday message?{Style.RESET_ALL}\n")
    
    # Challenge 1: Caesar Cipher
    print(f"{Fore.GREEN}Challenge 1: Decrypt this Caesar cipher{Style.RESET_ALL}")
    cipher1 = "Ohccm Ipyaokhf av tf mhcvypai jfilyzijaypaf zaplujiy!"
    print(f"{Fore.CYAN}{cipher1}{Style.RESET_ALL}")
    
    answer1 = input(f"{Fore.YELLOW}Your decryption (shift is your birth date): {Style.RESET_ALL}")
    if answer1.lower() == "happy birthday to my favorite cybersecurity scientist!":
        print(f"{Fore.GREEN}Correct! Moving to the next challenge...{Style.RESET_ALL}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}That's not quite right. The shift key is your birth date (e.g., if born on the 15th, shift is 15){Style.RESET_ALL}")
        input("\nPress Enter to return to the main menu...")
        return
    
    # Challenge 2: Vigenère Cipher
    clear_screen()
    print(f"{Fore.GREEN}Challenge 2: Decrypt this Vigenère cipher{Style.RESET_ALL}")
    cipher2 = "Mlv tfv bks fprx kzwprxrfx pcwkt!"
    print(f"{Fore.CYAN}{cipher2}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Hint: The key is the month of your birthday in lowercase.{Style.RESET_ALL}")
    
    answer2 = input(f"{Fore.YELLOW}Your decryption: {Style.RESET_ALL}")
    if answer2.lower() == "you are the most amazing hacker!":
        print(f"{Fore.GREEN}Excellent work! One final challenge...{Style.RESET_ALL}")
        time.sleep(2)
    else:
        print(f"{Fore.RED}That's not quite right. The key is the month of your birthday (e.g., 'january'){Style.RESET_ALL}")
        input("\nPress Enter to return to the main menu...")
        return
    
    # Final challenge: Base64 encoded message
    clear_screen()
    print(f"{Fore.GREEN}Final Challenge: Decode this Base64 message{Style.RESET_ALL}")
    final_message = "SSBsb3ZlIHlvdSBzbyBtdWNoISBZb3UgYXJlIHRoZSBtb3N0IGJyaWxsaWFudCwgYmVhdXRpZnVsLCBhbmQgYW1hemluZyBwZXJzb24gSSBrbm93LiBIYXBweSBCaXJ0aGRheSEgPDM="
    print(f"{Fore.CYAN}{final_message}{Style.RESET_ALL}")
    
    decoded = base64.b64decode(final_message).decode()
    answer = input(f"{Fore.YELLOW}Enter 'DECODE' to reveal the secret message: {Style.RESET_ALL}")
    
    if answer.upper() == "DECODE":
        print(f"\n{Fore.MAGENTA}Message decoded:{Style.RESET_ALL}")
        slow_print(f"{Fore.CYAN}{decoded}{Style.RESET_ALL}", 0.05)
        print(f"\n{Fore.MAGENTA}🎉 Congratulations! You've completed all the challenges! 🎉{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}That's not the right command. Try again!{Style.RESET_ALL}")
    
    input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program interrupted. Goodbye!{Style.RESET_ALL}")
        sys.exit(0) 