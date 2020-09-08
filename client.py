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
import requests
import sanic

from functools import partial
from fortnitepy import ClientPartyMember
from utils import config, update_check
from Events import ready, party, Friend, Message, others

app = sanic.Sanic('')
server = None

r = requests.get("https://fortnite-api.com/cosmetics/br")

if str(r.status_code).startswith("2"):

    with open("cosmetics.json", "w+") as f:
        jsson = r.json()
        cosmetics = jsson["data"]
        jsson = json.dumps(cosmetics)
else:
    with open("cosmetics.json", "r") as f:
        text = f.read()
        if not text:
            raise Exception("File not found, and not Code 200")
            
        jsson = json.loads(text)
        cosmetics = jsson

a = requests.get("http://scuffedapi.xyz/api/playlists")

if str(a.status_code).startswith("2"):

    with open("playlists.json", "w+") as f:
        jsson1 = a.json()
        playlists = jsson1
        jsson1 = json.dumps(playlists)
else:
    with open("playlists.json", "r") as f:
        text = f.read()
        if not text:
            raise Exception("File not found, and not Code 200")
            
        jsson1 = json.loads(text)
        playlists = jsson

class FNClient(fortnitepy.Client):
    def __init__(self, auth, cosmetics, exchange_code=None, config=None, *args, **kwargs):
        self.cosmetics = cosmetics

        self.config = config

        self.__auth = auth
        if "deviceAuth" in auth.keys():
            self.__auth = auth["deviceAuth"]
        if not auth and not exchange_code:
            raise Exception("DEVICE AUTH OR EXCHANGE CODE!")

        self.invited_on_startup = 0

        self.got_ready = 0

        self.was_offline = {}
        self.resent = {}
        
        if "deviceId" in self.__auth.keys():
            self.deviceId = self.__auth["deviceId"]
        elif "device_id" in self.__auth.keys():
            self.deviceId = self.__auth["device_id"]
        else:
            self.deviceId = ""
            if not exchange_code:
                raise Exception("Auth nicht richtig angegeben.")
            
        if "accountId" in self.__auth.keys():
            self.accountId = self.__auth["accountId"]
        elif "account_id" in self.__auth.keys():
            self.accountId = self.__auth["account_id"]
        else:
            self.accountId = ""
            if not exchange_code:
                raise Exception("Auth nicht richtig angegeben.")

        if "secret" in self.__auth.keys():
            self.secret = self.__auth["secret"]
        else:
            self.secret = ""
            if not exchange_code:
                raise Exception("Auth nicht richtig angegeben.")

        super().__init__(
            auth=fortnitepy.DeviceAuth(
                account_id=self.accountId,
                device_id=self.deviceId,
                secret=self.secret,
                exchange_code=exchange_code if exchange_code else ""
            ),
            status='🔥 YT: SAC Doener 🔥',
            default_party_member_config=fortnitepy.DefaultPartyMemberConfig(meta=[
                partial(ClientPartyMember.set_outfit, config.get("COSMETIC_SETTINGS", {}).get("OUTFIT", "CID_028_Athena_Commando_F")),
                partial(ClientPartyMember.set_backpack, config.get("COSMETIC_SETTINGS", {}).get("BACKPACK", "BID_138_Celestial")),
                partial(ClientPartyMember.set_pickaxe, config.get("COSMETIC_SETTINGS", {}).get("PICKAXE", "Pickaxe_ID_013_Teslacoil")),
                partial(ClientPartyMember.set_banner, config.get("COSMETIC_SETTINGS", {}).get("BANNER", "InfluencerBanner38"), season_level=config.get("COSMETIC_SETTINGS", {}).get("LEVEL", "9999"), color=config.get("COSMETIC_SETTINGS", {}).get("BANNER_COLOR", "black")),
                partial(ClientPartyMember.set_battlepass_info, has_purchased=True, level=config.get("COSMETIC_SETTINGS", {}).get("BATTLEPASS_LEVEL", "9999"), self_boost_xp=True, friend_boost_xp=True)
            
            ]),
            avatar=fortnitepy.Avatar(
                asset=config.get("COSMETIC_SETTINGS", {}).get("AVATAR", "CID_028_Athena_Commando_F"),
                background_colors=config.get("COSMETIC_SETTINGS", {}).get("AVATAR_COLOR", ["#ffffff", "#ffffff", "#ffffff"])
),
        )
        self.default_skin = config.get("COSMETIC_SETTINGS", {}).get("SKIN", "CID_017_Athena_Commando_M")
        self.default_pickaxe = config.get("COSMETIC_SETTINGS", {}).get("PICKAXE", "Pickaxe_ID_013_Teslacoil")
        self.default_backpack = config.get("COSMETIC_SETTINGS", {}).get("BACKPACK", "BID_138_Celestial")
        self.default_banner = config.get("COSMETIC_SETTINGS", {}).get("BANNER", "InfluencerBanner38")
        self.default_banner_color = config.get("COSMETIC_SETTINGS", {}).get("BANNER_COLOR", "black")
        self.default_level = config.get("COSMETIC_SETTINGS", {}).get("LEVEL", "9999")

        self.cosmetics = cosmetics
        self.playlists = playlists
        self.app = app
        self.server = server

    async def event_ready(self):
        await ready.event_ready(self)

    async def event_close(self):
        await ready.event_close(self)

    async def event_restart(self):
        await ready.event_restart

    async def event_party_message(self, message):
        await Message.Command(self, message)

    async def event_friend_message(self, message):
        await Message.Command(self, message)

    async def event_party_member_join(self, member):
        await party.event_party_member_join(self, member)

    async def event_party_member_leave(self, member):
        await party.event_party_member_leave(self, member)
    
    async def event_party_member_promote(self, old_leader, new_leader):
        await party.event_party_member_promote(self, old_leader, new_leader)

    async def event_invalid_party_invite(self, invitation):
        await party.event_invalid_party_invite(self, invitation)
    
    async def event_party_invite(self, invitation):
        await party.event_party_invite(self, invitation)

    async def event_friend_remove(self, friend):
        await Friend.event_friend_remove(self, friend)

    async def event_friend_request(self, request):
        await Friend.event_friend_request(self, request)

    async def event_friend_add(self, friend):
        await Friend.event_friend_add(self, friend)

    async def event_friend_request_decline(self, friend):
        await Friend.event_friend_request_decline(self, friend)

    async def event_friend_request_abort(self, friend):
        await Friend.event_friend_request_abort(self, friend)

    async def event_device_auth_generate(self, details, email):
        await others.event_device_auth_generate(self, details, email)

clients = []

with open(f"./auths.json", "r") as f:
    auth = f.read()
    auth = json.loads(auth)
    for email, dAuth in auth.items():

        client = FNClient(dAuth, cosmetics, config=config)
        clients.append(client)

loop = asyncio.get_event_loop()
loop.create_task(fortnitepy.start_multiple(clients))