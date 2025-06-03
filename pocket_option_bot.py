import streamlit as st
import time
from datetime import datetime, timedelta
from bots.rf_bot import RandomForestBot
from exchanges.pocket_option_exchange import PocketOptionExchange


class PocketOptionBot(RandomForestBot):
    def __init__(self, exchange: PocketOptionExchange, pair: str, entry_value: float, 
                 stop_gain: float, stop_loss: float, expiration_time: int = 60):
        super().__init__(exchange, pair, entry_value, stop_gain, stop_loss)
        self.expiration_time = expiration_time  # время экспирации в секундах

    def wait_complete(self, order_id):
        """Ожидание завершения сделки для Pocket Option"""
        start_time = time.time()

        while True:
            # Проверяем статус сделки
            try:
                order_status = self.exchange.check_win_v3(order_id)

                if order_status is not None:
                    if order_status > 0:
                        # Выигрыш
                        profit = order_status
                        return self.get_profit(profit)
                    else:
                        # Проигрыш
                        loss = -self.entry_value
                        return self.get_profit(loss)

                # Проверяем таймаут
                if time.time() - start_time > self.expiration_time + 30:
                    st.warning("⏰ Таймаут ожидания результата сделки")
                    return self.get_profit(-self.entry_value)

            except Exception as e:
                st.error(f"❌ Ошибка проверки сделки: {str(e)}")
                time.sleep(1)

            time.sleep(2)

    def run(self):
        # Проверяем подключение перед запуском
        try:
            if not self.exchange.check_connect():
                st.warning("🔄 Переподключение к Pocket Option...")
                if not self.exchange.retry():
                    st.error("❌ Не удалось подключиться к Pocket Option")
                    return
        except Exception as e:
            st.error(f"❌ Ошибка проверки подключения: {str(e)}")
            return

        st.info(f"""
        🚀 Запуск Pocket Option бота
        📈 Актив: {self.pair}
        💰 Сумма входа: ${self.entry_value}
        📊 Стоп лосс: ${self.stop_loss}
        📈 Стоп прибыль: ${self.stop_gain}
        ⏰ Экспирация: {self.expiration_time} сек
        """)

        # Контейнер для обновления статистики
        stats_container = st.empty()
        chart_container = st.empty()

        while True:
            try:
                # Проверяем соединение
                if not self.exchange.check_connect():
                    st.warning("🔄 Потеря соединения. Переподключение...")
                    if not self.exchange.retry():
                        st.error("❌ Не удалось переподключиться")
                        time.sleep(10)
                        continue

                # Получаем данные свечей
                df = self.exchange.candles_to_df(pair=self.pair)

                if df.empty:
                    st.warning("⚠️ Нет данных для анализа")
                    time.sleep(5)
                    continue

                # Показываем график
                with chart_container.container():
                    st.line_chart(df["close"])

                # Получаем сигнал
                entry_sign = self.sinal(df)

                if entry_sign:
                    # Определяем направление для Pocket Option
                    direction = "call" if entry_sign == "call" else "put"

                    # Размещаем ордер
                    status, order_id = self.exchange.api.buy(
                        amount=self.entry_value,
                        active=self.pair,
                        direction=direction,
                        duration=self.expiration_time
                    )

                    if status:
                        st.success(f"✅ Ордер размещен: {direction.upper()} на ${self.entry_value}")
                        self.wait_complete(order_id)
                    else:
                        st.error("❌ Ошибка размещения ордера")

                # Обновляем статистику
                with stats_container.container():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("💰 Баланс", f"${self.exchange.balance:.2f}")
                    with col2:
                        st.metric("📊 Прибыль", f"${self.lucro:.2f}")
                    with col3:
                        profit_percent = (self.lucro / abs(self.stop_loss)) * 100 if self.stop_loss != 0 else 0
                        st.metric("📈 Прогресс", f"{profit_percent:.1f}%")

                time.sleep(5)  # Пауза между анализами

            except Exception as e:
                st.error(f"❌ Ошибка в работе бота: {str(e)}")
                time.sleep(10)
