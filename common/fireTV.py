import subprocess

class FTVController:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # adb keyevent num is below
        self.gesture_order_map = {  'Up': 19,
                                    'Down': 20,
                                    'Left': 21,
                                    'Right': 22,
                                    'Select': 66,
                                    'Back': 4,
                                    'Home': 3,
                                    'Menue': 1,
                                    'StartStop': 85}
        
    def __del__(self):
        self.kill()
    
    def connect(self):
        if subprocess.run(['adb', 'connect', f'{self.ip}:{self.port}']).returncode == 0:
            print('\tsuccessfully connected')
            return 0
        else:
            print('could not connect')
            return 1

    def command(self, key):
        if subprocess.run(['adb', 'shell', 'input', 'keyevent', str(self.gesture_order_map[key])]):
            print(f'send {key} command')
    
    def kill(self):
        subprocess.run(['adb', 'kill-server'])
    
    def restart(self):
        subprocess.run(['adb', 'start-server'])
    
    
if __name__=="__main__":
    pass