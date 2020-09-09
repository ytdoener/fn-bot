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
import fortnitepy
import json
import random
import requests

from typing import Tuple, Any, Union, Optional

def get_random_chapter1_default_cid(self) -> str:
    return random.choice(list(fortnitepy.DefaultCharactersChapter1)).name

with open("config.json", "r") as f:
    config = f.read()
    if not config or not config.startswith("{"):
        config = {}
    else:
        config = json.loads(config) 

async def Command(self, message):
    content = message.content.lower()
    args = content.split(" ")
    split = args[1:]
    joinedArguments = " ".join(split)

    if not self.has_friend(message.author.id):
        try:
            await self.add_friend(message.author.id)
            await asyncio.sleep(0.5)
        except:
            pass
                            
    if args[0] == '!promote':
        if not message.author.display_name in config["SETTINGS"]["OWNER_NAMES"]:
            await message.reply('You dont have the permissions to use this command.')
        if message.author.display_name in config["SETTINGS"]["OWNER_NAMES"]:
            await message.author.promote()

    if args[0] == '?friends' or args[0] == '!friends':
        await message.reply(f'I have {len(self.friends)} friends and {sum(1 for friend in self.friends if friend.is_online())} of them are online.')

    if args[0] == '?party' or args[0] == '!party':
        if self.party:
            await message.reply(f"---\nMembers: {len(self.party.members)}\nPrivacy: {self.party.privacy.name}\nLeader: {self.party.leader.display_name}")

    if args[0] == '?members' or args[0] == '!members':
        if self.party:
            await message.reply(f"---\nMembers: {[member.display_name for member in self.party.members]}")

    if content == '!remove all friends':
        if message.author.display_name in config["SETTINGS"]["OWNER_NAMES"]:
            deletedFriends = 0
            for friend in self.friends:
                if friend.display_name not in config["SETTINGS"]["OWNER_NAMES"]:
                    try:
                        await friend.remove()
                        await asyncio.sleep(0.3)
                        deletedFriends += 1
                    except: pass
            await message.author.send(f'Deleted {deletedFriends} friends.')

    if args[0] == '!playlist' or args[0] == '!playlists' or args[0] == '!gamemode' or args[0] == '!gamemodes':
        playlist = joinedArguments
        playlist_upper = playlist
        playlist = playlist.lower()
        playlist = playlist.strip()
        playlist_search = None
        for item in self.playlists:
            if (item["displayName"].lower().startswith(playlist.lower()) or item["id"].lower == playlist.lower()):
                playlist_search = item
                break

        if not playlist_search:
            await message.reply(f'Playlist {playlist_upper} was not found!')
            return
        await self.party.set_playlist(playlist=playlist_search["id"])
        await message.reply(f'Playlist set to {playlist_search["displayName"]}')
            
    if args[0] == '!skin' or args[0] == '!s':
        skin = joinedArguments
        skin_upper = skin
        skin = skin.lower()
        skin = skin.strip()
        skin_search = None
        for item in self.cosmetics:
            if (item["name"].lower().startswith(skin.lower()) or item["id"].lower == skin.lower()) and item["type"] == "outfit":
                skin_search = item
                break

        if not skin_search:
            await message.reply(f"Skin {skin_upper} was not found!")
            return
        await self.party.me.clear_emote()
        await self.party.me.set_outfit(asset=skin_search["id"])
        await message.reply(f"Skin set to {skin_search['name']}!")

    if args[0] == '!emote' or args[0] == '!e':
        emote = joinedArguments
        emote_upper = emote
        emote = emote.lower()
        emote = emote.strip()
        emote_search = None
        for item in self.cosmetics:
            if (item["name"].lower().startswith(emote.lower()) or item["id"].lower == emote.lower()) and (item["type"] == "emote" or item["type"] == "emoji"):
                emote_search = item
                break

        if not emote_search:
            await message.reply(f"Emote {emote_upper} was not found!")
            return

        if emote_search["type"] == "emote":
            await self.party.me.set_emote(emote_search["id"])
        
        elif emote_search["type"] == "emoji":
            await self.party.me.set_emoji(emote_search["id"])
        
        else:
            # How did we get here?
            pass
        await message.reply(f"Emote set to {emote_search['name']}!")

    if args[0] == '!backpack' or args[0] == '!b':
        backpack = joinedArguments
        backpack_upper = backpack
        backpack = backpack.lower()
        backpack = backpack.strip()
        backpack_search = None
        for item in self.cosmetics:
            if (item["name"].lower().startswith(backpack.lower()) or item["id"].lower == backpack.lower()) and item["type"] == "backpack":
                backpack_search = item
                break

        if not backpack_search:
            await message.reply(f"Backpack {backpack_upper} was not found!")
            return

        await self.party.me.set_backpack(backpack_search["id"])
        await message.reply(f"Backpack set to {backpack_search['name']}!")

    if args[0] == '!pickaxe' or args[0] == '!p':
        pickaxe = joinedArguments
        pickaxe_upper = pickaxe
        pickaxe = pickaxe.lower()
        pickaxe = pickaxe.strip()
        pickaxe_search = None
        for item in self.cosmetics:
            if (item["name"].lower().startswith(pickaxe.lower()) or item["id"].lower == pickaxe.lower()) and item["type"] == "pickaxe":
                pickaxe_search = item
                break

        if not pickaxe_search:
            await message.reply(f"Pickaxe {pickaxe_upper} was not found!")
            return

        await self.party.me.set_pickaxe(pickaxe_search["id"])
        await message.reply(f"Pickaxe set to {pickaxe_search['name']}!")
        await asyncio.sleep(0.3)
        await self.party.me.set_emote("EID_IceKing")

    if args[0] == '!leave':
        if message.author.display_name in config["SETTINGS"]["OWNER_NAMES"]:
            try:
                await message.reply('Leaving the party now..')
                await self.party.me.set_emote("EID_Wave")
                await asyncio.sleep(1)
                await self.initialize_party()
            except:
                pass    

    if args[0] == '!level':
        level = args[1]
        if level.isnumeric():
            try:
                await self.party.me.set_banner(season_level=level)
                await message.reply(f'Level set to {level}!')
            except: pass
        if not level.isnumeric():
            try:
                await message.reply('An error has occured. The level needs to be a positive (+) number!')
            except: pass
    
    if args[0] == '!stop' or args[0] == '!clear':
        if args[1] == 'emote':
            await message.reply('Successfully cleared my Emote.')
            await self.party.me.clear_emote()
        if args[1] == 'backpack':
            await message.reply('Successfully cleared my Backpack.')
            await self.party.me.clear_backpack()

    # Cosmetic Shortcuts

    if args[0] == '!purpleskull':
        try:
            await self.party.me.set_outfit("CID_030_Athena_Commando_M_Halloween", variants=self.party.me.create_variants(clothing_color=1))
            await message.reply('Skin set to Skull Trooper with Purple Glow Variant!')
        except: pass
    
    if args[0] == '!checkeredrenegade' or args[0] == '!renegade':
        try:
            await self.party.me.set_outfit("CID_028_Athena_Commando_F", variants=self.party.me.create_variants(material=2))
            await message.reply('Skin set to Checkered Renegade!')
        except: pass

    if args[0] == '!hologram' or args[0] == '!holo':
        try:
            await self.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
            await message.reply('Skin set to Hologram (Star Wars)!')
        except: pass

    if args[0] == '!ironman' or args[0] == '!iron man':
        try:
            await self.party.me.set_outfit("CID_843_Athena_Commando_M_HightowerTomato_Casual", variants=self.party.me.create_variants(progressive=2))
            await message.reply('Skin set to Iron Man!')
        except: pass

    if args[0] == '!hatlessrecon' or args[0] == '!reconexpert' or args[0] == '!nohatrecon':
        try:
            await self.party.me.set_outfit("CID_022_Athena_Commando_F", variants=self.party.me.create_variants(parts=2))
            await message.reply('Skin set to Hatless Recon!')
        except: pass

    if args[0] == '!ninja':
        try:
            await self.party.me.set_outfit("CID_605_Athena_Commando_M_TourBus")
            await message.reply('Skin set to Ninja!')
        except: pass

    if args[0] == '!invisible' or args[0] == '!invis':
        try:
            await self.party.me.set_outfit("CID_YoIWantToGetMyselfInvisibleSoJustIgnoreThisThankYou")
            await message.reply('Successfully made myself INVISIBLE!')
        except:
            pass

    if args[0] == '!visible':
        try:
            await self.party.me.set_outfit(f'{config["COSMETIC_SETTINGS"]["OUTFIT"]}')
            await message.reply('Successfully made myself VISIBLE!')
        except:
            pass

    if args[0] == '!pinkghoul':
        try:
            await self.party.me.set_outfit("CID_029_Athena_Commando_F_Halloween", variants=self.party.me.create_variants(material=3))
            await message.reply('Skin set to Ghoul Trooper with Pink Variant!')
        except: pass

    if args[0] == '!mintyelf':
        try:
            await self.party.me.set_outfit("CID_051_Athena_Commando_M_HolidayElf",variants=self.party.me.create_variants(material=2))
            await message.reply('Skin set to Minty Elf!')
        except: pass

    if args[0] == '!sitout':
        try:
            await self.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        except: pass

    if args[0] == '!ready':
        try:
            await message.reply('Readiness set to READY!')
            await self.party.me.set_ready(fortnitepy.ReadyState.READY)
        except: pass

    if args[0] == '!unready':
        try:
            await message.reply('Readiness set to UNREADY!')
            await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        except: pass
