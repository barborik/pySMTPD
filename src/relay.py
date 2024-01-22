import socket
import dns.resolver  # dnspython
from collections import deque

import log
import config

relay_queue = deque()
relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def lookup_mx(domain):
    record = dns.resolver.resolve(domain, "MX")[0].to_text()
    return record.split(" ")[1]


def check_reply(reply):
    code = reply.split(" ")[0]

    if code[0] == "2" or code[0] == "3":
        return True

    return False


def relay():
    while True:
        if not relay_queue:
            continue

        envelope = relay_queue.popleft()
        address = envelope.forward_path[0].split("@")[1]

        split = address.split(":")
        if len(split) > 1:
            address = split[0]
            port = int(split[1])
        else:
            port = 25

        try:  # validate an ip address
            socket.inet_aton(address)
            mx = address
        except socket.error:
            mx = lookup_mx(address)

        log.sending(f"{mx}:{port}")

        relay_socket.connect((mx, port))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue

        relay_socket.send(f"HELO {config.HOSTNAME}\r\n".encode("ascii"))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue

        relay_socket.send(f"MAIL FROM:<{envelope.reverse_path}>\r\n".encode("ascii"))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue

        for mailbox in envelope.forward_path:
            relay_socket.send(f"RCPT TO:<{mailbox}>\r\n".encode("ascii"))
            relay_socket.recv(512)

        relay_socket.send(f"DATA\r\n".encode("ascii"))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue

        relay_socket.send(envelope.data.encode("ascii"))
        relay_socket.send("\r\n.\r\n".encode("ascii"))

        if check_reply(reply := relay_socket.recv(512).decode("ascii")):
            log.outbound_success(mx)
        else:
            log.outbound_fail(mx, reply)
