import aiohttp
import os
import asyncio
from dotenv import load_dotenv
import json
import re
import discord
import pathlib
import collections



# uncomment during dev. stopgap solution since docker loads env vars 'correctly'.
# load_dotenv() 

OLLAMA_SERVER = str(os.environ.get("OLLAMA_SERVER"))
DISCORD_TOKEN = str(os.environ.get("DISCORD_TOKEN"))
OLLAMA_MODEL_NAME = str(os.environ.get("OLLAMA_MODEL_NAME"))

SYSTEMPROMPT = pathlib.Path("./systemprompt.txt")
ALLOWEDCHANNELS = pathlib.Path("./allowed_channels.txt")

intents = discord.Intents.default()
intents.message_content = True  

bot = discord.Client(intents=intents)

async def IsModel(model):
    async with aiohttp.ClientSession() as client:
        print("Checking models...")
        resp = await client.get(OLLAMA_SERVER + "/api/tags")
        tags = await resp.json()
        print(f"Models:")
        for _model in tags.get("models"):
            print(_model.get("name"))
        out = re.search(model, json.dumps(tags)) # admittedly a really stupid way to do this
        if out:
            print(f"Model {model} exists in ollama. Hooray!")
        else:
            print(f"Model {model} does not exist in ollama.")
        return out
async def PullModel(model):
    async with aiohttp.ClientSession() as client:
        resp = await client.post(OLLAMA_SERVER + "/api/pull", json={"model": model})
        data = await resp.json()
        print(data)

async def GenerateText(prompt):
    async with aiohttp.ClientSession() as client:

        prompt = json.dumps(
            {
            "systemprompt":SYSTEMPROMPT.read_text(),
            "prompt":prompt
        }
        )


        async with client.post(
            OLLAMA_SERVER + "/api/generate",
            json={"model": OLLAMA_MODEL_NAME, "prompt": prompt}
        ) as resp:
            output = []
            async for line in resp.content:
                if line:
                    obj = json.loads(line.decode("utf-8"))
                    if "response" in obj:
                        print(obj["response"], end="")
                        output.append(obj["response"])
                    if obj.get("done_reason") == "stop":
                        print()
                        return "".join(output)

async def main():
    if not await IsModel(OLLAMA_MODEL_NAME):
        print(f"Uh oh. {OLLAMA_MODEL_NAME} doesn't exist. Pulling now. This may take some time...")
        await PullModel(OLLAMA_MODEL_NAME)



    try:
        while True:
            prompt = input("> ").strip()
            if not prompt:
                continue
            out = await GenerateText(prompt)

    except KeyboardInterrupt:
        print("\nExiting gracefully.")


user_histories: dict[int, collections.deque[str]] = {}

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    
    try:
        allowed_lines = {l.strip() for l in ALLOWEDCHANNELS.read_text().splitlines() if l.strip()}
    except Exception:
        allowed_lines = set()

    if str(message.channel.id) not in allowed_lines and message.channel.name not in allowed_lines:
        return
        

    print(f"[{message.author} / {message.author.display_name}]: {message.content}")

    # get or create a deque for this user
    history = user_histories.setdefault(message.author.id, collections.deque(maxlen=5))
    history.append(message.content)

    # format context nicely WHEY
    user_context = "\n".join(f"User: {msg}" for msg in history)

    full_prompt = (
        f"[User Past Messages]\n{user_context}\n\n"
        f"[New Prompt]\n{message.content}\n\n"
    )

    reply_text = await GenerateText(full_prompt)
    await message.reply(reply_text)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(token=DISCORD_TOKEN)



