__all__ = ('Settings',)

from os import getenv
from pathlib import Path

from pydantic import BaseSettings, SecretStr, conint, validator


class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        env_prefix = 'valheim_'

    # where the `valheim_server` executable lives
    path: Path = Path(getenv('ProgramFiles(x86)')) / 'Steam/steamapps/common/Valheim dedicated server'

    @validator('path')
    def executable_exists(cls, value: Path) -> Path:
        v = value / 'valheim_server.exe'
        assert v.exists(), f'could not find {v!r}'
        return value

    # where the `world/` folder lives
    saves: Path = Path(f'{getenv("LOCALAPPDATA")}Low') / 'IronGate/Valheim'

    @validator('saves')
    def saves_location_exists(cls, value: Path) -> Path:
        assert value.exists(), f'could not find {value!r}'
        return value

    # filename of the save minus extension
    world: str = 'Dedicated'
    # the name that appears in listings
    server: str
    # constrained for valid, non-reserved ports
    port: conint(ge=1 << 10, lt=1 << 16, strict=True) = 2456
    # constrained for valid passwords
    password: SecretStr

    @validator('password')
    def constrain_password(cls, value: SecretStr, values) -> SecretStr:
        v = value.get_secret_value()
        assert len(v) >= 5, 'password must be at least five characters long'
        assert v not in values['server'], 'password cannot be part of server name'
        return value

    # controls whether the server is listed in the community browser in-game
    is_community_server: bool = True
