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

async def event_party_member_join(self, member):
    if member.id != self.user.id:
        await asyncio.sleep(0.1)
        await self.party.send(f'---\nHey @{member.display_name},\nIf you want to support me for FREE:\n1) Follow me on TikTok: @ludoen,\n2) Follow me on Instagram: @sac_doener\n3 Join on my Discord-Server: https://discord.gg/RVs9hvD')
        if not self.has_friend(member.id):
            try:
                await self.add_friend(member.id)
                await asyncio.sleep(0.5)
            except:
                pass

async def event_party_member_leave(self, member):
    if member.id != self.user.id:
        await asyncio.sleep(0.1)
        if config["SETTINGS"]["INVITE_ON_LEAVE"].lower() == 'true':
            if self.has_friend(member.id):
                try:
                    await member.invite()
                    await asyncio.sleep(0.5)
                except:
                    pass
            if not self.has_friend(member.id):
                try:
                    await self.add_friend(member.id)
                    await asyncio.sleep(0.5)
                except:
                    pass

async def event_party_member_promote(self, old_leader, new_leader):
    if new_leader.id == self.user.id:
        await self.party.send(f'@{old_leader.display_name}, Thanks for promoting me!')
        if not self.has_friend(old_leader.id):
            try:
                await self.add_friend(old_leader.id)
                await asyncio.sleep(0.5)
            except:
                pass

async def event_invalid_party_invite(self, invitation):
    if invitation.sender.display_name in config["SETTINGS"]["OWNER_NAMES"]:
        try:
            await invitation.author.send("I can't join your party because your party is private and I got kicked out of it.")
        except: pass
    
async def event_party_invite(self, invitation):
    if invitation.sender.display_name in config["SETTINGS"]["OWNER_NAMES"]:
        try:
            await invitation.accept()
        except: pass
