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

import fortnitepy
import asyncio
import json

with open("config.json", "r") as f:
    config = f.read()
    if not config or not config.startswith("{"):
        config = {}
    else:
        config = json.loads(config) 

async def event_friend_remove(self, friend):
    if config["SETTINGS"]["SEND_FRIEND_REQUESTS_ON_REMOVE"] == 'true':
        try:
            await self.add_friend(friend.id)
            await asyncio.sleep(0.5)
        except:
            pass

async def event_friend_request(self, request):
    try:
        await request.accept()
        await asyncio.sleep(0.5)
    except:
        pass

async def event_friend_add(self, friend):
    if friend is not None:
        await friend.send(f'---\nHey @{friend.display_name}!\nThanks for adding my Bot!\nIf you want to support me for FREE:\n1) Follow me on TikTok: @ludoen,\n2) Follow me on Instagram: @sac_doener\n3 Join on my Discord-Server: https://discord.gg/RVs9hvD - For support, questions etc.')
    if friend is None:
        await friend.send(f'---\nHey!\nThanks for adding my Bot!\nIf you want to support me for FREE:\n1) Follow me on TikTok: @ludoen,\n2) Follow me on Instagram: @sac_doener\n3 Join on my Discord-Server: https://discord.gg/RVs9hvD - For support, questions etc.')
    try:
        await friend.invite()
    except: pass

async def event_friend_request_decline(self, friend):
    if config["SETTINGS"]["SEND_FRIEND_REQUESTS_ON_DECLINE"] == 'true':
        try:
            await self.add_friend(friend.id)
            await asyncio.sleep(0.5)
        except:
            pass

async def event_friend_request_abort(self, friend):
    try:
        await self.add_friend(friend.id)
        await asyncio.sleep(0.5)
    except:
        pass
