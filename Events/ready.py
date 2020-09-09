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


async def check_party_validity(self):
    while True:
        try:
            fixed = False
            if self.party is None:
                await self.initialize_party()
                print(f'Initialized party of {self.display_name}.')
                fixed = True
            if self.party.member_count == 0:
                await self.initialize_party()
                print(f'Initialized party of {self.display_name}.')
                fixed = True
            if not fixed:
                try:
                    party_id = self.party.id
                    party = await self.http.party_lookup(party_id)
                except:
                    await self.initialize_party()
                    print(f'Initialized party of {self.display_name}.')

        except:
            pass
        else:
            await asyncio.sleep(60)

async def event_ready(self):
    friends = self.friends
    friends_accepted = 0
    friends_online_count = 0
    for pending in list(self.incoming_pending_friends):
        try:
            await pending.accept()
            await asyncio.sleep(0.5)
            friends_accepted += 1
        except:
            pass
    for friend in friends:
        if friend.is_online():
            try:
                friends_online_count += 1
            except:
                pass
    await self.initialize_party()
    self.loop.create_task(check_party_validity(self))
    print(f'-----------------------\nClient ready as: {self.user.display_name}\nAccount-ID: {self.user.id}\n-----------------------\nFriends: {len(self.friends)}\nFriends online: {friends_online_count}\nAccepted friend-requests: {friends_accepted}\n-----------------------')

async def event_close(self):
    print(f'{self.user.display_name} is now offline!')

async def event_restart(self):
    print(f'Restarted {self.user.display_name}!')
