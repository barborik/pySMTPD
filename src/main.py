import sys

import log
import config
import client
import server
import threading

from relay import relay


def main():
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(f"Usage: {sys.argv[0]} [flags] <config path> <user path>")
            exit(0)

        mail_conf = sys.argv[1]
        user_conf = sys.argv[2]
    except IndexError:
        print("ERROR: mandatory argument missing")
        exit(1)

    log.starting()
    config.load(mail_conf, user_conf)
    server.init()

    relay_thread = threading.Thread(target=relay)
    relay_thread.start()

    while True:
        client.accept()
        client.receive()


if __name__ == "__main__":
    main()
