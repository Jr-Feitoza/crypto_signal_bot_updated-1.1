import ccxt
import asyncio
from utils.data_manager import DataManager

class OrderExecutor:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui
        self.exchanges = {}
        self.on_order_update = None # Callback para a UI
        self.data_manager = DataManager()
        self._load_exchanges()

    def _load_exchanges(self):
        # Carregar credenciais das exchanges de forma segura
        # Exemplo básico para Binance
        if "binance_api_key" in self.config and "binance_api_secret" in self.config:
            self.exchanges["binance"] = ccxt.binance({
                'apiKey': self.config["binance_api_key"],
                'secret': self.config["binance_api_secret"],
                'options': {
                    'defaultType': 'future', # Para Binance Futures
                },
            })
            self.ui.update_panel("Conectado à Binance Futures.")
        
        # TODO: Adicionar suporte para MEXC, dYdX, GMX
        # Exemplo para MEXC (spot, para futuros seria diferente)
        if "mexc_api_key" in self.config and "mexc_api_secret" in self.config:
            self.exchanges["mexc"] = ccxt.mexc({
                'apiKey': self.config["mexc_api_key"],
                'secret': self.config["mexc_api_secret"],
            })
            self.ui.update_panel("Conectado à MEXC.")

        # dYdX e GMX são DEXs e exigem web3.py ou APIs específicas, que são mais complexas
        # e podem precisar de uma fase separada para implementação.
        # Por enquanto, apenas um placeholder.
        if "dydx_api_key" in self.config:
            self.ui.update_panel("dYdX configurado (requer implementação web3.py).")
        if "gmx_api_key" in self.config:
            self.ui.update_panel("GMX configurado (requer implementação web3.py).")

    async def process_signal(self, signal_data):
        self.ui.update_panel(f"Processando sinal: {signal_data["content"][:50]}...")
        
        # TODO: Implementar a interpretação de sinais de forma mais robusta
        # Isso exigirá parsing de texto para extrair: par, tipo de ordem (LONG/SHORT), alavancagem, SL, TP
        # Por exemplo, usando regex ou processamento de linguagem natural simples.

        # Exemplo simplificado de parsing para BTCUSDT LONG
        if "BTCUSDT LONG" in signal_data["content"].upper():
            symbol = "BTC/USDT"
            side = "buy"
            amount = 0.001 # Exemplo de quantidade, deve ser dinâmico
            exchange_name = "binance" # Deve ser extraído do sinal ou configurado
            leverage = 25 # Exemplo de alavancagem

            if exchange_name in self.exchanges:
                exchange = self.exchanges[exchange_name]
                try:
                    # Adaptar nomenclaturas de pares (ex: BTCUSDT -> BTC/USDT)
                    # ccxt já faz isso na maioria dos casos, mas pode ser necessário um mapeamento customizado

                    # Validar saldo, par, margem e regras da exchange/DEX
                    # Exemplo: verificar saldo disponível
                    # balance = await exchange.fetch_balance()
                    # if balance["USDT"]["free"] < amount * price: # Exemplo simplificado
                    #    self.ui.update_panel("Saldo insuficiente.")
                    #    return

                    # Definir alavancagem (apenas para futuros)
                    if hasattr(exchange, 'set_leverage') and exchange.options.get('defaultType') == 'future':
                        await exchange.set_leverage(leverage, symbol)
                        self.ui.update_panel(f"Alavancagem de {leverage}x definida para {symbol}.")

                    # Executar ordem
                    order = await exchange.create_market_buy_order(symbol, amount)
                    self.ui.update_panel(f"Ordem executada na {exchange_name}: {order["id"]}")
                    self.data_manager.save_order(order) # Salvar a ordem
                except Exception as e:
                    self.ui.update_panel(f"Erro ao executar ordem na {exchange_name}: {e}")
            else:
                self.ui.update_panel(f"Exchange {exchange_name} não configurada ou não suportada para este tipo de operação.")
        
        # TODO: Implementar a execução manual de comandos via terminal
        # Isso será feito na TerminalUI, que chamará métodos aqui no OrderExecutor

    async def close_position(self, symbol, exchange_name):
        # TODO: Implementar lógica para fechar posição
        self.ui.update_panel(f"Fechando posição para {symbol} na {exchange_name}...")
        pass

    async def switch_dex(self, dex_name):
        # TODO: Implementar lógica para trocar de DEX
        self.ui.update_panel(f"Trocando para DEX: {dex_name}...")
        pass


