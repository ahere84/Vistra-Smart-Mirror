class EventManager:
    def __init__(self):
        self.listeners = {}

    def register_event(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def send_event(self, event_name, **kwargs):
        for callback in self.listeners.get(event_name, []):
            callback(**kwargs)
    
