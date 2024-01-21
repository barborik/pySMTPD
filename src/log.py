import config


def starting():
    print("Starting pySMTPD")


def listening():
    print(f"Listening on {config.LISTEN_ADDR}:{config.LISTEN_PORT}")


def accepted(client):
    print(f"Connection {client.address}:{client.port} accepted")


def terminated(client):
    print(f"Connection {client.address}:{client.port} terminated")


def command_issued(client):
    print(f"{client.address}:{client.port} issued command {client.buffer}")


def timeout(client):
    print(f"{client.address}:{client.port} timed out")
