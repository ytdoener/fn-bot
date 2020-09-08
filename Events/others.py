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

async def event_device_auth_generate(self, details, email):
    print(details)
    with open("auths.json", "r") as f:
        text = f.read()

        auths = json.loads(text)

    auths[email] = details

    with open("auths.json", "w+") as f:
        text = json.dumps(auths)
        f.write(text)
