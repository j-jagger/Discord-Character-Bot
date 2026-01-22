# Discord Ollama Adapter

### By Joe Jagger. Made for the r/okbuddychicanery discord server.

> **"Have some more chicken. Have some more pie. 
> It doesn't matter if it's boiled or fried.**
>
> — _Chuck 'Chicanery' McGill_


'Discord Character Bot' because it was created to imitate a character as a joke.

In practice, this is a Discord <-> Ollama connector with surprising functionality.

allowed-channels.txt denotes channels wherein the bot can talk. A newline seperates the channels.
systemprompt.txt is the system prompt. It's currently set to James McGill from Better Call Saul. [PROPERTY OF AMC]

Both are checked at runtime, so no reboot is needed for modifications. They mount directly to their respective files.

# Environment Variables

```
OLLAMA_SERVER=http://ollama:11434
DISCORD_TOKEN=Your Bot Token.
OLLAMA_MODEL_NAME=gemma3:4b
OLLAMA_HOST="0.0.0.0"
OLLAMA_KEEP_ALIVE="-1"
```

The only thing you should change is DISCORD_TOKEN or the model.

# Deployment

> **"Waltuh, you're gonna need Docker installed for this, Waltuh.  
> I'm not running Ollama on my host unless I'm stupid, Waltuh.  
> Containerization is the future, Waltuh."**
>
> — _Mike 'Pimento' Ehrmantraut_

DCB is designed to be deployed with Docker. It is by far
the easiest way to set it up and have it running reliably.
You could run it on a host without docker, but you'd need to
uncomment `load_dotenv()` at the top of `main.py` to make it load the envfile correctly, and also run ollama seperately.

## Docker

Paste the following into your CLI.

```bash
git clone https://github.com/j-jagger/discord-character-bot
cd discord-character-bot
```

then:

```bash
nano .env
```

(doesn't have to be nano. Use Vim or eMacs if you're deranged.)

fill the env file from the top out, then run

```bash
docker compose up -d --build
```

and it should run!
