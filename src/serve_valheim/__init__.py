import os
import re
from datetime import datetime
from signal import CTRL_BREAK_EVENT
from subprocess import CREATE_NEW_PROCESS_GROUP, PIPE, STDOUT, Popen
from threading import Thread

import rich

from .config import Settings

console = rich.get_console()

dt_pattern = re.compile(r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}:\s*)(.*)', re.IGNORECASE)


def proc(config: Settings) -> Popen:
    env = os.environ.copy()
    env['SteamAppId'] = (config.path / 'steam_appid.txt').read_text().strip()

    params = {
        'args': [
            str(config.path / 'valheim_server.exe'), '-nographics',
            '-batchmode', '-name', config.server, '-port',
            str(config.port), '-world', config.world, '-password',
            config.password.get_secret_value(), '-savedir',
            str(config.saves), '-public',
            str(int(config.is_community_server))],
        'stdout': PIPE,
        'stderr': STDOUT,
        'env': env,
        'text': True,
        'creationflags': CREATE_NEW_PROCESS_GROUP,
    }

    return Popen(**params)


def handle_stdout(process: Popen):
    for line in process.stdout:
        if not (line := line.strip()) or '(Filename:' in line:
            continue

        dt = datetime.utcnow()

        if m := dt_pattern.match(line):
            line = m.group(2)

        console.print(f'[{dt}] {line}')


def main():
    try:
        process = proc(Settings())
        thread = Thread(target=handle_stdout, args=(process,))
        thread.start()
        while input(): pass
    except KeyboardInterrupt:
        process.send_signal(CTRL_BREAK_EVENT)
        process.wait()
        thread.join()
