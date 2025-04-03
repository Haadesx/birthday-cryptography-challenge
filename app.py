from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import base64
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Create uploads directory if needed
os.makedirs('uploads', exist_ok=True)

# Caesar cipher function
def caesar_cipher(text, shift, decrypt=False):
    """Apply Caesar cipher to the given text"""
    result = ""
    if decrypt:
        shift = -shift
    
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    
    return result

# Vigenère cipher function
def vigenere_cipher(text, key, decrypt=False):
    """Apply Vigenère cipher to the given text"""
    result = ""
    key = key.lower()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('a')
            
            if decrypt:
                shift = -shift
                
            if char.islower():
                result += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            
            key_index += 1
        else:
            result += char
    
    return result

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/birthday-challenge')
def birthday_challenge():
    # Encrypt the messages for the challenges
    plaintext1 = "happy birthday to my favorite cybersecurity queen lisa!"
    ciphertext1 = caesar_cipher(plaintext1, 5)
    
    plaintext2 = "i love you liz, my incredible hacker girl!"
    key = "pagal"
    ciphertext2 = vigenere_cipher(plaintext2, key)
    
    return render_template('all_challenges.html', 
                          plaintext1=plaintext1,
                          ciphertext1=ciphertext1,
                          plaintext2=plaintext2,
                          ciphertext2=ciphertext2,
                          key=key)

# Redirect old challenge routes to the birthday challenge
@app.route('/challenge1')
@app.route('/challenge2')
@app.route('/challenge3')
def redirect_to_challenges():
    return redirect(url_for('birthday_challenge'))

# API endpoint for verification
@app.route('/api/challenge-verify', methods=['POST'])
def verify_challenge():
    data = request.json
    challenge_type = data.get('challenge')
    answer = data.get('answer')
    
    if challenge_type == 'caesar':
        # Verify Caesar cipher solution
        encrypted = "lettc fmvxlhec xs qc jezsvmxi gcfivwigyvmxc uyiir pmwe!"
        decrypted = caesar_cipher(encrypted, 4, decrypt=True)
        check = "happy birthday to my favorite cybersecurity queen lisa!"
        
        return jsonify({
            'success': True,
            'correct': answer.lower().strip() == decrypted
        })
    
    elif challenge_type == 'vigenere':
        # Verify Vigenere cipher solution
        encrypted = "i afdp ydl ttz, bp qycgvltbav plczvz rigc!"
        decrypted = vigenere_cipher(encrypted, "april", decrypt=True)
        check = "i love you liz, my incredible hacker girl!"
        
        return jsonify({
            'success': True,
            'correct': answer.lower().strip() == decrypted
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid challenge type'
    })

if __name__ == '__main__':
    # Print the cipher outputs for verification
    print("\nCaesar plain: ", "happy birthday to my favorite cybersecurity queen lisa!")
    print("Caesar cipher:", caesar_cipher("happy birthday to my favorite cybersecurity queen lisa!", 4))
    
    print("\nVigenère plain: ", "i love you liz, my incredible hacker girl!")
    print("Vigenère cipher:", vigenere_cipher("i love you liz, my incredible hacker girl!", "april"))
    
    app.run(debug=True) 