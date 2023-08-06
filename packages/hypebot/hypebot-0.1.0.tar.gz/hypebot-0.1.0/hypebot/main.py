import argparse
import errno
import getpass
import socket
import time

from hypebot import log
from hypebot.net import LiveSplitClient
from hypebot.twitter import create_twitter_api


LOGGER = log.create_logger(__name__)


def update(livesplit_client, twitter, last_split_index, name, target_split_index):
    """ Update loop. Returns current world index. """
    current_split_index = int(livesplit_client.post("getsplitindex"))
    if last_split_index != current_split_index:
        LOGGER.info("Split index changed to %d", current_split_index)
    if last_split_index < target_split_index and current_split_index == target_split_index:
        delta = livesplit_client.post("getdelta")
        pb_pace = "−" in delta
        LOGGER.info("Split delta: %s", delta)
        if pb_pace:
            twitter.PostUpdate(f"{name} on p.b. pace with delta {delta}")
    return current_split_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help=f"Your name in tweets, e.g. {getpass.getuser()}")
    parser.add_argument("split_index", help="Split index against which we compare delta, e.g. 7", type=int)
    args = parser.parse_args()
    twitter = create_twitter_api()
    last_split_index = -1
    livesplit_client = LiveSplitClient()
    LOGGER.info("Connected and ready for updates...")
    while True:
        try:
            last_split_index = update(livesplit_client, twitter, last_split_index, args.name, args.split_index)
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                LOGGER.info("Socket connection reset, attempting to reconnect")
                livesplit_client.connect()
        time.sleep(1)


if __name__ == "__main__":
    main()
