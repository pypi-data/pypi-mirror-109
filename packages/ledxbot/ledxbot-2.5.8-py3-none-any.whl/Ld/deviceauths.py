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

# System imports.
from typing import Optional, Union

import json

import aiofiles


class DeviceAuth:
    def __init__(self,
                 device_id: Optional[str] = None,
                 account_id: Optional[str] = None,
                 secret: Optional[str] = None
                 ) -> None:
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret


class DeviceAuths:
    def __init__(self, filename: str) -> None:
        self.device_auth = None
        self.filename = filename

    async def load_device_auths(self) -> None:
        raw_device_auths = {}

        async with aiofiles.open(self.filename, mode='r') as f:
            async for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                raw_device_auths[key] = value.replace("\"", "")

        self.device_auth = DeviceAuth(
            device_id=raw_device_auths['DEVICE_ID'] if 'DEVICE_ID' in raw_device_auths else None,
            account_id=raw_device_auths['ACCOUNT_ID'] if 'ACCOUNT_ID' in raw_device_auths else None,
            secret=raw_device_auths['SECRET'] if 'SECRET' in raw_device_auths else None
        )

    def get_device_auth(self) -> Union[DeviceAuth, None]:
        return self.device_auth
