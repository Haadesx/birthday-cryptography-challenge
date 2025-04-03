#!/usr/bin/env python3
import base64
import sys

def generate_base64_message():
    print("Enter your custom birthday message (Ctrl+D or Ctrl+Z when done):")
    message_lines = []
    
    try:
        while True:
            line = input()
            message_lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    
    message = "\n".join(message_lines)
    encoded = base64.b64encode(message.encode()).decode()
    
    print("\nYour Base64 encoded message:")
    print(encoded)
    print("\nReplace the 'final_message' variable in birthday_crypto.py with this string.")

def generate_caesar_cipher():
    message = input("Enter your message for Caesar cipher: ")
    try:
        shift = int(input("Enter shift value (usually the birthday date, e.g., 15): "))
        if shift < 1 or shift > 25:
            print("Shift should be between 1 and 25")
            return
    except ValueError:
        print("Shift must be a number")
        return
    
    # Encrypt with Caesar cipher
    result = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    
    print(f"\nYour Caesar cipher encrypted message (shift={shift}):")
    print(result)
    print("\nReplace the 'cipher1' variable in birthday_crypto.py with this string.")
    print(f"The recipient will need to use a shift of {shift} to decrypt it.")

def generate_vigenere_cipher():
    message = input("Enter your message for Vigenère cipher: ")
    key = input("Enter key (usually month of birthday, e.g., 'august'): ").lower()
    
    if not key.isalpha():
        print("Key must contain only letters")
        return
    
    # Encrypt with Vigenère cipher
    result = ""
    key_index = 0
    
    for char in message:
        if char.isalpha():
            # Calculate shift based on key character
            key_char = key[key_index % len(key)]
            key_index += 1
            shift = ord(key_char) - ord('a')
            
            # Apply shift
            if char.islower():
                result += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            result += char
    
    print(f"\nYour Vigenère cipher encrypted message (key='{key}'):")
    print(result)
    print("\nReplace the 'cipher2' variable in birthday_crypto.py with this string.")
    print(f"The recipient will need to use '{key}' as the key to decrypt it.")

def main():
    print("Birthday Crypto Customization Tool")
    print("=================================")
    print("1. Generate Base64 encoded message")
    print("2. Generate Caesar cipher message")
    print("3. Generate Vigenère cipher message")
    
    try:
        choice = int(input("\nSelect an option (1-3): "))
        if choice == 1:
            generate_base64_message()
        elif choice == 2:
            generate_caesar_cipher()
        elif choice == 3:
            generate_vigenere_cipher()
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")

if __name__ == "__main__":
    main() 