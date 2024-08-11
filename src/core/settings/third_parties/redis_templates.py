import dataclasses


@dataclasses.dataclass(frozen=True)
class RedisKeyTemplates:
    AUTH_REGISTER_OTP: str = "auth:register:otp:{cellphone}"
    AUTH_LOGIN_TOKEN: str = "auth:login:token:{cellphone}"
    AUTH_REGISTER_TOKEN: str = "auth:register:token:{token}"
    AUTH_REGISTER_INFORMATION: str = "auth:register:information:{token}"
    AUTH_LOGIN_ATTEMPTS: str = "auth:login:attempts:{identifier}"
    AUTH_REGISTER_ATTEMPTS: str = "auth:register:attempts:{identifier}"
    RATE_LIMITER: str = "rate_limiter:{key}:block"

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
    def format_register_information_key(cls, token: str) -> str:
        return cls.AUTH_REGISTER_INFORMATION.format(token=token)

    @classmethod
    def format_login_attempts_key(cls, identifier: str) -> str:
        return cls.AUTH_LOGIN_ATTEMPTS.format(identifier=identifier)

    @classmethod
    def format_register_attempts_key(cls, identifier: str) -> str:
        return cls.AUTH_REGISTER_ATTEMPTS.format(identifier=identifier)

    @classmethod
    def format_rate_limiter_key(cls, key: str) -> str:
        return cls.RATE_LIMITER.format(key=key)
