import requests
import telegram as tel
import asyncio

data = requests.get("https://api.telegram.org/bot6264357965:AAH10GjcRl8iQ0sW1pavXDdAckvAMXE5Tpk/getUpdates").json()
async def main():
    chat_id = data['result'][0]['message']['chat']['id']
    bot = tel.Bot(token="6264357965:AAH10GjcRl8iQ0sW1pavXDdAckvAMXE5Tpk")
    await bot.send_message(chat_id=chat_id, text="hello jaejung")

asyncio.run(main())
print("halsdjfas")