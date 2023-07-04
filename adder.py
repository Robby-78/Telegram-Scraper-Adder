from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerChat, User
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import configparser
import os
import sys
import csv
import traceback
import time
import random
from time import sleep
from telethon.tl.types import ChatForbidden



re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

print(re + "╔╦╗┌─┐┬  ┌─┐╔═╗  ╔═╗┌┬┐┌┬┐┌─┐┬─┐")
print(gr + " ║ ├┤ │  ├┤ ║ ╦  ╠═╣ ││ ││├┤ ├┬┘")
print(re + " ╩ └─┘┴─┘└─┘╚═╝  ╩ ╩─┴┘─┴┘└─┘┴└─")

print(cy + "version : 1.01")
print(cy + "Make sure you Subscribed Termux Professor On Youtube")
print(cy + "www.youtube.com/c/cubiclecyber")

print(re + "NOTE :")
print("1. Telegram only allows adding 200 members to a group by one user.")
print("2. You can use multiple Telegram accounts to add more members.")
print("3. Add only 50 members to the group each time, otherwise, you may get a flood error.")
print("4. Wait for 15-30 minutes before adding members again.")
print("5. Make sure you enable the 'Add User' permission in your group.")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    print(re + "[!] run python setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))

users = []
with open(r"members.csv", encoding='UTF-8') as f:  # Enter your file name
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))

chats.extend(result.chats)

print(gr + 'Choose a group to add members:' + cy)
for i, chat in enumerate(chats):
    print(f"{i}. {chat.title}")


g_index = int(input(gr + "Enter the group number: "))
target_group = chats[g_index]

if isinstance(target_group, InputPeerChannel):
    target_group_entity = target_group
elif isinstance(target_group, ChatForbidden):
    sys.exit("You are not allowed to add members to this group.")
else:
    target_group_entity = client.get_input_entity(target_group)

    sys.exit("Invalid target group.")

# ... remaining code ...


n = 0
batch_size = 50
delay_seconds = 60

mode = int(input(gr + "Enter 1 to add by username or 2 to add by ID: " + cy))

for user in users:
    n += 1
    if n % 80 == 0:
        sleep(delay_seconds)
    try:
        print("Adding {} to group: {}".format(user['id'], target_group.title))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = User(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 60-180 Seconds...")
        time.sleep(random.randint(60, 180))
    except PeerFloodError:
        print("Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
        print("Waiting {} seconds".format(20))
        time.sleep(20)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        print("Waiting for 5 Seconds...")
        time.sleep(random.randint(60, 180))
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

time.sleep(random.randint(300, 600))

# ... remaining code ...
