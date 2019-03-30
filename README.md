# Twitch Bot

A Twitch bot written in Python3 for use with the Yegnaro and Concealed Armies channel.

## Setup

To correctly setup TwitchBot, modify the section of files below

### TwitchBot

``` python3
# Twitch Bot Configuration
self.HOST = "irc.chat.twitch.tv"
self.PORT = 6667
self.RATE = (20/30)
self.NICK = "<Twitch Bot Name>"
self.PASS = "<Oauth Token>"
self.CHAN = "#<Twitch Account Channel>"
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
