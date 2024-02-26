import config
from client import Client

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


def service_ready(client: Client) -> None:
    client.send(f"220 {config.HOSTNAME} pySMTPD ready\r\n")


def service_busy(client: Client) -> None:
    client.send(f"421 {config.HOSTNAME} pySMTPD busy, try again later\r\n")


def service_terminate(client: Client) -> None:
    client.send("221 Bye\r\n")


def action_success(client: Client) -> None:
    client.send("250 Action success\r\n")


def sequence_fail(client: Client) -> None:
    client.send("503 Bad sequence of commands\r\n")


def invalid_command(client: Client) -> None:
    client.send("500 Invalid command\r\n")


def start_input(client: Client) -> None:
    client.send("354 Start mail input; end with <CRLF>.<CRLF>\r\n")


def syntax_error(client: Client) -> None:
    client.send("501 Syntax error\r\n")
