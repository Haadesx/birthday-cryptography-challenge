from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
import os
import base64
import hashlib
import secrets
import io
import cv2
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure upload folder - handle both Vercel and local environments
if os.environ.get('VERCEL'):
    # Use /tmp for Vercel
    app.config['UPLOAD_FOLDER'] = '/tmp'
else:
    # Use local uploads directory
    app.config['UPLOAD_FOLDER'] = 'uploads'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads directory if it doesn't exist and we're not on Vercel
if not os.environ.get('VERCEL'):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Cryptography functions
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
    """
    Apply Caesar cipher to the given text
    
    Args:
        text (str): The text to encrypt/decrypt
        shift (int): The number of positions to shift each letter
        decrypt (bool): If True, decrypt instead of encrypt
        
    Returns:
        str: The encrypted/decrypted text
    """
    result = ""
    if decrypt:
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Handle case preservation
            ascii_offset = ord('a') if char.islower() else ord('A')
            # Apply shift and wrap around using modulo
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            # Preserve non-alphabetic characters
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
            shift = ord(key_char) - ord('a')
            
            if decrypt:
                shift = -shift
                
            # Apply shift
            if char.islower():
                result += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            
            key_index += 1
        else:
            result += char
    
    return result

# Steganography functions
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

def encode_image(image_path, secret_data, password):
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
        return False, "Error: Image could not be read."
    
    # Calculate maximum bytes that can be encoded
    max_bytes = image.shape[0] * image.shape[1] * 3 // 8
    
    # Check if the data size is too large
    total_data_len = len(binary_data) + len(binary_salt) + 64  # 64 bits for header
    if total_data_len > max_bytes * 8:
        return False, "Error: Data too large to encode in this image."
    
    # Add a magic header to identify this as a steganographic image (32 bits)
    magic_header = "STEG"
    magic_header_binary = to_binary(magic_header)
    
    # Prepare data: magic header (32 bits) + salt length (32 bits) + salt + encrypted data
    salt_len = len(binary_salt)
    salt_len_binary = format(salt_len, '032b')
    
    # Add redundancy by duplicating the header and key info
    redundant_header = magic_header_binary + salt_len_binary
    data_to_hide = redundant_header + redundant_header + binary_salt + binary_data
    
    data_index = 0
    data_length = len(data_to_hide)
    
    # Flatten the image
    height, width, _ = image.shape
    
    # Use a deterministic pattern to spread data across all channels
    # This makes it more resilient to image processing and compression
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):  # Use all RGB channels
                if data_index < data_length:
                    # Convert pixel value to binary
                    pixel_binary = to_binary(image[row, col, color_channel])
                    
                    # Replace the least significant bit
                    new_pixel = pixel_binary[:-1] + data_to_hide[data_index]
                    
                    # Update the pixel with the new value
                    image[row, col, color_channel] = int(new_pixel, 2)
                    data_index += 1
                else:
                    break
    
    # Save the image to memory with high quality to prevent loss
    img_params = [int(cv2.IMWRITE_PNG_COMPRESSION), 0]  # Use lossless compression
    is_success, buffer = cv2.imencode(".png", image, img_params)
    if not is_success:
        return False, "Error: Failed to encode image."
    
    return True, buffer

