import json
import re
import socket
from time import sleep


class TwitchBot:

    def __init__(self):

        # Twitch Bot Configuration
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.RATE = (20/30)
        self.NICK = ""
        self.PASS = ""
        self.CHAN = "#"

        # Socket Connection
        self.socket = socket.socket()
        self.socket.connect((self.HOST, self.PORT))
        self.socket.send("PASS {}\r\n".format(self.PASS).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
        self.socket.send("JOIN {}\r\n".format(self.CHAN).encode("utf-8"))

        # Chat Message REGEX
        self.MSG = re.compile(
            r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"
        )

        # Main Bot Loop
        while True:

            self.response = self.socket.recv(1024).decode("utf-8")

            if self.response == "PING :tmi.twitch.tv\r\n":

                self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            else:

                self.username = re.search(r"\w+", self.response).group(0)

                self.message = self.MSG.sub("", self.response)

                # Need to log
                print("{}: {}".format(self.username, self.message))

                with open("Commands.json") as cmd_file:

                    self.commands = json.load(cmd_file)

                    for self.command in self.commands:

                        if re.match("!" + self.command + r"\b", self.message):

                            self.validate()

                            break

            sleep(1 / self.RATE)

    def send(self, msg):
        """
        Send a chat message to the server.
        Keyword arguments:
        msg  -- the message to be sent
        """
        self.socket.send(
            "PRIVMSG {} :{}".format(
                self.CHAN, msg
            ).encode(
                "utf-8"
            )
        )

    def validate(self):

        """
        Retrieves the configured value for the command.
        """
        if "<username>" in self.commands[self.command]:

            self.send(
                "{}\r\n".format(
                    self.commands[self.command].replace(
                        "<username>", self.username
                    )
                )
            )

        else:

            self.send(
                "{}\r\n".format(
                    self.commands[self.command]
                )
            )

TwitchBot().__init__()
