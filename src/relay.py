import socket
import dns.resolver  # requires the dnspython package
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
    """
    Relay email in the relay queue indefinitely on a second thread.
    Unlike receiving email, sending is done one at a time.
    """

    while True:
        if not relay_queue:
            continue

        envelope = relay_queue.popleft()
        hostname = envelope.forward_path[0].split("@")[1]
        
        # determine if the host is known by a hostname or a numerical address
        if "[" in hostname:
            mx = hostname.replace("[", "").replace("]", "")
        else:
            mx = lookup_mx(hostname)

        log.sending(f"{mx}:{config.RELAY_PORT}")
        
        # connect
        relay_socket.connect((mx, int(config.RELAY_PORT)))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue
        
        # HELO command
        relay_socket.send(f"HELO {config.HOSTNAME}\r\n".encode("ascii"))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue
        
        # MAIL command
        relay_socket.send(f"MAIL FROM:<{envelope.reverse_path}>\r\n".encode("ascii"))
        if not check_reply(relay_socket.recv(512).decode("ascii")):
            relay_socket.close()
            continue
        
        # RCPT command
        for mailbox in envelope.forward_path:
            relay_socket.send(f"RCPT TO:<{mailbox}>\r\n".encode("ascii"))
            relay_socket.recv(512)
            
        # DATA command
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
