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

from .deviceauths import DeviceAuths
from .web import SanicServer
from .bot import LobbyBot
from .sync import SyncBot

import asyncio
import os

import BenBotAsync
import fortnitepy
import aiohttp
import crayons


class PartyBotClient:
    def __init__(self) -> None:
        self.device_auths = None

        self.server = SanicServer(self)
        self.sync = SyncBot(self)

        self.bot = None
        self.httpclient = None

        self.message = '[PartyBot.net] %s'
        self.url = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"

        self.auth_error = False, ""

    async def _set_device_auths(self) -> None:
        if not os.path.isfile('.auth'):
            print(self.message % '[WARNING] No ".auth" file found, creating one for you. '
                                 'Please paste your device auths.')
            open(".auth", "x")

        self.device_auths = DeviceAuths(
            filename='.auth'
        )

        await self.device_auths.load_device_auths()

    async def _setup_lobby_bot(self) -> None:
        self.httpclient = aiohttp.ClientSession()

        if self.device_auths:
            self.bot = LobbyBot(self)

        await self.sync.get_commands()

        from commands.cosmetic import CosmeticCommands
        from commands.client import ClientCommands
        from commands.party import PartyCommands

        self.bot.add_cog(CosmeticCommands(self.bot))
        self.bot.add_cog(ClientCommands(self.bot))
        self.bot.add_cog(PartyCommands(self.bot))

        commands_to_remove = [
            'status',
            'avatar',
            'clean',
            'away',
            'banner',
            'sitout',
            'bp',
            'level',
            'echo',
            'leave',
            'kick',
            'promote',
            'playlist_id',
            'privacy',
            'matchmakingcode',
            'join',
            'friend',
            'playlist',
            'invite',
            'hide',
            'justchattin'
        ]

        async with self.httpclient.request(
            method="GET",
            url="https://partybot.net/api/blacklisted"
        ) as request:
            if request.status == 200:
                commands_to_remove = await request.json()
            else:
                print(crayons.yellow(self.message % '[WARNING] Failed to synchronize, is the PartyBot API down?'))

        for command in commands_to_remove:
            self.bot.remove_command(command)

    async def start(self) -> None:
        print(crayons.cyan(self.message % 'PartyBot made by xMistt. '
                                          'Massive credit to Terbau for creating the library.'))
        print(crayons.cyan(self.message % f'Discord server: https://discord.gg/fnpy - For support, questions, etc.'))

        await self._set_device_auths()

        await self.server.register_routes()
        await self.server.start_server()

        await self._setup_lobby_bot()

        try:
            await self.bot.start()
        except fortnitepy.errors.AuthException as e:
            self.auth_error = True, str(e)
            print(crayons.red(self.message % f"[ERROR] {e}"))

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        loop.run_forever()
        # loop.close()
