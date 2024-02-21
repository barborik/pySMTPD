import log
import reply
import re
from state import State
from envelope import Envelope
from server import client_pool


email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


def exec_command(client):
    """
    Identifies the command and passes it to the relevant function.
    """

    if client.state == State.DATA:
        client.recv_data()
        return
    else:
        log.command_issued(client)

    if re.match(r"^HELO \S+[\r\n]$", client.buffer):
        helo(client)
        return

    if re.match(r"^MAIL FROM:<(\S|)+>[\r\n]$", client.buffer):
        mail(client)
        return

    if re.match(r"^RCPT TO:<\S+>[\r\n]$", client.buffer):
        rcpt(client)
        return

    if re.match(r"^DATA[\r\n]$", client.buffer):
        data(client)
        return

    if re.match(r"^RSET[\r\n]$", client.buffer):
        rset(client)
        return

    if re.match(r"^NOOP[\r\n]$", client.buffer):
        noop(client)
        return

    if re.match(r"^QUIT[\r\n]$", client.buffer):
        quit(client, client_pool)
        return

    reply.invalid_command(client)
    client.buffer = str()


def helo(client):
    client.hostname = client.buffer.split(" ")[1].strip()
    client.buffer = str()

    if client.state != State.UNIDENTIFIED:
        reply.sequence_fail(client)
        return

    client.state = State.IDENTIFIED
    reply.action_success(client)


def mail(client):
    if client.state != State.IDENTIFIED or client.envelope:
        reply.sequence_fail(client)
        return

    if "<>" in client.buffer:
        reverse_path = str()
    elif "<" in client.buffer and ">" in client.buffer:
        reverse_path = client.buffer.split("<")[1].split(">")[0]
        client.buffer = str()
    else:
        reply.syntax_error(client)
        client.buffer = str()
        return
    
    tmp = reverse_path.replace("[", "").replace("]", "")
    if not re.match(email_regex, tmp):
        reply.syntax_error(client)
        return

    client.envelope = Envelope()
    client.envelope.reverse_path = reverse_path

    reply.action_success(client)


def rcpt(client):
    if client.envelope.reverse_path is None:
        reply.sequence_fail(client)
        return

    if "<>" not in client.buffer and "<" in client.buffer and ">" in client.buffer:
        forward_path = client.buffer.split("<")[1].split(">")[0]
        client.buffer = str()
    else:
        reply.syntax_error(client)
        client.buffer = str()
        return
    
    tmp = forward_path.replace("[", "").replace("]", "")
    if not re.match(email_regex, tmp):
        reply.syntax_error(client)
        return

    client.envelope.forward_path.append(forward_path)

    reply.action_success(client)


def data(client):
    if len(client.envelope.forward_path) == 0:
        reply.sequence_fail(client)
        return

    client.buffer = str()
    client.state = State.DATA
    reply.start_input(client)


def rset(client):
    client.buffer = str()

    if client.state == State.UNIDENTIFIED:
        reply.sequence_fail(client)
        return

    client.state = State.IDENTIFIED
    client.envelope = None
    reply.action_success(client)


def noop(client):
    reply.action_success(client)


def quit(client, client_pool):
    log.terminated(client)
    reply.service_terminate(client)
    client_pool.remove(client)
