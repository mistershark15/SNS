import socket
import threading
import random
from colorama import init, Fore

# Inicializace knihovny colorama
init(autoreset=True)

# ASCII Art
ascii_art = '''
                                                        
                                                        
                                                        
         .#@@@#.                                        
       #@@#.                     :@@@@@@@@#.            
       %@                     :@@@*.     -@@*           
       %@@+                  %@@.          =@@+         
         +@@@*     +@:      -@#                         
            +@@=   *@:      -@*                         
              @@   @@@       =@@+                       
              @@  %@@@         *@@@.                    
    -*        @@ .@@@@     *@.   .#@@=                  
    %@-      *@@ -@+@@     @%.      -@@@%:              
     @%      @@. @@.@@    @@=          :@@@.            
     #@:   .@@= *@: @@   =@#             -@@            
     -@@: :@@= -@#. *@+ :@@.             :@@            
      .@@@@%  :@@   :@*.%@             +@@%.            
              @@=   :@*-@*          *@@@*               
             :@@    .@@@@      =@@@@%.                  
             *@.     %@@-  *@@@@*                       
             *@.     =@@                                
     :#. @@*                                            
     -@@*@@   .@@@@@%.      -@@@@@@@*                   
      :@@@-        +@@      -@=    =@@-                 
       %@@-       #@@@:     :@@-    *@-                 
        #@:     :%+ =@*  :+   #@@@@@@@                  
                 :@@@#                                  
Welcome in Shark Network System.All you can find on SNS site
https://perfektnistranky.wixsite.com/sharknetworksystem .
Made by Mr Shark
'''

# Seznam dostupných barev
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Vybereme náhodnou barvu pro ASCII art
ascii_color = random.choice(colors)
print(ascii_color + ascii_art)

def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        encrypted_text += chr((ord(char) + shift) % 256)
    return encrypted_text

def caesar_cipher_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        decrypted_text += chr((ord(char) - shift) % 256)
    return decrypted_text

SHIFT = 69

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.95', 12345))  # Nahraďte '192.168.1.95' IP adresou serveru

room_name = input("Enter the room name: ")
client.send(room_name.encode('utf-8'))
password = input("Enter the room password: ")
client.send(password.encode('utf-8'))

response = client.recv(1024).decode('utf-8')
if response == 'WRONG_PASSWORD':
    print("Incorrect password. Connection closed.")
    client.close()
    exit()

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

# Vybereme náhodnou barvu pro tohoto uživatele
user_color = random.choice(colors)

def receive():
    while True:
        try:
            encrypted_message = client.recv(1024).decode('utf-8')
            message = caesar_cipher_decrypt(encrypted_message, SHIFT)
            if message == 'NICK':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    while True:
        try:
            message = f'{username}: {input("")}'
            encrypted_message = caesar_cipher_encrypt(user_color + message + Fore.RESET, SHIFT)
            client.send(encrypted_message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
