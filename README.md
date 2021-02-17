# Valheim Dedicated Server

A simple wrapper for the `valheim_server` executable to make controlling the
configuration easier.

* [Requirements](#requirements)
* [Setup](#setup)
* [Running the Script](#running-the-script)

## Requirements

### Valheim

I hope this is a given, but it seems you can only get access to the server
software after you've purchased the game.

### PowerShell v5+

If you're on Windows 10, this is already the case.

You can confirm your version by pressing "WinKey+X" and selecting "Windows
PowerShell" from the menu:

![power-user-menu][]

Then run:

```powershell
PS C:\> $PSVersionTable.PSVersion
```

## Setup

### Install the Server

1. Enable the "Tools" filter

![steam-tools-enable][]

2. Search for the software

![steam-tools-search][]

3. Install the server

![steam-tools-install][]

4. Keep a reference to where it's installed for later

![steam-tools-find-install][]

![steam-tools-copy-path][]

### Firewall

The server requires TCP/UDP ports 2456-2458 open to accept connections. The
UAC prompt should appear when attempting to run the script for the first time
and accepting it creates inbound firewall rules named `valheim_server`. The
`Program` column should contain the full path to `valheim_server.exe`.

![firewall-rules][]

### Port Forwarding

In your router's management webpage, you should set up your PC with a static IP
address on your local network, and you should forward the ports 2456-2458 on
both TCP and UDP protocols to that static IP.

### Domain Name

If you want to host your server privately, off-list and do not want your
players to have to remember or update your public IP address constantly, I
recommend using [`NoIP`][]'s client to have a free, public domain name. Their
startup documentation is good enough, so I recommend reading it if you want to
pursue this route, but I won't be covering it in this guide.

## Running the Script

Open up PowerShell and run the following commands, replacing the placeholders
according to where you have things downloaded or installed on your local PC:

```powershell
PS C:\> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force  # enables running the script
PS C:\> Set-Location -Path "DOWNLOAD_LOCATION"
PS C:\> ./start.ps1 -Path "PATH_FROM_SETUP" -World myworld -Server myserver
```

[power-user-menu]: <./docs/power-user-menu.png>
[steam-tools-enable]: <./docs/steam-tools-enable.png>
[steam-tools-search]: <./docs/steam-tools-search.png>
[steam-tools-install]: <./docs/steam-tools-install.png>
[steam-tools-find-install]: <./docs/steam-tools-find-install.png>
[steam-tools-copy-path]: <./docs/steam-tools-copy-path.png>
[firewall-rules]: <./docs/firewall-rules.png>
[`NoIP`]: <https://www.noip.com/remote-access>
