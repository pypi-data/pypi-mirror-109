 # -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2020
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
Software: PartyBot (fortnitepy-bot)
License: Apache 2.0

You are one honestly one of the saddest person to ever live
and I genuinely dislike you. People like you think the
world is yours and you can just take it. I spent hours and
hours writing this code for you to just steal it, I hope you
feel better about yourself after you exploit my honest code
for money, for supporters, for discord members, etc.

Fuck you.
"""

from .defaults import Defaults

import aiofiles
import os


class SyncBot:
    def __init__(self, client: "LdClient") -> None:
        self.client = client

    async def get_commands(self) -> None:
        if not os.path.isdir('commands'):
            os.mkdir('commands')

        command_files = ['cosmetic', 'client', 'party']

        for command_file in command_files:
            async with self.client.httpclient.request(
                method="GET",
                url=f"https://raw.githubusercontent.com/xMistt/fortnitepy-bot/master/partybot/{command_file}.py"
            ) as request:
                raw = await request.text(encoding='utf-8')

            async with aiofiles.open(f'commands/{command_file}.py', 'w', encoding='utf-8') as f:
                await f.truncate()
                await f.write(raw.strip())

    async def get_default_cosmetics(self) -> None:
        async with self.client.httpclient.request(
            method="GET",
            url="https://partybot.net/api/cosmetics"
        ) as request:
            data = await request.json()

        return Defaults(data)
