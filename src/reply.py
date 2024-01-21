import config

"""

Action outcome:
---------------
2yz - Success
3yz - Accepted, waiting for more information
4yz - Temporary failure
5yz - Permanent failure

Reply category:
---------------
x0z - Syntax
x2z - Connection
x5z - Mail system
 
"""


def service_ready(client):
    client.send(f"220 {config.HOSTNAME} pySMTPD ready\r\n")


def service_busy(client):
    client.send(f"421 {config.HOSTNAME} pySMTPD busy, try again later\r\n")


def service_terminate(client):
    client.send("221 Bye\r\n")


def action_success(client):
    client.send("250 Action success\r\n")


def sequence_fail(client):
    client.send("503 Bad sequence of commands\r\n")


def invalid_command(client):
    client.send("500 Invalid command\r\n")


def start_input(client):
    client.send("354 Start mail input; end with <CRLF>.<CRLF>\r\n")
