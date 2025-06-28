from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.table import Table
import asyncio
import os

class TerminalUI:
    def __init__(self, config):
        self.config = config
        self.console = Console()
        self.layout = Layout(name="root")
        self.status_text = Text("Inicializando...", style="bold green")
        self.balance_text = Text("Saldo: Carregando...", style="bold blue")
        self.positions_table = Table(title="Posições Abertas")
        self.signals_log = Text("Últimos Sinais:\n", style="dim")
        self.logs_panel = Text("Logs:\n", style="dim")
        self.command_input = Text("Comando: ", style="bold yellow")

        self._setup_layout()

    def _setup_layout(self):
        terminal_width = self.console.width

        if terminal_width < 80: # Modo compacto para telas pequenas (celular)
            self.layout.split(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )
            self.layout["main"].split(
                Layout(Panel(self.balance_text, title="Conta"), name="balance_info"),
                Layout(Panel(self.positions_table, title="Posições"), name="positions"),
                Layout(Panel(self.signals_log, title="Sinais"), name="signals"),
                Layout(Panel(self.logs_panel, title="Logs"), name="logs"),
            )
        else: # Modo desktop
            self.layout.split(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )
            self.layout["main"].split_row(
                Layout(name="left_panel"),
                Layout(name="right_panel")
            )
            self.layout["left_panel"].split(
                Layout(Panel(self.balance_text, title="Informações da Conta"), name="balance_info"),
                Layout(Panel(self.positions_table, title="Posições"), name="positions"),
            )
            self.layout["right_panel"].split(
                Layout(Panel(self.signals_log, title="Sinais Recentes"), name="signals"),
                Layout(Panel(self.logs_panel, title="Logs do Sistema"), name="logs"),
            )
        self.layout["header"].update(Panel(Text("Crypto Signal Bot", justify="center", style="bold magenta"), title="Status"))
        self.layout["footer"].update(Panel(self.command_input, title="Comandos"))

        self.positions_table.add_column("Par")
        self.positions_table.add_column("Tipo")
        self.positions_table.add_column("Entrada")
        self.positions_table.add_column("Quantidade")
        self.positions_table.add_column("PNL")

    def update_panel(self, data):
        # Atualiza o painel visual com os dados recebidos
        if isinstance(data, str):
            self.logs_panel.append(f"{data}\n")
        elif isinstance(data, dict):
            if "status" in data:
                self.status_text.plain = data["status"]
            if "balance" in data:
                self.balance_text.plain = f"Saldo: {data["balance"]:.2f} USDT"
            if "new_signal" in data:
                self.signals_log.append(f"{data["new_signal"]}\n")
            if "positions" in data:
                self.positions_table.rows = [] # Limpa e adiciona novamente
                for pos in data["positions"]:
                    self.positions_table.add_row(pos["symbol"], pos["type"], str(pos["entry_price"]), str(pos["amount"]), str(pos["pnl"])) # Exemplo

    async def run(self, listener, executor):
        self.executor = executor # Armazena o executor para uso nos comandos
        with Live(self.layout, screen=True, refresh_per_second=4) as live:
            self.update_panel({"status": "Conectando ao Telegram..."})
            # Inicia o listener do Telegram em uma tarefa separada
            asyncio.create_task(listener.start_listening())

            # Loop principal para manter a UI ativa e processar comandos
            while True:
                # Implementar a leitura de comandos manuais interativos
                # Usando input() bloqueia a UI, para uma solução não bloqueante, textual seria melhor integrado
                # Por simplicidade, usaremos um input() simples por enquanto, mas em um ambiente real, textual.App seria o ideal.
                # Para este exemplo, o input será simulado ou feito fora do loop Live para não bloquear.
                # Uma solução mais robusta com textual.App seria:
                # app = MyApp(listener, executor)
                # await app.run()
                await asyncio.sleep(1) # Atualiza a cada segundo

    def get_command(self):
        # Placeholder para entrada de comando manual
        # Em um ambiente real com textual, isso seria tratado por um widget de input
        return self.console.input("[bold yellow]Comando: [/bold yellow]")

    async def process_command(self, command):
        # Chamar métodos do executor com base no comando
        if command.startswith("/fechar"):
            parts = command.split(" ")
            if len(parts) > 1:
                symbol = parts[1]
                await self.executor.close_position(symbol, "binance") # Exemplo
                self.update_panel(f"Comando: Fechar {symbol}")
        elif command.startswith("/trocar"):
            parts = command.split(" ")
            if len(parts) > 1:
                dex_name = parts[1]
                await self.executor.switch_dex(dex_name) # Exemplo
                self.update_panel(f"Comando: Trocar para {dex_name}")
        else:
            self.update_panel(f"Comando desconhecido: {command}")



