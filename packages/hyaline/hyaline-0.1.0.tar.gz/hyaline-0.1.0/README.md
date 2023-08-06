# Hyaline Discord API Wrapper.

**WARNING**: Hyaline is not easy to use library.

Hyaline is a discord api wrapper for python. hyaline is created for discord developers and hyaline makes everything harder. _Its in alpha-release and still not finished._

Check `./docs` folder for documentation and more informations about hyaline. Documentation is not finished. You can use python `dir()` function for get all functions, attrs in the object. Also use `help()` for get help about a function / class.

**Current Version** - 0.1.0
## Change Log:
- Added PyPi Support!

## Example Ping-Pong Discord Bot

```py
# Import the library and intent helper.
import hyaline
from hyaline.helpers.Intents import ALL

# Setup session configurations.
# NOTE: If you want to limit message cache add MAX_MESSAGES
session = hyaline.Session({
    "TOKEN": "token",
    "INTENTS": ALL
})


async def on_ready(_packet):
    print(f"Bot Started with name: {session.client.username}.")


async def on_message(msg):
    if not msg.author.id == session.client.id and msg.content.lower() == "ping":
        await msg.reply({
            "content": ":ping_pong: Pong!"
        })

# Configure the events.
# Also you can configure multiple event.
session.event("MESSAGE_CREATE", on_message)
session.event("READY", on_ready)

# Start the session.
session.start()
```
