# Discord Character Bot

A simple ``ollama`` to ``Discord.py`` translator.

allowed-channels.txt denotes channels wherein the bot can talk. A newline seperates the channels.
systemprompt.txt is the system prompt. It's currently set to James McGill from Better Call Saul. [PROPERTY OF AMC]

Both are checked at runtime, so no reboot is needed for modifications. They mount directly to their respective files.

# Environment Variables

```
OLLAMA_SERVER=http://ollama:11434
DISCORD_TOKEN=Your Bot Token.
OLLAMA_MODEL_NAME=gemma3:4b 
OLLAMA_HOST="0.0.0.0"
OLLAMA_KEEP_ALIVE="-1
"
```

The only thing you should change is DISCORD_TOKEN or the model. 