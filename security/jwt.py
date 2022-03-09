import re
from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import UUID

from jose import jwt

is_uuid = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$", re.IGNORECASE).match


class JWTController:
    def __init__(self, secret_key: str, algorithm: str, default_expiration: timedelta):
        """
        Create a JWTController client
        @param secret_key: basically a long-password (256 bits) - may depend in the algorithm used
        @param algorithm: Algorithm to be used in the JWT
        @param default_expiration: default expiration time (seconds) used in freshness (exp field)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.default_expiration = default_expiration

    def create(self, payload: dict) -> str:
        """
        Create jwt token
        @param payload: payload for token without freshness
        @return: token string
        """
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_with_freshness(self, payload: dict, expiration: timedelta = None) -> str:
        """
        Create jwt token with freshness / expire datetime
        @param payload: payload for token without freshness
        @param expiration: timedelta for freshness / expire date (default set in constructor)
        @return: token string
        """
        for name, value in payload.items():
            if isinstance(value, UUID):
                payload[name] = str(value)

        return self.create(
            {**payload, 'exp': (datetime.utcnow() + (expiration or self.default_expiration)).timestamp()})

    def parse(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def parse_if_fresh(self, token: str) -> Optional[dict[str, Any]]:
        payload = self.parse(token)

        expire_dt = payload.get('exp')
        if expire_dt and datetime.fromtimestamp(expire_dt) > datetime.utcnow():
            for name, value in payload.items():
                if isinstance(value, str) and is_uuid(value):
                    payload[name] = UUID(value)
            return payload
        return None
