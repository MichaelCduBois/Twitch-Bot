from datetime import datetime
from dotenv import load_dotenv
import json
import os
import re
import socket
from time import sleep


class TwitchBot:

    def __init__(self):

        # Load .env file
        load_dotenv()

        # Twitch Bot Configuration
        self.HOST = os.getenv("TTV_HOST")
        self.PORT = int(os.getenv("TTV_PORT"))
        self.RATE = (20/30)
        self.NICK = os.getenv("TTV_USERNAME")
        self.PASS = os.getenv("TTV_TOKEN")
        self.CHAN = os.getenv("TTV_CHANNEL")

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
                self.log("{}: {}".format(self.username, self.message))

                with open("Commands.json") as cmd_file:

                    self.commands = json.load(cmd_file)

                    for self.command in self.commands:

                        if "!" + self.command in self.message.split():

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

    def log(self, msg):
        """
        Sends chat message to log.
        Keyword arguments:
        msg - the message to send to log
        """
        print(
            "{} -- {}".format(
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                msg
            )
        )


TwitchBot().__init__()
