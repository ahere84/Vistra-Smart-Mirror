import websocket
import threading
import json

def on_message(ws, message):
    try:
        # Parse the JSON data received from the server
        data = json.loads(message)
        print("Parsed Data:", data)
        
        # Example processing: print out GazeX and GazeY
        print("GazeX:", data["GazeX"], "GazeY:", data["GazeY"])
        
        # Further processing can be done here
        # For example, storing data in a database, or updating a live graph

    except json.JSONDecodeError:
        print("Error decoding JSON")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, status_code, message):
    print(f"Connection closed with status code {status_code} and message {message}")

def on_open(ws):
    def run(*args):
        app_key = "AppKeyTrial"  # Ensure to replace with your actual app key
        ws.send(app_key)
        print("AppKey sent to server:", app_key)
    threading.Thread(target=run).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:43333",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
