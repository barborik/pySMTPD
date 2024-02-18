from hashlib import sha256

import log
import config
from relay import relay_queue


class Envelope:

    def process(self):
        relay = False

        for mailbox in self.forward_path.copy():
            split = mailbox.split("@")
            user = split[0]

            # parse hostname
            if len(split) > 1:
                hostname = split[1]
            else:
                hostname = config.HOSTNAME

            # check if the mail is meant for the local machine
            if hostname == config.HOSTNAME:
                if user in config.USER_LIST:
                    log.inbound_received(user)
                    self.store(user)
                    self.forward_path.remove(mailbox)
                else:
                    # send delivery status
                    pass
            # if not, relay the mail
            else:
                relay = True

        if relay:
            log.outbound_received(mailbox)
            relay_queue.append(self)

    def store(self, user):
        filename = sha256(self.data.encode("ascii")).hexdigest()
        file = open(config.USER_LIST[user] + filename, "w")
        file.write(self.data)
        file.close()

    def __init__(self):
        self.reverse_path = None
        self.forward_path = []
        self.data = str()
