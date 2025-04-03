#!/usr/bin/env python3
import os
import sys
import cv2
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def to_binary(data):
    """Convert data to binary format"""
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, '08b') for i in data])
    elif isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, '08b')
    else:
        raise TypeError("Type not supported.")

def encode_image(image_path, secret_data, password, output_path=None):
    """Encode secret data into an image"""
    # Encrypt the secret data first
    encrypted_data, salt = encrypt_message(secret_data, password)
    
    # Convert encrypted data to binary
    binary_data = to_binary(encrypted_data)
    
    # Convert salt to binary
    binary_salt = to_binary(salt)
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image exists
    if image is None:
        print(f"{Fore.RED}Error: Image not found at {image_path}{Style.RESET_ALL}")
        return False
    
    # Calculate maximum bytes that can be encoded
    max_bytes = image.shape[0] * image.shape[1] * 3 // 8
    
    # Check if the data size is too large
    total_data_len = len(binary_data) + len(binary_salt) + 32  # 32 bits for salt length
    if total_data_len > max_bytes * 8:
        print(f"{Fore.RED}Error: Data too large to encode in this image.{Style.RESET_ALL}")
        return False
    
    # Prepare data: salt length (32 bits) + salt + encrypted data
    salt_len = len(binary_salt)
    salt_len_binary = format(salt_len, '032b')
    data_to_hide = salt_len_binary + binary_salt + binary_data
    
    data_index = 0
    
    # Flatten the image
    height, width, _ = image.shape
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):  # RGB channels
                if data_index < len(data_to_hide):
                    # Convert pixel value to binary
                    pixel_binary = to_binary(image[row, col, color_channel])
                    
                    # Replace the least significant bit
                    new_pixel = pixel_binary[:-1] + data_to_hide[data_index]
                    
                    # Update the pixel with the new value
                    image[row, col, color_channel] = int(new_pixel, 2)
                    data_index += 1
                else:
                    break
    
    # Set output path if not specified
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_secret{ext}"
    
    # Save the image
    cv2.imwrite(output_path, image)
    return output_path

def decode_image(image_path, password):
    """Decode hidden data from an image"""
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image exists
    if image is None:
        print(f"{Fore.RED}Error: Image not found at {image_path}{Style.RESET_ALL}")
        return None
    
    binary_data = ""
    
    # Flatten the image
    height, width, _ = image.shape
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):
                # Convert pixel value to binary
                pixel_binary = to_binary(image[row, col, color_channel])
                
                # Extract the least significant bit
                binary_data += pixel_binary[-1]
    
    # First 32 bits contain the salt length
    salt_len_binary = binary_data[:32]
    salt_len = int(salt_len_binary, 2)
    
    # Extract the salt
    salt_binary = binary_data[32:32+salt_len]
    salt_bytes = b''
    for i in range(0, len(salt_binary), 8):
        if i + 8 <= len(salt_binary):
            byte = salt_binary[i:i+8]
            salt_bytes += bytes([int(byte, 2)])
    
    # Extract the encrypted data
    encrypted_binary = binary_data[32+salt_len:]
    encrypted_bytes = b''
    for i in range(0, len(encrypted_binary), 8):
        if i + 8 <= len(encrypted_binary):
            byte = encrypted_binary[i:i+8]
            encrypted_bytes += bytes([int(byte, 2)])
    
    try:
        # Decrypt the data
        decrypted_data = decrypt_message(encrypted_bytes, password, salt_bytes)
        return decrypted_data
    except Exception as e:
        print(f"{Fore.RED}Error decrypting data: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This could be due to an incorrect password or the image doesn't contain hidden data.{Style.RESET_ALL}")
        return None

def print_banner():
    clear_screen()
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {Fore.CYAN}███████╗████████╗███████╗ ██████╗  ██████╗ {Fore.MAGENTA}                   ║
║  {Fore.CYAN}██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔═══██╗{Fore.MAGENTA}                   ║
║  {Fore.CYAN}███████╗   ██║   █████╗  ██║  ███╗██║   ██║{Fore.MAGENTA}                   ║
║  {Fore.CYAN}╚════██║   ██║   ██╔══╝  ██║   ██║██║   ██║{Fore.MAGENTA}                   ║
║  {Fore.CYAN}███████║   ██║   ███████╗╚██████╔╝╚██████╔╝{Fore.MAGENTA}                   ║
║  {Fore.CYAN}╚══════╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝ {Fore.MAGENTA}                   ║
║                                                              ║
║  {Fore.YELLOW}██████╗ ██╗██████╗ ████████╗██╗  ██╗██████╗  █████╗ ██╗   ██╗{Fore.MAGENTA} ║
║  {Fore.YELLOW}██╔══██╗██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝{Fore.MAGENTA} ║
║  {Fore.YELLOW}██████╔╝██║██████╔╝   ██║   ███████║██║  ██║███████║ ╚████╔╝{Fore.MAGENTA}  ║
║  {Fore.YELLOW}██╔══██╗██║██╔══██╗   ██║   ██╔══██║██║  ██║██╔══██║  ╚██╔╝{Fore.MAGENTA}   ║
║  {Fore.YELLOW}██████╔╝██║██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║{Fore.MAGENTA}    ║
║  {Fore.YELLOW}╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝{Fore.MAGENTA}    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def main():
    while True:
        print_banner()
        print(f"\n{Fore.CYAN}Welcome to the Birthday Steganography Tool!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Hide secret messages in images for your special someone.{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}1. {Fore.WHITE}Hide a message in an image")
        print(f"{Fore.GREEN}2. {Fore.WHITE}Reveal a hidden message from an image")
        print(f"{Fore.GREEN}3. {Fore.RED}Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): {Style.RESET_ALL}")
        
        if choice == '1':
            clear_screen()
            print(f"{Fore.GREEN}=== Hide a Message in an Image ==={Style.RESET_ALL}\n")
            
            image_path = input(f"{Fore.YELLOW}Enter the path to the image: {Style.RESET_ALL}")
            secret_data = input(f"{Fore.YELLOW}Enter your secret message: {Style.RESET_ALL}")
            password = input(f"{Fore.YELLOW}Enter a password to encrypt the message: {Style.RESET_ALL}")
            output_path = input(f"{Fore.YELLOW}Enter the output image path (or press Enter for default): {Style.RESET_ALL}")
            
            if not output_path:
                output_path = None
            
            result = encode_image(image_path, secret_data, password, output_path)
            if result:
                print(f"\n{Fore.GREEN}Success! Your message has been hidden in: {result}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Remember the password - it will be needed to reveal the message.{Style.RESET_ALL}")
            
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '2':
            clear_screen()
            print(f"{Fore.GREEN}=== Reveal a Hidden Message ==={Style.RESET_ALL}\n")
            
            image_path = input(f"{Fore.YELLOW}Enter the path to the image with hidden data: {Style.RESET_ALL}")
            password = input(f"{Fore.YELLOW}Enter the password: {Style.RESET_ALL}")
            
            result = decode_image(image_path, password)
            if result:
                print(f"\n{Fore.GREEN}Success! Hidden message:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
            
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '3':
            print(f"\n{Fore.MAGENTA}Thank you for using the Birthday Steganography Tool! Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
            
        else:
            input(f"{Fore.RED}Invalid choice. Press Enter to try again...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program interrupted. Goodbye!{Style.RESET_ALL}")
        sys.exit(0) 