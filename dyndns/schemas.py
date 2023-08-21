from pydantic import BaseModel, SecretStr, TypeAdapter


class DynDns(BaseModel):
    username: SecretStr
    password: SecretStr


DynDnsDict = TypeAdapter(dict[str, DynDns])
