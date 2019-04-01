from datetime import datetime
from dotenv import load_dotenv
import json
import logging
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
        self.PREFIX = os.getenv("TTV_CMD_PREFIX")

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

                # self.message = self.message.replace("\r\n", "")

                logging.info("{}: {}".format(self.username, self.message))

                with open("Commands.json") as cmd_file:

                    self.commands = json.load(cmd_file)

                    for self.command in self.commands:

                        if self.PREFIX + self.command in self.message.split():

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


try:

    # Logging Setup
    logging.basicConfig(
        filename="logs/{} - Twitch Chat.log".format(
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        ),
        format='%(asctime)s -- %(message)s',
        datefmt='%Y-%M-%d %H:%M:%S',
        level=logging.INFO
    )

    # Starts the Bot
    TwitchBot().__init__()

except KeyboardInterrupt:

    # Need to log
    logging.info("Script closed by user.")
