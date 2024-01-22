import log
import config
import client
import server
import threading

from relay import relay


from hashlib import sha256

def main():
    log.starting()
    config.load()
    server.init()

    relay_thread = threading.Thread(target=relay)
    relay_thread.start()

    while True:
        client.accept()
        client.receive()


if __name__ == "__main__":
    main()
