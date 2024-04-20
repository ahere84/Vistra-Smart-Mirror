import websocket
import threading
import json
from time import time
from EventManager import EventManager

event_manager = EventManager()
last_processed_time = 0
process_interval = 0.1  # Process every 0.1 seconds

def on_message(ws, message):
    global last_processed_time
    try:
       # current_time = time()
        # Parse the JSON data received from the server
        data = json.loads(message)
        print("Parsed Data:", data)
        
        
        event_manager.send_event('GazeMove', x=data["GazeX"], y=data["GazeY"])
        
        # Example processing: print out GazeX and GazeY
        #send data to send event of GazeX and GazeY
        #also processing gaze data at every 10tenth of second for optimized update 
        #if current_time - last_processed_time >= process_interval:
       #     data = json.loads(message)
       #     event_manager.send_event('GazeMove', x=data["GazeX"], y=data["GazeY"])
        #    last_processed_time = current_time
        
    except json.JSONDecodeError:
        print("Error decoding JSON")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, status_code, message):
    print(f"Connection closed with status code {status_code} and message {message}")

def on_open(ws):
    def run(*args):
        app_key = "AppKeyTrial" #registered key
        ws.send(app_key)
        print("AppKey sent to server:", app_key)
    threading.Thread(target=run).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:43333", #"ws://127.0.0.1:43333"
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
