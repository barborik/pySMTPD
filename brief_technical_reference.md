pySMTPD is structured into ten key modules, here is a brief overview of each of them.

### 01. main.py

This is the entry point of the program. Firstly, it checks command line arguments, loads up the configuration files and starts the main loop for sending and receiving mail, which are done on separate threads.

### 02. server.py

The core of the SMTP daemon, implementing its logic, including listening for connections, processing incoming messages, and managing sessions.

### 03. client.py

Defines a structure for "low-level" connection management, handling data transmission one ASCII character at a time.

### 04. envelope.py

Handles the construction and management of email envelopes, encapsulating sender and recipient information, as well as the message content.

### 05. relay.py

Manages the relaying of emails to their destination MX servers. Includes functionalities for DNS lookup to find MX records.

### 06. config.py

Manages configuration settings for the SMTP daemon, including server parameters and virtual users.

### 07. command.py

Defines the SMTP command parser and handler, interpreting SMTP commands received from clients and passing them to their according handling routines.

### 08. reply.py

Ensures that clients receive appropriate feedback for their commands according to the SMTP protocol.
Defines a set of possible replies to clients, including standard status codes and messages.

### 09. log.py

Handles logging functionalities for the daemon, providing a way to record events, errors and other messages to make debugging easier and monitor its operation.

### 10. state.py

Defines three possible states of a transaction: UNIDENTIFIED (no commands, identify with HELO), IDENTIFIED (all commands available), DATA (received lines not treated as commands).














