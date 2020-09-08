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

import requests
import asyncio
import json

with open("config.json", "r") as f:
    config = f.read()
    if not config or not config.startswith("{"):
        config = {}
    else:
        config = json.loads(config) 

def update_check():
    r = requests.get("https://fortnite-api.com/cosmetics/br")

    if str(r.status_code).startswith("2"):

        with open("cosmetics.json", "w+") as f:
            jsson = r.json()
            cosmetics = jsson["data"]
            jsson = json.dumps(cosmetics)
            f.write(jsson)
            print('Updated Cosmetics!')
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
            jsson = a.json()
            playlists = jsson
            jsson = json.dumps(playlists)
            f.write(jsson)
            print('Updated Playlists!')
    else:
        with open("playlists.json", "r") as f:
            text = f.read()
            if not text:
                raise Exception("File not found, and not Code 200")
                
            jsson = json.loads(text)
            playlists = jsson