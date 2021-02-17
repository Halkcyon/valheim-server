#requires -Version 5

[CmdletBinding()]
param(
    [Parameter(HelpMessage = 'Path to the `valheim_server` executable')]
    [Alias('ValheimPath')]
    [System.IO.DirectoryInfo]
    $Path = "${Env:ProgramFiles(x86)}\Steam\steamapps\common\Valheim dedicated server",

    [Parameter(HelpMessage = 'Name of the savefile minus its extension')]
    [string]
    $World = 'MyWorld',

    [Parameter(HelpMessage = 'Name of the server displayed in lists')]
    [Alias('ServerName')]
    [string]
    $Name = 'COMM_SERVER_1',

    [Parameter(HelpMessage = 'Determines whether the server is visible in the community list')]
    [bool]
    $IsCommunityServer = $true,

    [Parameter(DontShow, HelpMessage = 'Port the game server binds to. Recommends forwarding 2456-2458')]
    [uint16]
    $Port = 2456
)
$script:ErrorActionPreference = 'Stop'

if (-not $Path.Exists) {
    throw "Cannot find path ``${Path}``!"
}

$valheimServer = $Path | Get-ChildItem -Filter valheim_server.exe | Select-Object -First 1
if (-not $valheimServer) {
    throw "Cannot find ``valheim_server.exe`` in ``${Path}``!"
}

$password = $Env:VALHEIM_SERVER_PWD
if (-not $password) {
    # an ugly hack to mask the password at the console for pwsh <v6
    $password = [pscredential]::new(
        'TMP', (Read-Host -AsSecureString -Prompt 'Valheim Dedicated Server Password')
    ).GetNetworkCredential().Password
}
else {
    'Retrieved server password from `VALHEIM_SERVER_PWD` environment variable.'
}

if ($Name.ToLower().Contains($password.ToLower())) {
    throw 'Password cannot be a part of the server name!'
}
if ($password.Length -lt 5) {
    throw 'Password must be longer than four characters!'
}

# unsure if this is needed, but it was configured in the template script
$Env:SteamAppId = Get-Content -LiteralPath "${Path}\steam_appid.txt"

"Starting server; press CTRL-C to exit.`n"

# TODO! backup and rotate savefiles. the existing server impl only saves hourly or on shutdown

$valheimParms = @(
    '-nographics'
    '-batchmode'
    '-name', $Name
    '-port', $Port
    '-world', $World
    '-password', $password
    # path to the `worlds/` folder
    '-savedir', $PSScriptRoot
    '-public', [int]$IsCommunityServer
)
& $valheimServer.FullName @valheimParms
