import dataclasses


@dataclasses.dataclass(frozen=True)
class RedisTemplates:
    auth_register_otp: str = "auth:register:otp:{cellphone}"
    auth_login_token: str = "auth:login:token:{cellphone}"
    auth_register_token: str = "auth:register:token:{token}"
    auth_register_information: str = "auth:register:information:{token}"

    @classmethod
    def format_auth_register_otp(cls, cellphone: str) -> str:
        return cls.auth_register_otp.format(cellphone=cellphone)

    @classmethod
    def format_auth_register_token(cls, token: str) -> str:
        return cls.auth_register_token.format(token=token)

    @classmethod
    def format_auth_login_token(cls, cellphone: str) -> str:
        return cls.auth_login_token.format(cellphone=cellphone)

    @classmethod
    def format_auth_register_information(cls, token: str) -> str:
        return cls.auth_register_information.format(token=token)
