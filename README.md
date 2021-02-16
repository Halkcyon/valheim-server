# Valheim Dedicated Server

A simple wrapper for the `valheim_server` executable to make controlling the
configuration easier.

## Setup

### Firewall

The server requires TCP/UDP ports 2456-2458 open and forwarded to operate. The
UAC prompt should appear when attempting to launch the server and accepting it
creates inbound firewall rules named `valheim_server`. The `Program` column
should contain the `valheim_server.exe` path.

![firewall-rules][]

### Port Forwarding

In your router's management page, you should set up your PC with a static IP
address on your local network, and you should forward the ports 2456, 2457 and
2458 on both TCP and UDP protocols to that static IP.

### Domain Name

If you want to host your server privately, off-list and do not want your
players to have to remember or update your public IP address constantly, I
recommend using [`NoIP`][]'s client to have a free, public domain name. Their
startup documentation is good enough, so I recommend reading it if you want to
pursue that route.

[firewall-rules]: <./docs/firewall-rules.png>
[`NoIP`]: <https://www.noip.com/>
