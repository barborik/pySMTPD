import config
from client import Client


def starting():
    print("Starting pySMTPD")


def listening():
    print(f"Listening on {config.LISTEN_ADDR}:{config.LISTEN_PORT}")


def sending(mail_agent: str):
    print(f"Sending to {mail_agent}")


def outbound_fail(mail_agent: str, reply: str):
    print(
        f"Outbound mail delivery to {mail_agent} failed, remote server replied with:\n{reply}")


def outbound_success(mail_agent: str):
    print(f"Outbound mail delivery to {mail_agent} successful")


def outbound_received(mailbox: str):
    print(f"Outbound mail for {mailbox} accepted for delivery")


def inbound_received(user: str):
    print(f"Inbound mail for {user} delivered")


def accepted(client: Client):
    print(f"Connection {client.address}:{client.port} accepted")


def terminated(client: Client):
    print(f"Connection {client.address}:{client.port} terminated")


def command_issued(client: Client):
    print(f"{client.address}:{client.port} issued command {client.buffer}")


def timeout(client: Client):
    print(f"{client.address}:{client.port} timed out")
