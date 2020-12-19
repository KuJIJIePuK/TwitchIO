"""
The MIT License (MIT)

Copyright (c) 2017-2020 TwitchIO

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
from typing import Union, Callable

from .websocket import WSConnection
from .http import TwitchHTTP


class Client:

    def __init__(self,
                 irc_token: str,
                 *,
                 nick: str,
                 api_token: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 initial_channels: Union[list, tuple, Callable] = None,
                 loop: asyncio.AbstractEventLoop = None,
                 **kwargs
                 ):

        self._nick = nick.lower()
        self.loop = loop or asyncio.get_event_loop()
        self._connection = WSConnection(bot=self, token=irc_token, nick=nick.lower(), loop=self.loop,
                                        initial_channels=initial_channels)
        self._http = TwitchHTTP(self, nick, api_token=api_token, client_id=client_id, client_secret=client_secret)


    def run(self):
        try:
            self.loop.create_task(self._connection._connect())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.create_task(self.close())

    async def close(self):
        # TODO session close
        self._connection._close()