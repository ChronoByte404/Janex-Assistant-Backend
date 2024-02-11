import nextcord
from nextcord.ext import commands

import asyncio
import json
import os
from Utilities.functions import loadconfig

class DiscordBot:
    def __init__(self):
        config = loadconfig("Settings/config.json")
        key = loadconfig("Settings/discord_key.json")
        servers = loadconfig("Settings/JURISDICTION.json")

        self.key = key.get("DiscordAPI")
        self.prefix = config.get("Command_Prefix")
        self.UIName = config.get("UIName")
        self.disallowed_words = config.get("disallowed-words")
        self.warning_message = config.get("warning_message")
        self.authorised_users = config.get("Authorised_Users")
        self.incoming_servers = servers.get("servers")
        self.port = config.get("default-port")

        self.discordintents = nextcord.Intents.default()
        self.discordintents.message_content = True
        self.discordintents.reactions = True

        self.client = commands.Bot(command_prefix='/', intents=self.discordintents)
    
    def activate_bot(self):
        @self.client.event
        async def on_message(message):
            if str(message.guild) in self.incoming_servers:
                sentence_words = str(message.content)
                for word in self.disallowed_words:
                    if word in sentence_words:
                        await message.delete()
                        response = await message.channel.send(self.warning_message)
                        time.sleep(4)
                        await response.delete()
                        break
            
            if self.prefix in message.content:
                    user = message.author
                    if "creative" in message.content:
                        guild = message.guild  # Fix here
                        role = discord.utils.get(guild.roles, name="Creative Minecraft")
                        await user.add_roles(role)
                        response = await message.reply("You now have the Creative Minecraft rank! <:creative:1195315907191373905>")
                        time.sleep(1)
                        await message.delete()
                        await response.delete()
                    elif "survival" in message.content:
                        guild = message.guild  # Fix here
                        role = discord.utils.get(guild.roles, name="Survival Minecraft")
                        await user.add_roles(role)
                        response = await message.reply("You now have the Survival Minecraft rank! <:survival:1195315854171185152>")
                        time.sleep(1)
                        await message.delete()
                        await response.delete()
            
            if self.UIName.lower() in message.content.lower() or message.guild is None or message.reference and message.reference.resolved.author == self.client.user:
                await message.channel.trigger_typing()

                self.message = message
                self.user = message.author
                sentence = str(message.content)

                if message.author == self.client.user:
                    return

                sentence = str(sentence)
                sentence = sentence.replace("'", "")
                os.system(f"./Utilities/send_request http://localhost:{self.port} '{sentence}'")

                with open("./short_term_memory/output.txt", "r") as f:
                    ResponseOutput = f.read()
                
                self.ResponseOutput = ResponseOutput

                await message.reply(ResponseOutput)
        
        print(f"Logged in as {self.client}")
        self.client.run(self.key)

