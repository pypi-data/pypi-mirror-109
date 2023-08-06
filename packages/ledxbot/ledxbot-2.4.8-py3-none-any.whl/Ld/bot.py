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

from fortnitepy.ext import commands
from typing import Any

import functools
import asyncio
import json
import crayons

import fortnitepy
import FortniteAPIAsync


class LobbyBot(commands.Bot):
    def __init__(self, client: "PartyBotClient", **kwargs) -> None:
        self.client = client
        self.message = client.message

        self.fortnite_api = FortniteAPIAsync.APIClient()
        self.defaults = Defaults()

        device_auth = self.client.device_auths.get_device_auth()

        super().__init__(
            command_prefix='!',
            auth=fortnitepy.DeviceAuth(
                account_id=device_auth.account_id,
                device_id=device_auth.device_id,
                secret=device_auth.secret
            ),
            status=self.defaults.status,
            default_party_config=fortnitepy.DefaultPartyConfig(
                privacy=fortnitepy.PartyPrivacy.PUBLIC
            ),
            **kwargs
        )

    async def set_and_update_member_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.me.patch(updated=prop)

    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)

    async def update_defaults(self) -> None:
        while True:
            updated_defaults = await self.client.sync.get_default_cosmetics()
            self.defaults = updated_defaults

            await self.set_presence(self.defaults.status)

            await asyncio.sleep(3600)

    async def event_ready(self) -> None:
        print(crayons.green(self.client.message % f'Client ready as {self.user.display_name}.'))

        self.loop.create_task(self.update_defaults())

        # await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

        try:
            async with self.client.httpclient.request(
                method="POST",
                url="https://partybot.net/api/submit",
                data=json.dumps({
                    "url": self.client.url
                })
            ) as request:
                data = await request.json()

                if request.status == 200:
                    print(self.client.message % 'Successfully submitted url.')
                else:
                    print(
                        crayons.yellow(self.client.message % f'[WARNING] Status {request.status} when trying to '
                                                             f'submit url - '
                                                             f'{data["error"] if "error" in data else data["message"]}'
                                       ))
        except Exception as e:
            print(crayons.red(self.client.message % f'[ERROR] Python error when trying to submit url - {e}.'))

        for pending in self.incoming_pending_friends:
            try:
                epic_friend = await pending.accept() if self.settings.friend_accept else await pending.decline()
                if isinstance(epic_friend, fortnitepy.Friend):
                    print(self.client.message % f"Accepted friend request from: {epic_friend.display_name}.")
                else:
                    print(self.client.message % f"Declined friend request from: {pending.display_name}.")
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise

                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.accept() if self.settings.friend_accept else await pending.decline()

    async def event_party_invite(self, invite: fortnitepy.ReceivedPartyInvitation) -> None:
        await invite.accept()
        print(self.client.message % f'Accepted party invite from {invite.sender.display_name}.')

    async def event_friend_request(self, request: fortnitepy.IncomingPendingFriend) -> None:
        if isinstance(request, fortnitepy.OutgoingPendingFriend):
            return

        await request.accept()
        print(self.client.message % f"Received & accepted friend request from: {request.display_name}.")

    async def event_party_member_join(self, member: fortnitepy.PartyMember) -> None:
        await self.party.send(self.defaults.welcome.replace('{DISPLAY_NAME}', member.display_name))

        if self.default_party_member_config.cls is not fortnitepy.party.JustChattingClientPartyMember:
            await self.party.me.edit(
                functools.partial(
                    self.party.me.set_outfit,
                    self.defaults.skin
                ),
                functools.partial(
                    self.party.me.set_backpack,
                    self.defaults.backpack
                ),
                functools.partial(
                    self.party.me.set_pickaxe,
                    self.defaults.pickaxe
                ),
                functools.partial(
                    self.party.me.set_banner,
                    icon=self.defaults.banner,
                    color=self.defaults.banner_colour,
                    season_level=self.defaults.level
                ),
                functools.partial(
                    self.party.me.set_battlepass_info,
                    has_purchased=True,
                    level=self.defaults.tier
                )
            )

        await asyncio.sleep(1)

        if self.default_party_member_config.cls is not fortnitepy.party.JustChattingClientPartyMember:
            await self.party.me.clear_emote()
            await self.party.me.set_emote(asset=self.defaults.emote)

            if self.user.display_name != member.display_name:
                print(self.client.message % f"{member.display_name} has joined the lobby.")

    async def event_friend_message(self, message: fortnitepy.FriendMessage) -> None:
        print(self.client.message % f'{message.author.display_name}: {message.content}.')

        await message.reply(self.defaults.whisper.replace('{DISPLAY_NAME}', message.author.display_name))

    async def event_command_error(self, ctx: fortnitepy.ext.commands.Context,
                                  error: fortnitepy.ext.commands.CommandError) -> None:
        if isinstance(error, fortnitepy.ext.commands.errors.CommandNotFound):
            if isinstance(ctx.message, fortnitepy.FriendMessage):
                await ctx.send('Command not found, are you sure it exists?')
            else:
                pass
        elif isinstance(error, fortnitepy.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Failed to execute commands as there are missing requirements, please check usage.')
        elif isinstance(error, fortnitepy.ext.commands.errors.PrivateMessageOnly):
            pass
        else:
            await ctx.send(f'When trying to process !{ctx.command.name}, an error occured: "{error}"\n'
                           f'Please report this on Discord or GitHub.')
            raise error

    # async def event_party_privacy_change(self,
    #                                      party: fortnitepy.ClientParty,
    #                                      before: fortnitepy.PartyPrivacy,
    #                                      after: fortnitepy.PartyPrivacy
    #                                      ) -> None:
    #     if self.party.me.leader and self.party.privacy != fortnitepy.PartyPrivacy.PUBLIC:
    #         await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
