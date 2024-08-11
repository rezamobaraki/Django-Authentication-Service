import dataclasses


@dataclasses.dataclass(frozen=True)
class RedisKeyTemplates:
    AUTH_REGISTER_OTP: str = "auth:register:otp:{cellphone}"
    AUTH_LOGIN_TOKEN: str = "auth:login:token:{cellphone}"
    AUTH_REGISTER_TOKEN: str = "auth:register:token:{token}"
    MIDDLEWARE_RATE_LIMITER: str = "middleware:rate_limiter:{key}:block"
    RATE_LIMITER_SERVICE_ATTEMPTS: str = "rate_limiter:attempts:{identifier}"
    RATE_LIMITER_SERVICE_USER_BLOCK: str = "rate_limiter:user:block:{identifier}"

    @classmethod
    def format_register_otp_key(cls, cellphone: str) -> str:
        return cls.AUTH_REGISTER_OTP.format(cellphone=cellphone)

    @classmethod
    def format_register_token_key(cls, token: str) -> str:
        return cls.AUTH_REGISTER_TOKEN.format(token=token)

    @classmethod
    def format_login_token_key(cls, cellphone: str) -> str:
        return cls.AUTH_LOGIN_TOKEN.format(cellphone=cellphone)

    @classmethod
    def format_attempts_key(cls, identifier: str) -> str:
        return cls.RATE_LIMITER_SERVICE_ATTEMPTS.format(identifier=identifier)

    @classmethod
    def format_user_block_key(cls, identifier: str) -> str:
        return cls.RATE_LIMITER_SERVICE_USER_BLOCK.format(identifier=identifier)

    @classmethod
    def format_rate_limiter_key(cls, key: str) -> str:
        return cls.MIDDLEWARE_RATE_LIMITER.format(key=key)
