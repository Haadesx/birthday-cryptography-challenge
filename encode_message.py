import base64

message = """I love you, Lisa! The universe kept us in the same class for 3.5 years, yet it wasn't until semester 7 that we finally found each other. It was always meant to be. Your brilliant mind, beautiful smile, and kind heart make me fall deeper in love with you every day. These past months have been the happiest of my life. Happy Birthday, my darling! - Your Pagal"""

encoded = base64.b64encode(message.encode()).decode()
print(encoded)

# Also write to a file for easy copying
with open('encoded_message.txt', 'w') as f:
    f.write(encoded) 