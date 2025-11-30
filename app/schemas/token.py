from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" # ตามมาตรฐาน OAuth2 มักจะเป็น "bearer"

# สำหรับโครงสร้างข้อมูลของ Token ที่เก็บใน JWT Payload
class TokenData(BaseModel):
    username: str | None = None