# pySMTPD
pySMTPD is an [RFC 788](https://datatracker.ietf.org/doc/html/rfc788) compatible SMTP daemon written in Python implementing the [minimum implementation](https://www.rfc-editor.org/rfc/rfc788.html#page-35) as described by the standard.

This document serves as a user's manual, for technical reference see the [wiki](https://github.com/barborik/pySMTPD/wiki).

### Standard Compliance
As is the norm with RFC compliant software being non-compliant in one way or another, pySMTPD isn't any different.

#### missing
pySMTPD lacks the option to specify a forward path with more than one MTA in the transfer process.  
To better illustrate, here is an RFC 788 compliant forward path not supported by pySMTPD: ```<@AAA,@BBB,john@CCC>```  
pySMTPD would accept only: ```<john@CCC>``` and would send the email directly to the specified MX server (performing a DNS lookup).

This is just a remnant of the ARPANET days and on today's internet it would just give spammers a way to send (possibly malicious) emails via a chain of servers where each subsequent one would accept mail from the previous while also being more trusted in the whole network, building the trust of the email in transfer and finally reaching the victims mailbox.

#### extra
A fully RFC 788 compatible SMTP server operates only with hostnames, this again is a relic left over from ARPANET since the standard itself precedes the implementation of Internet Protocol on the network. To make the software a little more usable, I borrowed from a more modern standard so that compatibility with other SMTP server implementations is retained. As described in [RFC 5321, section 4.1.3. "Address Literals"](https://www.rfc-editor.org/rfc/rfc5321.html#section-4.1.3), an address literal is able to replace the hostname part of either the foward-path or reverse-path while enclosed by square brackets.
The address literal should be written according to its relevant standard (i. e. [RFC 4291](https://www.rfc-editor.org/rfc/rfc4291.html) for IPv6).  

In other words, ```john@[109.43.197.25]```, is a valid pySMTPD forward/reverse-path.

### Prerequisites

- Python 3 (Python 2 untested, although it might work with the right package versions)
- ```dnspython``` Pip package

### Logging
pySMTPD follows the Unix philosophy, this means that all its logging is done on the standard output. For keeping logs as files you will need to redirect the text output into a file using the ">" symbol or directly instructing the init system what to do with stdout if you're running pySMTPD as a daemon. This is shown in the example service files at the very end of this document.

### Configuration
Configuration is done through two files whose paths are passed as arguments at launch, internally these files are referred to as ```mail.conf``` and ```user.conf```. Where mail.conf is a simple key value pair listing separated by the "=" symbol and user.conf specifies all the users and their mailbox directory. All users are what other implementations would call "virtual" and are not tied in any way to users on the system itself.  

#### list of mail.conf variables
- HOSTNAME
- RELAY_PORT
- LISTEN_ADDR
- LISTEN_PORT
- MAX_CLIENTS
- CLIENT_TIMEOUT (in seconds)

minimal mail.conf:
```
HOSTNAME = myemail.com
LISTEN_ADDR = 0.0.0.0
```
Apart from setting up port forwarding and MX records (if you own a domain), this is the minimal configuration you have to do to be able to send and accept email. If you don't own a domain and want to run pySMTPD with only an IP address, you must still specify your public address enclosed in square brackets in the HOSTNAME field like so:
```
HOSTNAME = [109.43.197.25]
```

example user.conf:
```
john:/tmp/mbox/john/
jack:/tmp/mbox/jack/
```

### (Example) Installation and Usage
Since the software is not available in any package repo, to run pySMTPD as a daemon on your machine you will have to perform a manual installation. Here is a little guide that should not be followed blindly step by step, but studied and adapted to suit your needs and specifics of the system you plan to deploy pySMTPD on.

1. **Obtaining the code**  
Make /etc your working directory.  
```$ cd /etc```  
Clone the repository.  
```$ git clone https://github.com/barborik/pySMTPD.git```

2. **Configuration**  
Change the contents of the ```/etc/pySMTPD/conf/mail.conf``` and ```/etc/pySMTPD/conf/user.conf``` files to your liking.

3. **Creating a service file**  
For systems running systemd as their init system, create a file named ```pySMTPD.service``` inside ```/etc/systemd/system``` and save the following inside.
```
[Unit]
Description=SMTP daemon

[Service]
WorkingDirectory=/etc/pySMTPD
ExecStart=python src/main.py conf/mail.conf conf/user.conf
StandardOutput=file:/var/mail.log
```

4. **Running**  
Finally, simply tell your init system to start the service.  
```$ systemctl start pySMTPD```
