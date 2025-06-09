print("Importing dotenv")
from dotenv import load_dotenv
print("Importing os")
import os
print("Importing discord")
import discord
print("Importing app_commands")
from discord import app_commands
print("Importing utils")
from discord.utils import get
print("Importing gacha")
from commands import gacha_group, custom_group
print("Importing request n cooking")
from rishan import Request, Cooking
print("Importing random")
import random

print("Loading dotenv")
load_dotenv()
discordkey: str = os.getenv('discordkey')
print("Loaded discordkey")

class Client(discord.Client):
    ROLE_NAME = "Member"
    COOKING_ROLE = "Cooking"
    EMOJI = "✅"
    TRACKED_MESSAGE_ID = 1342135518338613272

    WORD_FILTER = ["Fuck", "Rishan","Nigger","Nigga",
                   "onlyfans","cock","penis","dick","vagina",
                   "faggot","fellat","porn","rimjob",
                   "alcohol","cigarette","weed","drugs",
                   "cocaine","heroin","meth","fentanyl","mdma","ecstasy","lsd","acid","mushrooms","shrooms","ketamine","k-hole","xanax","xanny","lean","syrup",
                   "vape","vaping","vape","hookah","shisha","cigars","cigar","cigarette","cig","blunt","joint",
                   "asshole","rape","whore","hoe","cb","kontol","babi","anjing","asu","babi","sial","tolol","goblok","sampah","bangsat","bajingan","memek","jembut","tai","tai kucing","tai ayam","tai kambing","tai sapi",
                   "kys","yiff","porn","gay","sex"," bara","futa","hentai","loli","shota","yaoi","yuri","incest","pedo",
                   "furry","furries","fursuit","fursuits"
                   ]

    SERVER_ADMIN_CHANNELS = {
        937708790793502803: 974317952377716756,   # Server 1
        1333097847096082543: 1359891372831670554  # Server 2
    }

    def __init__(self, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.template = """ ... """  # (unchanged)

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            await self.tree.sync()
            print("Slash commands and context menus synced!")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def setup_hook(self):
        self.tree.add_command(gacha_group)
        self.tree.add_command(custom_group)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if any(word.lower() in message.content.lower() for word in self.WORD_FILTER):
            if any(role.name == self.COOKING_ROLE for role in message.author.roles):
                try:
                    await message.add_reaction("🔥")
                except Exception as e:
                    print(f"Couldn't add reaction: {e}")
            else:
                try:
                    await message.delete()
                    try:
                        await message.author.send(
                            f"⚠️ Your message in **#{message.channel}** was removed because it contained a restricted word. Please follow the dictatorship's rules."
                        )
                    except discord.Forbidden:
                        print(f"Could not DM user {message.author}.")

                    admin_channel_id = self.SERVER_ADMIN_CHANNELS.get(message.guild.id)
                    if admin_channel_id:
                        admin_channel = self.get_channel(admin_channel_id)
                        if admin_channel:
                            embed = discord.Embed(
                                title="🚫 Word Filter Triggered",
                                description=f"**User:** {message.author} (`{message.author.id}`)\n"
                                            f"**Channel:** <#{message.channel.id}>\n"
                                            f"**Content:** `{message.content}`",
                                color=discord.Color.red()
                            )
                            await admin_channel.send(embed=embed)
                except Exception as e:
                    print(f"Error filtering message: {e}")
                return

        try:
            if message.content == "!welcome":
                try:
                    media_folder = "./joinmedia"
                    images = [
                        f for f in os.listdir(media_folder)
                        if f.endswith(('.png', '.jpg', '.jpeg', '.gif')) and not f.startswith('temp_')
                    ]
                    if not images:
                        print("No images found in the media folder.")
                        return

                    random_image = os.path.join(media_folder, random.choice(images))

                    await message.channel.send(
                        f"Welcome!!\n"+
                        f"For you, here's what you can do here.\n"+
                        f"You can view <#1338038250685726820> to find out the various channels, or you can first introduce yourself at <#1338021134612041739>!",
                        file=discord.File(random_image)
                    )
                except Exception as e:
                    print(f"Error in !welcome: {e}")
                return

            if all(role.name != "Cooking" for role in message.author.roles):
                return

            if self.user in message.mentions:
                response = Request(message.content, self.template)
            elif "I summon the word of r" in message.content.lower():
                if any(role.name == "Cooking" for role in message.author.roles):
                    response = Cooking(self.template)
                else:
                    response = "How did you even get here???"
            else:
                return

            for i in range(0, len(response), 2000):
                await message.channel.send(response[i:i+2000])
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("An error occurred. Please try again.")

    async def on_raw_reaction_add(self, payload):
        if self.TRACKED_MESSAGE_ID and payload.message_id == self.TRACKED_MESSAGE_ID and str(payload.emoji) == self.EMOJI:
            guild = self.get_guild(payload.guild_id)
            if guild is None:
                return
            role = get(guild.roles, name=self.ROLE_NAME)
            if role is None:
                print(f"Role '{self.ROLE_NAME}' not found.")
                return
            member = await guild.fetch_member(payload.user_id)
            if member is None or member.bot:
                return
            await member.add_roles(role)
            print(f"Assigned {role.name} to {member.display_name}")

    async def on_raw_reaction_remove(self, payload):
        if self.TRACKED_MESSAGE_ID and payload.message_id == self.TRACKED_MESSAGE_ID and str(payload.emoji) == self.EMOJI:
            guild = self.get_guild(payload.guild_id)
            if guild is None:
                return
            role = get(guild.roles, name=self.ROLE_NAME)
            if role is None:
                print(f"Role '{self.ROLE_NAME}' not found.")
                return
            member = guild.get_member(payload.user_id)
            if member is None or member.bot:
                return
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.display_name}")

    async def on_member_join(self, member):
        try:
            media_folder = "./joinmedia"
            if member.guild.id == 937708790793502803:
                welcome_text = f"aaaaa"
                image_filter = lambda f: "jcc" in f.lower()
            else:
                welcome_text = (
                    f"へい！\n"
                    f"Nice to meet you, {member.mention}, Welcome to JCC Jinsei!\n"
                    f"Enjoy your stay and don't forget to read <#1338036966159290458> to gain access to the rest of the server!"
                )
                image_filter = lambda f: not f.startswith('temp_')

            images = [
                f for f in os.listdir(media_folder)
                if f.endswith(('.png', '.jpg', '.jpeg', '.gif')) and image_filter(f)
            ]
            if not images:
                print("No images found matching filter.")
                return

            random_image = os.path.join(media_folder, random.choice(images))
            channel = member.guild.system_channel
            if channel:
                await channel.send(
                    welcome_text,
                    file=discord.File(random_image)
                )
        except Exception as e:
            print(f"Error in on_member_join: {e}")

print("Getting intents")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
print("Matching intent to client")
client = Client(intents=intents)
print("Running client on discordkey")
client.run(discordkey)
