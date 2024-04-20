from pathlib import Path
import tkinter as tk 
import pyautogui
import time
from logging import root
from PIL import Image, ImageTk
from SettingsManager import SettingsManager
from queue import Queue
from threading import Thread, Timer
from EventManager import EventManager

root = tk.Tk()
message_queue = Queue()
event_manager = EventManager()

def setup_ui():
    global root
    root.title('Vistra Mirror UI')
    root.geometry('1080x1920')
    root.config(bg= 'black')
    
    #root.overrideredirect(True) #removing this will disable tab functions
    
    event_manager.register_event('GazeMove', lambda event: handle_gaze_move(root, event))
    SettingsManager.load_config(SettingsManager.configPath)  # Ensure this is the correct path to your config file

   
    image_positions = {
        'top_left': (50, 5),
        'top_right': (850, 5),
        'back': (90, 1780) #centered x
        #'bottom_left': (50, 1620),
        #'bottom_right': (830, 1620)
    }

    images = {}
    labels = {}
    for key, (x, y) in image_positions.items():
        try:
            img_path = SettingsManager.get_path("image_path/" + key) # Ensure you're using get() for safety
            
            if not img_path: raise ValueError(f"No path found for {key}")
            
            img = Image.open(Path(img_path))  # Use Path for better path handling
   
            if key != 'back': 
                img = img.resize((100, 100), Image.Resampling.LANCZOS) #rescale top icons to match resize
            
            if key == 'top_left': top_left_img = ImageTk.PhotoImage(img)
            if key == 'top_right': top_right_img = ImageTk.PhotoImage(img)
            if key == 'back': back_img = ImageTk.PhotoImage(img) #stores back button, should do the same for the rest maybe a switch
            
            photo = ImageTk.PhotoImage(img)

            images[key] = photo
            label = tk.Label(root, image=photo, bg= 'black')
            label.place(x=x, y=y)
            labels[key] = label    
        except Exception as e:
            print(f"Error processing {key}: {e}")
             # Define back button functionality
    
    def back_app():
        print("Back functionality not implemented yet")
    
    def top_left_app():
        print("left app functionality not implemented yet")
        
    def top_right_app():
        print("right app functionality not implemented yet")
        
    # Clock
    clock_label = tk.Label(root, font=('Helvetica', 35), bg='black', fg='white')
    ampm_label = tk.Label(root, font=('Helvetica', 20), bg='black', fg='white')  # Smaller font size for AM/PM
    ampm_label.place(x=578, y=23)
    clock_label.place(x=460, y=20)  # Positioning the clock at the center; adjust as needed
    update_time(clock_label, ampm_label)
    
    # Create buttons for left, right, and back apps
    back_button = tk.Button(root, image=back_img, command=back_app, bg='black', bd=0, highlightthickness=0)
    back_button.image = back_img  # Keep a reference!
    back_button.place(x=0, y=1742, width=1080, height=200)
    
    top_left_button = tk.Button(root, image=top_left_img, command=top_left_app, bg='black', bd=0, highlightthickness=0)
    top_left_button.image = top_left_img  
    top_left_button.place(x=0, y=5, width= 300, height=200)
    
    top_right_button = tk.Button(root, image=top_right_img, command=top_right_app, bg='black', bd=0, highlightthickness=0)
    top_right_button.image = top_right_img
    top_right_button.place(x=780, y=5, width=300, height=200)


    button_coords = {
        'back_button': (0, 1742, 1080, 1942),
        'top_left_button': (0, 5, 300, 205),
        'top_right_button': (780, 5, 1080, 205)
    }
    active_timers = {}

    def handle_gaze_move(root, event):
        x = event.x
        y = event.y
        print(f"Gaze Coordinates: {x}, {y}")
        
        # Run checks and update the UI in a thread-safe manner using root.after
        #root.after(0, lambda: check_gaze_interaction(x, y))
        event_manager.register_event('GazeMove', lambda event: handle_gaze_move(root, event))


    def check_gaze_interaction(x, y):
        active_timers
        found_button = False
        for button, (x1, y1, x2, y2) in button_coords.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                if button not in active_timers:
                    timer = Timer(3.5, lambda: trigger_click(button))
                    timer.start()
                    active_timers[button] = timer
                found_button = True
                break

        if not found_button:
            clear_timers()

    def clear_timers():
        for timer in active_timers.values():
            if timer.is_alive():
                timer.cancel()
        active_timers.clear()

    def trigger_click(button):
        print(f"Triggering click for {button}")
        pyautogui.click()

        
    root.mainloop()
    
def run_client():
    
    pass    

def center_image(image, window_width, window_height): #handy method 
    image_width, image_height = image.width(), image.height()
    x = (window_width - image_width) // 2
    y = (window_height - image_height) // 2
    return x, y 

def update_time(time_label, ampm_label):
    current_time = time.strftime('%I:%M')  # Time without AM/PM
    am_pm = time.strftime('%p')  # AM/PM
    if current_time.startswith('0'):  # Check if the hour starts with 0
        current_time = current_time[1:]  # Remove the leading zero
    time_label.config(text=current_time)
    ampm_label.config(text=am_pm)
    time_label.after(1000, update_time, time_label, ampm_label)  # Schedule itself to be called after 1000ms
    
def client_thread():
    while True:
        message = message_queue.get()
        if message == 'QUIT':
            break
        
def ui_thread(root):
    while True:
        # Update UI based on received messages
        pass
    
if __name__ == '__main__': 
    root = setup_ui()  # Your function to create and set up the Tkinter UI.
    thread1 = Thread(target=client_thread)
    thread2 = Thread(target=ui_thread, args=(root,))
    thread1.start()
    thread2.start()
    root.mainloop()  # Start the Tkinter event loop.
