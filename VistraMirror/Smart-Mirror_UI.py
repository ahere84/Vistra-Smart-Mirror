from pathlib import Path
import tkinter as tk 
from PIL import Image, ImageTk
from SettingsManager import SettingsManager


def create_window():
    root = tk.Tk()
    root.title('Vistra Mirror UI')


    root.geometry('1080x1920')
    root.config(bg= 'black')


    # Load the configuration
    SettingsManager.load_config(SettingsManager.configPath)  # Ensure this is the correct path to your config file
    
    image_positions = {
        'top_left': (50, 50),
        'top_right': (830, 50),
        'bottom_left': (50, 1620),
        'bottom_right': (830, 1620)
    }

    images = {}
    labels = {}
    for key, (x, y) in image_positions.items():
        try:
            img_path = SettingsManager.get_path("image_path/" + key) # Ensure you're using get() for safety
            if not img_path:
                raise ValueError(f"No path found for {key}")

            img = Image.open(Path(img_path))  # Use Path for better path handling
        
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            images[key] = photo
            label = tk.Label(root, image=photo, bg= 'black')
            label.place(x=x, y=y)
            labels[key] = label
        except Exception as e:
            print(f"Error processing {key}: {e}")

    root.mainloop()


if __name__ == '__main__':
    create_window()