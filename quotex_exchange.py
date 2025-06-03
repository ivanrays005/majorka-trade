
import time
import pandas as pd
from quotexapi.stable_api import Quotex
from exchanges.exchange import Exchange


class QuotexExchange(Exchange):
    def __init__(self, username: str, password: str, account_type: str = "PRACTICE"):
        super().__init__(username, password, account_type)
        self._api = None
        
    @property
    def api(self) -> Quotex:
        if self._api is None:
            self._api = Quotex(self.username, self.password)
            
            # Проверяем подключение
            check, reason = self._api.connect()
            if not check:
                raise Exception(f"Ошибка подключения к Quotex: {reason}")
            
            # Устанавливаем тип счета
            if self.account_type == "PRACTICE":
                self._api.change_balance("PRACTICE")
            else:
                self._api.change_balance("REAL")
                
        return self._api

    def retry(self):
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            try:
                if not self.api.check_connect():
                    print(f"Попытка переподключения {attempt + 1}/{max_attempts}...")
                    check, reason = self.api.connect()
                    if check:
                        print("✅ Успешно переподключен к Quotex")
                        return True
                    else:
                        print(f"❌ Ошибка подключения: {reason}")
                else:
                    print("✅ Подключение к Quotex активно")
                    return True
                    
                attempt += 1
                if attempt < max_attempts:
                    time.sleep(3)
                    
            except Exception as e:
                print(f"❌ Ошибка при переподключении: {str(e)}")
                attempt += 1
                time.sleep(3)
                
        print("❌ Превышено максимальное количество попыток подключения")
        return False

    @property
    def balance(self) -> float:
        return self.api.get_balance()

    def candles_to_df(self, pair):
        # Получаем свечи для Quotex
        timestamp = self.api.get_server_timestamp()
        candles = []

        # Получаем историю свечей
        for _ in range(5):
            data = self.api.get_candles(pair, 300, 1000, timestamp)
            if data:
                timestamp = int(data[0]["from"]) - 1
                candles += data

        if not candles:
            # Если нет данных, создаем пустой DataFrame
            return pd.DataFrame(columns=["from", "close", "min", "max", "volume"])

        dataframe = pd.DataFrame(candles)
        dataframe.sort_values(by=["from"], inplace=True, ascending=True)
        dataframe.drop(dataframe.tail(1).index, inplace=True)
        return dataframe[["from", "close", "min", "max", "volume"]]
