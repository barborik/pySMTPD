import config


def starting():
    print("Starting pySMTPD")


def listening():
    print(f"Listening on {config.LISTEN_ADDR}:{config.LISTEN_PORT}")


def sending(mail_agent):
    print(f"Sending to {mail_agent}")


def outbound_fail(mail_agent, reply):
    print(f"Outbound mail delivery to {mail_agent} failed, remote server replied with:\n{reply}")


def outbound_success(mail_agent):
    print(f"Outbound mail delivery to {mail_agent} successful")


def outbound_received(mailbox):
    print(f"Outbound mail for {mailbox} accepted for delivery")


def inbound_received(user):
    print(f"Inbound mail for {user} delivered")


def accepted(client):
    print(f"Connection {client.address}:{client.port} accepted")


def terminated(client):
    print(f"Connection {client.address}:{client.port} terminated")


def command_issued(client):
    print(f"{client.address}:{client.port} issued command {client.buffer}")


def timeout(client):
    print(f"{client.address}:{client.port} timed out")
