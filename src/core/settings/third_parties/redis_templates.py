import dataclasses


@dataclasses.dataclass(frozen=True)
class RedisTemplates:
    auth_signup_otp: str = "auth:signup:otp:{cellphone}"
    auth_signup_token: str = "auth:signup:token:{cellphone}"
    auth_login_token: str = "auth:login:token:{cellphone}"

    def format_auth_signup_otp(self, cellphone: str) -> str:
        return self.auth_signup_otp.format(cellphone=cellphone)

    def format_auth_login_token(self, cellphone: str) -> str:
        return self.auth_login_token.format(cellphone=cellphone)

    def format_auth_signup_token(self, cellphone: str) -> str:
        return self.auth_signup_token.format(cellphone=cellphone)


redis_templates = RedisTemplates()
