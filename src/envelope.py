import config
from relay import relay_queue
from relay import relay


class Envelope:
    def process(self):
        for mailbox in self.forward_path:
            # parse user
            user = mailbox.split("@")[0]

            # verify user exists on the local instance
            if user in config.USER_LIST:
                self.store(user)
            # if not, relay the mail
            else:
                relay_queue.append(self)
                relay()

    def store(self, user):
        file = open(config.USER_LIST[user] + "mail.txt", "w")
        file.write(self.data)
        file.close()

    def __init__(self):
        self.reverse_path = None
        self.forward_path = []
        self.data = str()