import streamlit as st
import time
from datetime import datetime, timedelta
from bots.rf_bot import RandomForestBot
from exchanges.pocket_option_exchange import PocketOptionExchange


class PocketOptionBot(RandomForestBot):
    def __init__(self, exchange: PocketOptionExchange, pair: str, entry_value: float, 
                 stop_gain: float, stop_loss: float, expiration_time: int = 60):
        super().__init__(exchange, pair, entry_value, stop_gain, stop_loss)
        self.expiration_time = expiration_time  # время экспирации в секундах

    def wait_complete(self, order_id):
        """Ожидание завершения сделки для Pocket Option"""
        start_time = time.time()

        while True:
            # Проверяем статус сделки
            try:
                order_status = self.exchange.check_win_v3(order_id)

                if order_status is not None:
                    if order_status > 0:
                        # Выигрыш
                        profit = self.entry_value * order_status
                        return self.get_profit(profit)
                    else:
                        # Проигрыш
                        loss = -self.entry_value
                        return self.get_profit(loss)

                # Проверяем таймаут
                if time.time() - start_time > self.expiration_time + 30:
                    st.warning("⏰ Таймаут ожидания результата сделки")
                    return self.get_profit(-self.entry_value)

            except Exception as e:
                st.error(f"❌ Ошибка проверки статуса: {str(e)}")
                time.sleep(5)
                continue

            time.sleep(2)

    def run(self):
        # Проверяем подключение перед запуском
        try:
            if not self.exchange.check_connect():
                st.warning("🔄 Переподключение к Pocket Option...")
                if not self.exchange.retry():
                    st.error("❌ Не удалось подключиться к Pocket Option")
                    return
        except Exception as e:
            st.error(f"❌ Ошибка проверки подключения: {str(e)}")
            return

        st.info(f"""
        🚀 Запуск Pocket Option бота
        📈 Актив: {self.pair}
        💰 Размер ставки: ${self.entry_value}
        ⏱️ Экспирация: {self.expiration_time}с
        🎯 Stop Gain: ${self.stop_gain}
        🛑 Stop Loss: ${self.stop_loss}
        """)

        # Отображаем баланс
        balance = self.exchange.balance
        st.metric("💳 Баланс", f"${balance:.2f}")

        while True:
            try:
                # Проверяем соединение
                if not self.exchange.check_connect():
                    st.warning("🔄 Потеря соединения. Переподключение...")
                    if not self.exchange.retry():
                        st.error("❌ Не удалось переподключиться")
                        time.sleep(10)
                        continue

                # Получаем данные свечей
                df = self.exchange.candles_to_df(pair=self.pair)

                if df is None or df.empty:
                    st.warning("⚠️ Нет данных для анализа")
                    time.sleep(10)
                    continue

                # Получаем сигнал
                sinal = self.sinal(df)

                if sinal != "WAIT":
                    direction = "call" if sinal == "PUT" else "put"

                    st.info(f"🎯 Сигнал: {sinal} | Направление: {direction.upper()}")

                    # Открываем позицию
                    order_id = self.exchange.buy(
                        pair=self.pair,
                        amount=self.entry_value,
                        direction=direction,
                        duration=self.expiration_time
                    )

                    if order_id:
                        st.success(f"✅ Позиция открыта: {order_id}")

                        # Ждем завершения
                        result = self.wait_complete(order_id)

                        # Обновляем баланс (демо)
                        if result > 0:
                            self.exchange._balance += result
                        else:
                            self.exchange._balance += result

                        st.metric("💳 Новый баланс", f"${self.exchange.balance:.2f}")
                    else:
                        st.error("❌ Ошибка открытия позиции")
                else:
                    st.info("⏳ Ожидание сигнала...")

            except Exception as e:
                st.error(f"❌ Ошибка в работе бота: {str(e)}")

            time.sleep(2)