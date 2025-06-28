import asyncio
from core.telegram_listener import TelegramListener
from core.order_executor import OrderExecutor
from core.terminal_ui import TerminalUI
from utils.config_loader import load_config


async def main():
    config = load_config()
    ui = TerminalUI(config)
    listener = TelegramListener(config, ui)
    executor = OrderExecutor(config, ui)

    # Encadeia sinais recebidos com a execução
    listener.on_new_signal = executor.process_signal
    executor.on_order_update = ui.update_panel

    await ui.run(listener, executor)

if __name__ == "__main__":
    asyncio.run(main())
    
