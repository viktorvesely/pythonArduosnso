import keyboard

from task import Task

class KeyChecker(Task):

    def __init__(self, callbacks: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callbacks = callbacks
        self.pressed = {key: False for key in self.callbacks.keys()}
    
    def check_keys(self, event):

        name = event.name
        type_ = event.event_type

        if name not in self.callbacks:
            return

        if type_ != keyboard.KEY_DOWN:
            if type_ == keyboard.KEY_UP:
                self.pressed[name] = False
            return

        if self.pressed[name]:
            return
            
        self.pressed[name] = True
        self.callbacks[name]()

    def run(self):
        super().run()
        
        while self.is_running():
            event = keyboard.read_event()
            self.check_keys(event)            
            self.sleep(0.001)