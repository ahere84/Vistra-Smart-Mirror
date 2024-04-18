from pathlib import Path
import tkinter as tk 
import time
from PIL import Image, ImageTk
from SettingsManager import SettingsManager


def create_window():
    
    root = tk.Tk()
    root.title('Vistra Mirror UI')
    root.geometry('1080x1920')
    root.config(bg= 'black')
    #root.overrideredirect(True) #removing this will disable tab functions
    
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
    ampm_label.place(x=582, y=23)
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
    
    root.mainloop()
   
      
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
    
if __name__ == '__main__':
    create_window()