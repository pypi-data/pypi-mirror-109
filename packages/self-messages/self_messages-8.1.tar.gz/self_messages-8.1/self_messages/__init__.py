class self_messages:
    def __init__(self, token: str):
            import requests
            self.token = token
            self.requests = requests 
    def get(self, channel_id: int, message_id: int):
        
        url = f"https://discord.com/api/v9/channels/{str(channel_id)}/messages?limit=50"
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9002 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
            'authorization': self.token
        }
        data = self.requests.get(url, headers=headers).json()
        for item in data:
            if item['id'] == str(message_id):
                return item['content']
        return None