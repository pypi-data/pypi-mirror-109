import asyncio
import json
import logging
import time
import re
import sys
import random
from typing import List, Union

from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, User
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated,
    UserDeactivatedBan,
    FloodWait,
    YouBlockedUser,
    UsernameInvalid, UsernameNotOccupied
)

logger = logging.getLogger(__name__)

session_name = ":memory:"


class Listen():
    token: str = None
    allow_submit: bool = None
    keywords: List[str] = []

    def __init__(
        self,
        botid: str = "ajtwBot",
        api_id: str = "5480654",
        api_hash: str = "09c7620e6734844b6992c209426f5e97",
        proxy: dict = None,
        show_msg: bool = None
    ):

        if proxy:
            self.__check_proxy(proxy)

        self.botid = botid
        self.show_msg = bool(show_msg)

        try:
            self.client = Client(session_name, api_id=api_id,
                                 api_hash=api_hash, proxy=proxy)
        except AuthKeyUnregistered:
            self.__log("登录身份失效")
        except (UserDeactivated, UserDeactivatedBan):
            self.__log("账号被封禁或销号")
        except Exception as e:
            logger.error(str(e), exc_info=True)
        else:
            self.client.add_handler(
                MessageHandler(
                    self.__query_token, filters=filters.me & filters.regex("^token$"))
            )

            self.client.add_handler(MessageHandler(
                self.__onSubmit, filters=filters.group & filters.text & ~filters.bot))

            self.client.add_handler(
                MessageHandler(
                    self.__onError, filters=filters.user(self.botid) & filters.regex("^(出错了)"))
            )

            self.client.add_handler(
                MessageHandler(
                    self.__onToken, filters=filters.user(self.botid) & filters.command("token"))
            )

    async def start(self):
        await self.client.start()
        self.me = await self.client.get_me()
        self.__log(
            f"监听账号：{self.me.first_name}{('(@'+self.me.username+')') if self.me.username else ''}上线")
        await self.__query_token()
        await idle()
        await self.client.stop()
        self.__log("结束消息监听，程序已停止")

    def __log(self, msg: str):
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f'[{timestr}] {msg}')

    def __check_proxy(self, proxy: dict):
        pattern = re.compile(
            r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')

        for k, v in proxy.items():
            if k not in ["hostname", "port", "username", "password"]:
                raise NameError(f'proxy中不能包含{k}字段')
            elif k == "hostname" and (not isinstance(v, str) or not pattern.match(v)):
                raise NameError("proxy中的hostname值必须是一个ip地址")
            elif k == "port" and not isinstance(v, int):
                raise NameError("proxy中的port值必须是一个端口数字")

    async def __onError(self, _, message: Message):
        self.allow_submit = False
        self.token = None
        self.__log(message.text)
        sys.exit()

    async def __onToken(self, _, message: Message):
        await message.delete()
        if len(message.command) > 1:
            self.token = message.command[1]
            self.keywords = message.command[2:]
            if not self.keywords:
                self.__log("主账号没有设置关键词")
                sys.exit()
            else:
                msg = "、".join(self.keywords)
                self.__log(f"监听关键词：{msg}")
                self.__log("如主账号的关键词有变化，请发送：token")
                self.allow_submit = True

    async def __query_token(self,*args):
        self.allow_submit = None
        try:
            msg = await self.client.send_message(self.botid, "/ajtw token")
        except YouBlockedUser as e:
            self.__log(f"@{self.botid} 已被你屏蔽")
        except (UserDeactivated, UserDeactivatedBan, UsernameInvalid, UsernameNotOccupied):
            self.__log(f"@{self.botid} 可能无效")
        except Exception as e:
            self.__log(str(e))
            logger.error(str(e), exc_info=True)
        else:
            await msg.delete()
            await asyncio.sleep(5)
            if self.allow_submit is None:
                self.allow_submit = False

    def __invalid_content(self, content: str):
        length = len(content)
        if length < 2 or length > 50:
            return True

    def __invalid_keywords(self, content: str):
        if not self.keywords:
            return True
        else:
            pattern = re.compile("|".join(self.keywords), re.I | re.M)
            return not bool(pattern.search(content))

    async def __onSubmit(self, _, message: Message):
        if self.allow_submit is None or self.__invalid_content(message.text):
            return
        elif self.__invalid_keywords(message.text):
            return

        message_id = message.message_id
        chat = message.chat
        user = message.from_user

        if self.show_msg:
            self.__log(f"{message.text}\t{chat.title}")

        text = {
            "token": self.token,
            "userid": self.me.id,
            "message_id": message_id,
            "chat": {
                "id": chat.id,
                "title": chat.title,
                "username": chat.username,
                "type": chat.type
            },
            "from_user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username
            },
            "content": message.text
        }

        try:
            msg = await self.client.send_message(self.botid, f"/ajtw {json.dumps(text)}")
            await msg.delete()
        except FloodWait as e:
            self.__log(f"提交太频繁，需等待{e.x}秒后再重新提交。")
        except YouBlockedUser as e:
            self.__log(f"@{self.botid} 已被你屏蔽")
        except (UserDeactivated, UserDeactivatedBan, UsernameInvalid, UsernameNotOccupied):
            self.__log(f"@{self.botid} 可能无效")
        except Exception as e:
            logger.error(str(e), exc_info=True)
