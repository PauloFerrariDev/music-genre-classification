import keyboard
# import identify

# Define the key to listen to
key_to_listen = ' '  # You can change this to any key you want

# Function to be called when the key is pressed
def on_key_event():
    print("Key was pressed!")
    # identify.run_singer_classifier_audios_script()
    # identify.run_singer_classifier_recording_script()
    # Here you can place the code you want to execute
    # You can also call another Python script
    # For example, using exec(open("other_script.py").read())
 
# Set up the key listener
keyboard.on_press_key(key_to_listen, lambda _: on_key_event())

# Keep the script running
print(f"< Press SPACE to record >")
keyboard.wait('esc')  # The script will keep running until 'esc' is pressed
