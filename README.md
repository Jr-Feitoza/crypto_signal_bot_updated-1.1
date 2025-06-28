# Crypto Signal Bot

Este projeto visa desenvolver um bot em Python, leve, modular e eficiente, para captação de sinais de criptomoedas do Telegram, execução de ordens em exchanges/DEXs e exibição de um painel visual no terminal, adaptado para desktop e celulares Android.

## Novas Funcionalidades e Ajustes (Conforme Requisitos)

Esta versão do bot incorpora os seguintes ajustes e melhorias:

1.  **Diferenciação e Filtragem de Sinais:**
    *   O bot agora é capaz de diferenciar mensagens de sinais, de alvo atingido e outros tipos de mensagens.
    *   **Processa somente mensagens de sinais válidas**, ignorando as demais.

2.  **Extração Detalhada de Dados do Sinal:**
    *   Extrai automaticamente o **par de moedas** (ex: BTCUSDT, ETHUSDT).
    *   Extrai o **preço de entrada**.
    *   Extrai o **preço do Stop Loss (SL)**.
    *   Extrai o **preço do Alvo 3 (TP3)**, que será usado como Take Profit.

3.  **Lógica de Margem Ajustável:**
    *   A entrada padrão para cada operação é de **$1 dólar de margem**.
    *   O **valor da margem de entrada é ajustável** e pode ser definido previamente na inicialização do bot.
    *   **Moedas que exigem uma margem maior** do que a estabelecida na configuração **serão ignoradas** para evitar operações indesejadas.

4.  **Gestão de TP e SL Pós-Abertura da Posição:**
    *   O bot agora inclui a lógica para gerenciar ordens de Take Profit (TP) e Stop Loss (SL) **após a abertura da posição**, permitindo ajustes no decorrer do trading.

## Requisitos

Para executar o bot, você precisará das seguintes bibliotecas Python:

*   `telethon`: Para interação com a API do Telegram.
*   `ccxt`: Para conexão com diversas exchanges e DEXs.
*   `rich`: Para a interface visual no terminal.
*   `textual`: Para a interface visual interativa no terminal.
*   `pandas`: Para manipulação e armazenamento de dados (CSV/JSON).

Você pode instalar todas as dependências usando `pip`:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `config.json` na raiz do projeto com suas credenciais do Telegram e configurações de margem:

```json
{
    "telegram_api_id": "SEU_API_ID",
    "telegram_api_hash": "SEU_API_HASH",
    "telegram_channels": [-1001234567890], // IDs dos canais do Telegram
    "binance_api_key": "SUA_BINANCE_API_KEY",
    "binance_api_secret": "SUA_BINANCE_API_SECRET",
    "entry_margin_usd": 1.0, // Valor da margem de entrada em USD (padrão: 1.0)
    "max_allowed_margin_rate": 0.05, // Taxa de margem máxima permitida (ex: 0.05 = 5%)
    "default_leverage": 25 // Alavancagem padrão para operações
}
```

**Importante:** Substitua `SEU_API_ID`, `SEU_API_HASH`, os IDs dos canais e as chaves da API da Binance pelas suas informações reais.

## Execução

### Android (Termux)

```bash
pkg install python git
pip install telethon ccxt rich textual pandas
termux-wake-lock
tmux new -s sinal_bot
python main.py
```

### Linux

```bash
sudo apt install tmux
tmux new -s sinal_bot
python3 main.py
```

## Estrutura do Projeto

```
crypto_signal_bot/
├── core/
│   ├── telegram_listener.py    # Captação e parsing de sinais do Telegram
│   ├── order_executor.py       # Execução de ordens e gestão de TP/SL
│   └── terminal_ui.py          # Interface visual no terminal
├── utils/
│   ├── config_loader.py        # Carregamento e salvamento de configurações
│   └── data_manager.py         # Armazenamento local de sinais e ordens
├── data/                       # Diretório para arquivos CSV/JSON de dados
├── main.py                     # Ponto de entrada principal do bot
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## Observações

*   A implementação de DEXs (dYdX, GMX) e exchanges como MEXC para futuros pode exigir bibliotecas adicionais (ex: `web3.py`) e lógica mais complexa, que não estão totalmente detalhadas neste README.
*   A lógica para ignorar moedas com margem superior é um placeholder e precisaria de integração real com a API da exchange para obter os requisitos de margem de cada par.

---

**Desenvolvido por:** Manus AI
**Data:** 28 de Junho de 2025


