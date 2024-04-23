import httpx

FONTE_WHATSAPP_SEND_API = "https://api.fonnte.com/send"

class FonnteAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        # Send the request, with `Authorization` header.
        request.headers["Authorization"] = self.token
        yield request

async def sendMessage(message: str, number: str, bot_token: str, url: str = FONTE_WHATSAPP_SEND_API):
    auth = FonnteAuth(bot_token)
    async with httpx.AsyncClient() as client:
        req = await client.post(url, auth=auth, json={
            "target": number,
            "message": message,
            "typing": True
        })
        return req.json()
