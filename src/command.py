import log
import reply
from state import State
from envelope import Envelope


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

    reverse_path = str()
    if "<>" not in client.buffer:
        reverse_path = client.buffer.split("<")[1].split(">")[0]
    client.buffer = str()

    client.envelope = Envelope()
    client.envelope.reverse_path = reverse_path

    reply.action_success(client)


def rcpt(client):
    if client.envelope.reverse_path is None:
        reply.sequence_fail(client)
        return

    forward_path = client.buffer.split("<")[1].split(">")[0]
    client.envelope.forward_path.append(forward_path)
    client.buffer = str()

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
