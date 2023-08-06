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


class Defaults:
    def __init__(self, data: dict = {}) -> None:
        self.raw = data

        self.skin = data.get('default_skin', 'CID_028_Athena_Commando_F')
        self.backpack = data.get('default_backpack', 'BID_023_Pinkbear')
        self.pickaxe = data.get('default_pickaxe', 'Pickaxe_Lockjaw')
        self.banner = data.get('banner', 'otherbanner51')
        self.banner_colour = data.get('banner_colour', 'defaultcolor15')
        self.level = data.get('default_level', 999)
        self.tier = data.get('default_bp_tier', 999999999)
        self.emote = data.get('default_emote', 'EID_NoDance')
        self.status = data.get('status', 'https://discord.gg/2kqu5SZMWZ')
        self.welcome = data.get('welcome', 'Notice: Join discord.gg/2kqu5SZMWZ for a free led bot.')
        self.whisper = data.get('whisper', 'If you need help or want your own bot, join discord.gg/2kqu5SZMWZ.')
