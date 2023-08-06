from typing import Optional

from .base import AuthenticationBase
from .file import AuthenticationFile


class AuthenticationFactory:

    def __new__(self, style: str) -> Optional[type]:
        if style.lower() == 'file':
            return AuthenticationFile
        return None
