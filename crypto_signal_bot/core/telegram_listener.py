from telethon import TelegramClient, events
import asyncio
from utils.data_manager import DataManager

class TelegramListener:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui
        self.client = TelegramClient("anon", config["telegram_api_id"], config["telegram_api_hash"])
        self.on_new_signal = None # Callback para o executor
        self.data_manager = DataManager()

    async def start_listening(self):
        await self.client.start()
        self.ui.update_panel("Conectado ao Telegram.")

        @self.client.on(events.NewMessage(chats=self.config["telegram_channels"])) 
        async def handler(event):
            await self.process_message(event.message)

        print("Listening for new messages...")
        await self.client.run_until_disconnected()

    async def process_message(self, message):
        content = message.text

        author = None
        if message.peer_id:
            if hasattr(message.peer_id, 'user_id'):
                author = message.peer_id.user_id
            elif hasattr(message.peer_id, 'channel_id'):
                author = message.peer_id.channel_id
            elif hasattr(message.peer_id, 'chat_id'):
                author = message.peer_id.chat_id

        timestamp = message.date.isoformat() if message.date else None

        attachments = []
        if message.media:
            attachments.append(str(message.media))

        signal_data = {
            "timestamp": timestamp,
            "author": author,
            "content": content,
            "message_type": "text", 
            "signal_id": message.id,
            "attachments": ", ".join(attachments) # Convertendo lista para string para CSV
        }

        self.data_manager.save_signal(signal_data)
        self.ui.update_panel({"new_signal": f"Sinal: {signal_data["content"][:50]}..."})

        if self.on_new_signal:
            self.on_new_signal(signal_data)