def decode_image(image_path, password):
    """Decode hidden data from an image"""
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image exists
    if image is None:
        return False, "Error: Image could not be read."
    
    binary_data = ""
    
    # Flatten the image and extract data from all channels
    height, width, _ = image.shape
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):  # Extract from all channels
                # Convert pixel value to binary
                pixel_binary = to_binary(image[row, col, color_channel])
                
                # Extract the least significant bit
                binary_data += pixel_binary[-1]
                
                # Check if we've collected enough for the redundant headers (64 bits)
                if len(binary_data) == 64:
                    # Check for magic header "STEG" in either first or second position
                    first_header = binary_data[:32]
                    second_header = binary_data[32:64]
                    
                    first_magic = ""
                    second_magic = ""
                    
                    for i in range(0, 32, 8):
                        if i + 8 <= 32:
                            first_byte = first_header[i:i+8]
                            second_byte = second_header[i:i+8]
                            first_magic += chr(int(first_byte, 2))
                            second_magic += chr(int(second_byte, 2))
                    
                    # If neither header matches, continue collecting data
                    if first_magic != "STEG" and second_magic != "STEG":
                        continue
    
    # Try to find the header in multiple positions due to redundancy
    if len(binary_data) < 128:  # Need enough data for redundant headers + some salt
        return False, "Error: No hidden data found in image."
    
    # Check first potential header
    magic_header_binary = binary_data[:32]
    magic_header = ""
    for i in range(0, len(magic_header_binary), 8):
        if i + 8 <= len(magic_header_binary):
            byte = magic_header_binary[i:i+8]
            magic_header += chr(int(byte, 2))
    
    # Check second potential header
    second_header_binary = binary_data[32:64]
    second_header = ""
    for i in range(0, len(second_header_binary), 8):
        if i + 8 <= len(second_header_binary):
            byte = second_header_binary[i:i+8]
            second_header += chr(int(byte, 2))
    
    # Decide which header to use (if any)
    if magic_header == "STEG":
        # First header is valid
        salt_len_binary = binary_data[32:64]
        salt_len = int(salt_len_binary, 2)
        start_of_data = 64
    elif second_header == "STEG":
        # Second header is valid
        salt_len_binary = binary_data[64:96]
        salt_len = int(salt_len_binary, 2)
        start_of_data = 96
    else:
        # Try legacy format for backward compatibility
        try:
            salt_len_binary = binary_data[:32]
            salt_len = int(salt_len_binary, 2)
            start_of_data = 32
        except ValueError:
            return False, "Error: Could not decode the image. It may be corrupted or not contain hidden data."
    
    # Extract the salt
    salt_binary = binary_data[start_of_data:start_of_data+salt_len]
    
    # Convert salt bits to bytes
    salt_bytes = b''
    for i in range(0, len(salt_binary), 8):
        if i + 8 <= len(salt_binary):
            byte = salt_binary[i:i+8]
            salt_bytes += bytes([int(byte, 2)])
    
    # Extract the encrypted data
    encrypted_binary = binary_data[start_of_data+salt_len:]
    
    encrypted_bytes = b''
    for i in range(0, len(encrypted_binary), 8):
        if i + 8 <= len(encrypted_binary):
            byte = encrypted_binary[i:i+8]
            encrypted_bytes += bytes([int(byte, 2)])
    
    try:
        # Decrypt the data
        decrypted_data = decrypt_message(encrypted_bytes, password, salt_bytes)
        return True, decrypted_data
    except Exception as e:
        return False, f"Error decrypting data: {e}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encryption')
def encryption():
    return render_template('encryption.html')

@app.route('/steganography')
def steganography():
    return render_template('steganography.html')

@app.route('/birthday-challenge')
def birthday_challenge():
    return render_template('all_challenges.html')

# Routes for individual challenge pages
@app.route('/challenge1')
def challenge1():
    return redirect(url_for('birthday_challenge'))

@app.route('/challenge2')
def challenge2():
    return redirect(url_for('birthday_challenge'))

@app.route('/challenge3')
def challenge3():
    return redirect(url_for('birthday_challenge'))

