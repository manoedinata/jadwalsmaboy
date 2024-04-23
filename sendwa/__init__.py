from pydantic import BaseModel

# Configuration
class Config(BaseModel):
    group_id: dict
    bot_token: str
