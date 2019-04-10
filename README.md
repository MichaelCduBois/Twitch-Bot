# Twitch Bot

A Twitch bot written in Python3 for use with the Yegnaro and Concealed Armies channel.

## Setup

To correctly setup TwitchBot, modify the files below

### .env-example

1. Rename `.env-example` to `.env`

``` environment
# Environment Specifics
TTV_HOST = "irc.chat.twitch.tv"
TTV_PORT = 6667
TTV_USERNAME = ""
TTV_TOKEN = ""
TTV_CHANNEL = "#"
TTV_CMD_PREFIX = "!"
```

### Commands.json

``` json
{
    "command1": "text1",
    "command2": "text2",
    "command3": "text3"
}
```

### Commands.json Variables

Variable | Output
-------- | ------
`<username>` | User that sent command

## Usage

### Standalone

``` python3
python3 TwitchBot.py
```

### Python Import

``` python3
from TwitchBot import TwitchBot
```