# API endpoints
@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.json
    message = data.get('message', '')
    password = data.get('password', '')
    
    if not message or not password:
        return jsonify({'success': False, 'error': 'Missing message or password'})
        
    try:
        encrypted_message, salt = encrypt_message(message, password)
        return jsonify({
            'success': True,
            'encrypted_message': encrypted_message.decode(),
            'salt': base64.urlsafe_b64encode(salt).decode()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.json
    encrypted_message = data.get('encrypted_message', '')
    password = data.get('password', '')
    salt_b64 = data.get('salt', '')
    
    if not encrypted_message or not password or not salt_b64:
        return jsonify({'success': False, 'error': 'Missing parameters'})
        
    try:
        encrypted_message = encrypted_message.encode()
        salt = base64.urlsafe_b64decode(salt_b64)
        decrypted_message = decrypt_message(encrypted_message, password, salt)
        return jsonify({
            'success': True,
            'decrypted_message': decrypted_message
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/caesar-cipher', methods=['POST'])
def api_caesar_cipher():
    data = request.json
    text = data.get('text', '')
    shift = data.get('shift', 0)
    operation = data.get('operation', 'encrypt')
    
    if not text:
        return jsonify({'success': False, 'error': 'Missing text'})
        
    try:
        shift = int(shift)
        if shift < 0 or shift > 25:
            return jsonify({'success': False, 'error': 'Shift must be between 0 and 25'})
            
        result = caesar_cipher(text, shift, operation == 'decrypt')
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/vigenere-cipher', methods=['POST'])
def api_vigenere_cipher():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', '')
    operation = data.get('operation', 'encrypt')
    
    if not text or not key:
        return jsonify({'success': False, 'error': 'Missing text or key'})
        
    if not key.isalpha():
        return jsonify({'success': False, 'error': 'Key must contain only letters'})
        
    try:
        result = vigenere_cipher(text, key, operation == 'decrypt')
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/hash', methods=['POST'])
def api_hash():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'success': False, 'error': 'Missing message'})
        
    try:
        return jsonify({
            'success': True,
            'md5': hashlib.md5(message.encode()).hexdigest(),
            'sha1': hashlib.sha1(message.encode()).hexdigest(),
            'sha256': hashlib.sha256(message.encode()).hexdigest(),
            'sha512': hashlib.sha512(message.encode()).hexdigest()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/encode-image', methods=['POST'])
def api_encode_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'})
        
    file = request.files['image']
    message = request.form.get('message', '')
    password = request.form.get('password', '')
    
    if not file.filename:
        return jsonify({'success': False, 'error': 'No image selected'})
        
    if not message or not password:
        return jsonify({'success': False, 'error': 'Message and password are required'})
    
    # Force PNG format for steganography to ensure lossless compression
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.png', '.bmp', '.tiff']:
        return jsonify({
            'success': False, 
            'error': 'Please use PNG format for best results across devices. JPG/JPEG compression will corrupt hidden data.'
        })
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Check image dimensions
        img = cv2.imread(filepath)
        if img is not None:
            height, width, _ = img.shape
            if height < 200 or width < 200:
                return jsonify({
                    'success': False,
                    'error': f'Image is too small ({width}x{height}). Please use an image at least 500x500 pixels for better cross-device compatibility.'
                })
        
        success, result = encode_image(filepath, message, password)
        
        if success:
            # Clean up the original file
            os.remove(filepath)
            
            # Always use PNG extension for output file
            output_filename = f"secret_{secrets.token_hex(4)}_{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            # Save the file
            with open(output_path, 'wb') as f:
                f.write(result.tobytes())
            
            return jsonify({
                'success': True,
                'message': 'Message hidden successfully! For cross-device compatibility, make sure to download and share the original PNG file. Do not take screenshots or use platforms that compress images.',
                'filename': output_filename,
                'tips': [
                    'Share via email attachment',
                    'Use cloud storage links (Google Drive, Dropbox)',
                    'Send as document/file, not as photo in messaging apps',
                    'Avoid taking screenshots or sharing on social media'
                ]
            })
        else:
            # Clean up on failure
            os.remove(filepath)
            return jsonify({'success': False, 'error': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/decode-image', methods=['POST'])
def api_decode_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'})
        
    file = request.files['image']
    password = request.form.get('password', '')
    
    if not file.filename:
        return jsonify({'success': False, 'error': 'No image selected'})
        
    if not password:
        return jsonify({'success': False, 'error': 'Password is required'})
    
    # Check file format and warn if not ideal
    file_ext = os.path.splitext(file.filename)[1].lower()
    warning_message = ""
    if file_ext not in ['.png', '.bmp', '.tiff']:
        warning_message = "Warning: This image format may have lost the hidden data due to compression. PNG format is recommended for cross-device compatibility."
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        success, result = decode_image(filepath, password)
        
        # Clean up
        os.remove(filepath)
        
        if success:
            response_data = {
                'success': True,
                'message': result
            }
            if warning_message:
                response_data['warning'] = warning_message
            return jsonify(response_data)
        else:
            error_message = result
            if "Error decrypting data" in result:
                if file_ext not in ['.png', '.bmp', '.tiff']:
                    error_message += " This may be due to image compression. Please use the original PNG file."
                else:
                    error_message += " This could be because the image was modified, screenshot was taken, or it was shared via a platform that compressed it. Please try using the original image file."
            return jsonify({'success': False, 'error': error_message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e) + " - Please make sure you're using the original image file without any modifications."})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/api/challenge-verify', methods=['POST'])
def api_challenge_verify():
    data = request.json
    challenge = data.get('challenge', '')
    answer = data.get('answer', '')
    
    print(f"Received challenge: {challenge}, answer: '{answer}'")
    
    if challenge == 'caesar':
        # Clean up answer and expected answer for comparison
        correct_answer = "happy birthday to my favorite cybersecurity queen lisa"
        
        # Normalize user answer - remove punctuation and extra spaces
        user_answer = answer.lower().strip()
        user_answer = ''.join(c for c in user_answer if c.isalnum() or c.isspace())
        user_answer = ' '.join(user_answer.split())
        
        # Normalize correct answer
        correct_answer = ''.join(c for c in correct_answer if c.isalnum() or c.isspace())
        correct_answer = ' '.join(correct_answer.split())
        
        print(f"Caesar normalized comparison:\nUser:    '{user_answer}'\nCorrect: '{correct_answer}'")
        
        # Check if answer is correct or close enough (allow for small typos)
        is_correct = user_answer == correct_answer
        
        return jsonify({'success': True, 'correct': is_correct})
    
    elif challenge == 'vigenere':
        # Clean up answer and expected answer for comparison
        correct_answer = "i love you liz my incredible hacker girl"
        user_answer = answer.lower().strip()
        
        # Very permissive comparison for this challenge
        # Remove all non-alphanumeric characters and normalize spaces
        user_answer = ''.join(c for c in user_answer if c.isalnum() or c.isspace())
        user_answer = ' '.join(user_answer.split())
        
        # Check if the answer contains the key phrases
        key_phrases = ["i love you", "incredible", "hacker girl"]
        matches = sum(1 for phrase in key_phrases if phrase in user_answer)
        is_close_match = matches >= 2
        
        # Normalize correct answer
        correct_answer = ''.join(c for c in correct_answer if c.isalnum() or c.isspace())
        correct_answer = ' '.join(correct_answer.split())
        
        # Exact match or close enough
        is_exact_match = user_answer == correct_answer
        
        print(f"Vigenere normalized comparison:\nUser:    '{user_answer}'\nCorrect: '{correct_answer}'")
        print(f"Matches: {matches}, Close match: {is_close_match}, Exact match: {is_exact_match}")
        
        return jsonify({'success': True, 'correct': is_exact_match or is_close_match})
    
    else:
        return jsonify({'success': False, 'error': 'Invalid challenge'})

# Test route for challenge verification
@app.route('/api/test-ciphers')
def api_test_ciphers():
    # Test Caesar cipher with shift = 4
    caesar_plain = "happy birthday to my favorite cybersecurity queen lisa!"
    caesar_encrypted = caesar_cipher(caesar_plain, 4)
    caesar_decrypted = caesar_cipher(caesar_encrypted, 4, decrypt=True)
    
    # Test Vigenère cipher with key = "april"
    vigenere_plain = "i love you liz, my incredible hacker girl!"
    vigenere_encrypted = vigenere_cipher(vigenere_plain, "april")
    vigenere_decrypted = vigenere_cipher(vigenere_encrypted, "april", decrypt=True)
    
    return jsonify({
        'success': True,
        'caesar_plain': caesar_plain,
        'caesar_encrypted': caesar_encrypted,
        'caesar_decrypted': caesar_decrypted,
        'vigenere_plain': vigenere_plain,
        'vigenere_encrypted': vigenere_encrypted,
        'vigenere_decrypted': vigenere_decrypted
    })

if __name__ == '__main__':
    # Test correct Caesar cipher output for challenge
    caesar_plain = "happy birthday to my favorite cybersecurity queen lisa!"
    caesar_encoded = caesar_cipher(caesar_plain, 4)
    print(f"\nCaesar plain:  {caesar_plain}")
    print(f"Caesar cipher: {caesar_encoded}")
    
    # Test correct Vigenère cipher output for challenge
    vigenere_plain = "i love you liz, my incredible hacker girl!"
    vigenere_encoded = vigenere_cipher(vigenere_plain, "april")
    print(f"\nVigenère plain:  {vigenere_plain}")
    print(f"Vigenère cipher: {vigenere_encoded}")
    
    app.run(debug=True) 