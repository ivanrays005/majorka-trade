
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from exchanges.exchange import Exchange


class PocketOptionExchange(Exchange):
    def __init__(self, username: str, password: str, account_type: str = "PRACTICE"):
        super().__init__(username, password, account_type)
        self._connected = True  # Демо режим всегда подключен
        self._balance = 10000.0  # Начальный демо баланс
        self._trades = []  # История сделок
        print(f"🎮 Pocket Option Демо режим активирован!")
        print(f"👤 Пользователь: {username}")
        print(f"💳 Демо баланс: ${self._balance}")
        
    @property
    def api(self):
        """API интерфейс для совместимости"""
        return self

    

    def check_connect(self) -> bool:
        """Проверка соединения в демо режиме"""
        return self._connected

    def retry(self):
        """Переподключение в демо режиме"""
        print("✅ Демо режим всегда подключен!")
        return True

    @property
    def balance(self) -> float:
        """Получение демо баланса"""
        return self._balance

    def candles_to_df(self, pair) -> pd.DataFrame:
        """Получение данных графика (демо данные)"""
        # В реальной реализации можно парсить данные с графика
        # Пока используем генерацию демо данных
        timestamps = []
        closes = []
        mins = []
        maxs = []
        volumes = []
        
        base_price = 1.2000 if "EUR" in pair else 1.0000
        
        for i in range(100):
            timestamp = int(time.time()) - (100 - i) * 60
            price_change = np.random.normal(0, 0.001)
            close = base_price + price_change
            
            high = close + abs(np.random.normal(0, 0.0005))
            low = close - abs(np.random.normal(0, 0.0005))
            volume = np.random.randint(100, 1000)
            
            timestamps.append(timestamp)
            closes.append(close)
            mins.append(low)
            maxs.append(high)
            volumes.append(volume)
            
            base_price = close
        
        return pd.DataFrame({
            "from": timestamps,
            "close": closes,
            "min": mins,
            "max": maxs,
            "volume": volumes
        })

    def buy(self, pair: str, amount: float, direction: str, duration: int = 60):
        """Демо торговля - симуляция открытия позиции"""
        if amount > self._balance:
            print(f"❌ Недостаточно средств! Баланс: ${self._balance}, требуется: ${amount}")
            return None
            
        order_id = f"po_demo_{int(time.time())}"
        trade_info = {
            'id': order_id,
            'pair': pair,
            'amount': amount,
            'direction': direction,
            'duration': duration,
            'open_time': time.time(),
            'status': 'active'
        }
        
        self._trades.append(trade_info)
        print(f"🎮 Демо позиция открыта: {pair} | {direction.upper()} | ${amount} | {duration}с")
        return order_id

    def check_win_v3(self, order_id: str):
        """Проверка результата демо сделки"""
        # Находим сделку по ID
        trade = None
        for t in self._trades:
            if t['id'] == order_id:
                trade = t
                break
                
        if not trade:
            return None
            
        # Проверяем истекло ли время сделки
        if time.time() - trade['open_time'] < trade['duration']:
            return None  # Сделка еще активна
            
        # Симулируем результат (70% выигрышей для демо)
        import random
        if random.random() < 0.7:
            payout = random.uniform(1.75, 1.95)  # Коэффициент выплаты
            profit = trade['amount'] * payout
            self._balance += profit - trade['amount']  # Обновляем баланс
            trade['status'] = 'win'
            trade['profit'] = profit - trade['amount']
            print(f"✅ Выигрыш: +${profit - trade['amount']:.2f} | Новый баланс: ${self._balance:.2f}")
            return payout
        else:
            self._balance -= trade['amount']  # Списываем проигрыш
            trade['status'] = 'loss'
            trade['profit'] = -trade['amount']
            print(f"❌ Проигрыш: -${trade['amount']:.2f} | Новый баланс: ${self._balance:.2f}")
            return -1

    def test_connection(self):
        """Тестирование демо режима"""
        print("🎮 Тестирование Pocket Option Демо режима...")
        print(f"✅ Статус: {'Подключен' if self._connected else 'Отключен'}")
        print(f"💳 Демо баланс: ${self._balance}")
        print(f"📊 Активных сделок: {len([t for t in self._trades if t['status'] == 'active'])}")
        print("✅ Демо режим работает корректно!")
        return True

    def __del__(self):
        """Очистка демо данных"""
        if hasattr(self, '_trades'):
            print(f"🎮 Завершение демо сессии. Всего сделок: {len(self._trades)}")
        pass
