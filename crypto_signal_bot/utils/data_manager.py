import pandas as pd
import json
import os

class DataManager:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.signals_file_csv = os.path.join(data_dir, "signals.csv")
        self.orders_file_json = os.path.join(data_dir, "orders.json")

        # Inicializa arquivos se não existirem
        if not os.path.exists(self.signals_file_csv):
            pd.DataFrame(columns=["timestamp", "author", "content", "message_type", "signal_id", "attachments"]).to_csv(self.signals_file_csv, index=False)
        if not os.path.exists(self.orders_file_json):
            with open(self.orders_file_json, "w") as f:
                json.dump([], f)

    def save_signal(self, signal_data):
        df = pd.DataFrame([signal_data])
        df.to_csv(self.signals_file_csv, mode=\

a", header=False, index=False)

    def save_order(self, order_data):
        with open(self.orders_file_json, "r+") as f:
            orders = json.load(f)
            orders.append(order_data)
            f.seek(0)
            json.dump(orders, f, indent=4)
            f.truncate()

    def load_signals(self):
        return pd.read_csv(self.signals_file_csv)

    def load_orders(self):
        with open(self.orders_file_json, "r") as f:
            return json.load(f)


