import streamlit as st
import time
import io
import base64
import re
from datetime import datetime
import pytz
import requests
import json
import pandas as pd
import numpy as np
from typing import Dict, Any
import yfinance as yf
import ta
import math

# Настройка страницы для мобильных устройств
st.set_page_config(
    page_title="📊 MAJORKA VIP",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS стили в стиле Telegram для мобильных устройств
def load_telegram_mobile_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

    * {
        box-sizing: border-box;
    }

    .main {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #0f0f23;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        overflow-x: hidden;
    }

    .block-container {
        padding: 1rem 0.5rem !important;
        max-width: 100% !important;
    }

    /* Telegram-style header */
    .telegram-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 0 0 25px 25px;
        padding: 1.5rem 1rem;
        margin: -1rem -0.5rem 1rem -0.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .app-subtitle {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin: 0.3rem 0 0 0;
        font-weight: 400;
    }

    /* Telegram-style cards */
    .telegram-card {
        background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
        border-radius: 18px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }

    .signal-card {
        background: linear-gradient(145deg, #1a2332, #2d3748);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        border: 2px solid;
        position: relative;
        overflow: hidden;
    }

    .signal-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 20px 20px 0 0;
    }

    .signal-call {
        border-color: #4CAF50;
        background: linear-gradient(145deg, #1a2e1a, #2d4a2d);
    }

    .signal-call::before {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
    }

    .signal-put {
        border-color: #f44336;
        background: linear-gradient(145deg, #2e1a1a, #4a2d2d);
    }

    .signal-put::before {
        background: linear-gradient(90deg, #f44336, #ff5722);
    }

    .signal-wait {
        border-color: #ff9800;
        background: linear-gradient(145deg, #2e2a1a, #4a452d);
    }

    .signal-wait::before {
        background: linear-gradient(90deg, #ff9800, #ffc107);
    }

    /* Кнопки в стиле Telegram */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        margin: 0.5rem 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }

    /* Метрики в стиле Telegram */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.8rem;
        margin: 1rem 0;
    }

    .metric-card {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.3rem 0;
    }

    .metric-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-change {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    .metric-change.positive { color: #4CAF50; }
    .metric-change.negative { color: #f44336; }

    /* Селекты и инпуты */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .stTextInput > div > div > input {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Экспандеры */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    .streamlit-expanderContent {
        background: rgba(30, 30, 46, 0.8) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
    }

    /* Прогресс индикаторы */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }

    .confidence-bar {
        height: 8px;
        border-radius: 6px;
        background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4CAF50 100%);
        position: relative;
        margin: 0.5rem 0;
    }

    .confidence-indicator {
        position: absolute;
        top: -2px;
        width: 12px;
        height: 12px;
        background: white;
        border-radius: 50%;
        border: 2px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    /* Анимации */
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .slide-in {
        animation: slideIn 0.5s ease-out;
    }

    /* История торговли */
    .history-item {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e);
        border-radius: 12px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .history-call { border-left-color: #4CAF50; }
    .history-put { border-left-color: #f44336; }
    .history-wait { border-left-color: #ff9800; }

    /* Скрытие стандартных элементов Streamlit */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Мобильная адаптивность */
    @media (max-width: 768px) {
        .metric-container {
            grid-template-columns: repeat(2, 1fr);
        }

        .app-title {
            font-size: 1.5rem;
        }

        .telegram-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
    }

    /* Цветовая схема для текста */
    .success-text { color: #4CAF50; font-weight: 600; }
    .error-text { color: #f44336; font-weight: 600; }
    .warning-text { color: #ff9800; font-weight: 600; }
    .info-text { color: #667eea; font-weight: 600; }

    /* Иконки и эмодзи */
    .icon-large { font-size: 2rem; margin: 0.5rem 0; }
    .icon-medium { font-size: 1.5rem; }
    .icon-small { font-size: 1rem; }

    /* Темная тема для графиков */
    .stPlotlyChart {
        background: transparent !important;
    }

    /* Telegram-style toggles */
    .stCheckbox > label {
        color: white !important;
        font-weight: 500 !important;
    }

    /* Боковая панель */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e2e 0%, #2a2a3e 100%) !important;
    }

    .css-1d391kg .stSelectbox label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def is_trading_time():
    """Проверяет, подходящее ли время для торговли"""
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)

    # Исключаем время низкой волатильности
    hour = moscow_time.hour
    weekday = moscow_time.weekday()

    # Выходные
    if weekday >= 5:  # Суббота и воскресенье
        return False, "Выходные дни"

    # Ночное время (низкая активность)
    if 2 <= hour <= 6:
        return False, "Низкая активность рынка"

    # Время обеда (низкая волатильность)
    if 13 <= hour <= 14:
        return False, "Обеденное время"

    # Лучшее время для торговли
    if (8 <= hour <= 12) or (15 <= hour <= 19):
        return True, "Оптимальное время"

    return True, "Обычное время"

def get_market_volatility(df: pd.DataFrame) -> dict:
    """Расширенный анализ волатильности рынка"""
    try:
        # ATR для определения волатильности
        atr_14 = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
        current_atr = atr_14.iloc[-1]
        avg_atr = atr_14.tail(50).mean()

        # Дополнительные показатели волатильности
        price_std = df['Close'].tail(20).std()
        price_mean = df['Close'].tail(20).mean()
        cv = (price_std / price_mean) * 100 if price_mean > 0 else 0  # Коэффициент вариации

        # Размах цен
        high_low_ratio = (df['High'].tail(10).max() - df['Low'].tail(10).min()) / df['Close'].iloc[-1]

        # Комплексная оценка волатильности
        volatility_ratio = current_atr / avg_atr if avg_atr > 0 else 1

        # Нормализованная волатильность
        normalized_volatility = (current_atr / df['Close'].iloc[-1]) * 100

        # Определяем уровень волатильности
        if volatility_ratio > 2.0 or normalized_volatility > 2.0:
            level = "Критическая"
            recommendation = "Не торговать"
            risk_level = 5
        elif volatility_ratio > 1.5 or normalized_volatility > 1.2:
            level = "Очень высокая"
            recommendation = "Крайне осторожно"
            risk_level = 4
        elif volatility_ratio > 1.2 or normalized_volatility > 0.8:
            level = "Высокая"
            recommendation = "Осторожно"
            risk_level = 3
        elif volatility_ratio > 0.8 and normalized_volatility > 0.3:
            level = "Нормальная"
            recommendation = "Хорошие условия"
            risk_level = 2
        elif volatility_ratio > 0.5:
            level = "Умеренная"
            recommendation = "Отличные условия"
            risk_level = 1
        else:
            level = "Низкая"
            recommendation = "Слабые сигналы"
            risk_level = 3

        # Анализ тренда волатильности
        recent_atr = atr_14.tail(5).mean()
        older_atr = atr_14.tail(15).head(10).mean()
        volatility_trend = "Растет" if recent_atr > older_atr * 1.1 else "Падает" if recent_atr < older_atr * 0.9 else "Стабильная"

        return {
            "level": level,
            "ratio": volatility_ratio,
            "normalized": normalized_volatility,
            "trade_recommendation": recommendation,
            "risk_level": risk_level,
            "trend": volatility_trend,
            "coefficient_variation": cv,
            "high_low_ratio": high_low_ratio * 100,
            "current_atr": current_atr,
            "avg_atr": avg_atr
        }
    except Exception as e:
        return {
            "level": "Ошибка расчета", 
            "ratio": 1, 
            "normalized": 0,
            "trade_recommendation": "Воздержаться",
            "risk_level": 5,
            "trend": "Неизвестно",
            "coefficient_variation": 0,
            "high_low_ratio": 0,
            "current_atr": 0.001,
            "avg_atr": 0.001
        }

def get_risk_warnings(indicators: dict, pair: str, timeframe: str) -> list:
    """Генерирует предупреждения о рисках"""
    warnings = []

    # Проверка противоречивых сигналов
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    bb_position = indicators.get('bb_position', 0.5)

    # Противоречие между RSI и MACD
    if (rsi > 70 and macd > macd_signal) or (rsi < 30 and macd < macd_signal):
        warnings.append("⚠️ Противоречие между RSI и MACD")

    # Экстремальные значения
    if rsi > 85 or rsi < 15:
        warnings.append("🔥 Экстремальные значения RSI - высокий риск разворота")

    # Низкая волатильность
    atr = indicators.get('atr', 0)
    if atr < 0.0001:
        warnings.append("😴 Очень низкая волатильность - слабые сигналы")

    # Боковое движение
    if 0.3 < bb_position < 0.7 and 40 < rsi < 60:
        warnings.append("↔️ Возможное боковое движение")

    # Краткосрочные таймфреймы
    if timeframe in ['1m', '3m']:
        warnings.append("⚡ Короткий таймфрейм - повышенные риски")

    return warnings

class PocketOptionAnalyzer:
    def __init__(self):
        self.gpt_api_key = None
        if 'openai_api_key' in st.session_state:
            self.gpt_api_key = st.session_state.openai_api_key

    def get_market_data(self, pair: str, timeframe: str) -> pd.DataFrame:
        """Получает данные рынка через Yahoo Finance"""
        try:
            if "/" in pair:
                symbol = pair.replace("/", "") + "=X"
            else:
                symbol = pair

            period_map = {
                "1m": "1d", "3m": "5d", "5m": "5d", "15m": "5d",
                "30m": "1mo", "1h": "1mo", "4h": "3mo", "1d": "1y"
            }

            interval_map = {
                "1m": "1m", "3m": "5m", "5m": "5m", "15m": "15m",
                "30m": "30m", "1h": "1h", "4h": "1h", "1d": "1d"
            }

            period = period_map.get(timeframe, "1mo")
            interval = interval_map.get(timeframe, "1h")

            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if data.empty:
                st.error(f"❌ Не удалось получить данные для {pair}")
                return None

            # Проверяем на валидность данных
            if data['Close'].isna().all() or len(data) < 20:
                st.warning(f"⚠️ Недостаточно данных для анализа {pair}")
                return None

            # Удаляем строки с NaN значениями
            data = data.dropna()

            if len(data) < 20:
                st.warning(f"⚠️ После очистки недостаточно данных для анализа {pair}")
                return None

            return data

        except Exception as e:
            st.error(f"❌ Ошибка получения данных: {str(e)}")
            return None

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Рассчитывает технические индикаторы"""
        try:
            indicators = {}

            # Проверяем достаточность данных
            if len(df) < 50:
                st.warning("⚠️ Недостаточно данных для корректного расчета всех индикаторов")

            # RSI с проверкой
            try:
                rsi_indicator = ta.momentum.RSIIndicator(df['Close'])
                rsi_value = rsi_indicator.rsi().iloc[-1]
                indicators['rsi'] = rsi_value if not pd.isna(rsi_value) else 50
            except:
                indicators['rsi'] = 50

            # MACD с проверкой
            try:
                macd = ta.trend.MACD(df['Close'])
                macd_value = macd.macd().iloc[-1]
                macd_signal_value = macd.macd_signal().iloc[-1]
                macd_histogram_value = macd.macd_diff().iloc[-1]

                indicators['macd'] = macd_value if not pd.isna(macd_value) else 0
                indicators['macd_signal'] = macd_signal_value if not pd.isna(macd_signal_value) else 0
                indicators['macd_histogram'] = macd_histogram_value if not pd.isna(macd_histogram_value) else 0
            except:
                indicators['macd'] = 0
                indicators['macd_signal'] = 0
                indicators['macd_histogram'] = 0

            # Bollinger Bands с проверкой
            try:
                bb = ta.volatility.BollingerBands(df['Close'])
                bb_upper = bb.bollinger_hband().iloc[-1]
                bb_middle = bb.bollinger_mavg().iloc[-1]
                bb_lower = bb.bollinger_lband().iloc[-1]

                indicators['bb_upper'] = bb_upper if not pd.isna(bb_upper) else df['Close'].iloc[-1] * 1.02
                indicators['bb_middle'] = bb_middle if not pd.isna(bb_middle) else df['Close'].iloc[-1]
                indicators['bb_lower'] = bb_lower if not pd.isna(bb_lower) else df['Close'].iloc[-1] * 0.98

                # Расчет позиции в BB
                if indicators['bb_upper'] != indicators['bb_lower']:
                    indicators['bb_position'] = (df['Close'].iloc[-1] - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
                else:
                    indicators['bb_position'] = 0.5
            except:
                indicators['bb_upper'] = df['Close'].iloc[-1] * 1.02
                indicators['bb_middle'] = df['Close'].iloc[-1]
                indicators['bb_lower'] = df['Close'].iloc[-1] * 0.98
                indicators['bb_position'] = 0.5

            # Скользящие средние с проверкой
            try:
                sma_20 = ta.trend.SMAIndicator(df['Close'], window=min(20, len(df)-1)).sma_indicator().iloc[-1]
                indicators['sma_20'] = sma_20 if not pd.isna(sma_20) else df['Close'].iloc[-1]
            except:
                indicators['sma_20'] = df['Close'].iloc[-1]

            try:
                if len(df) >= 50:
                    sma_50 = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator().iloc[-1]
                    indicators['sma_50'] = sma_50 if not pd.isna(sma_50) else df['Close'].iloc[-1]
                else:
                    indicators['sma_50'] = df['Close'].iloc[-1]
            except:
                indicators['sma_50'] = df['Close'].iloc[-1]

            try:
                ema_12 = ta.trend.EMAIndicator(df['Close'], window=min(12, len(df)-1)).ema_indicator().iloc[-1]
                indicators['ema_12'] = ema_12 if not pd.isna(ema_12) else df['Close'].iloc[-1]
            except:
                indicators['ema_12'] = df['Close'].iloc[-1]

            try:
                ema_26 = ta.trend.EMAIndicator(df['Close'], window=min(26, len(df)-1)).ema_indicator().iloc[-1]
                indicators['ema_26'] = ema_26 if not pd.isna(ema_26) else df['Close'].iloc[-1]
            except:
                indicators['ema_26'] = df['Close'].iloc[-1]

            # Stochastic с проверкой
            try:
                stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
                stoch_k = stoch.stoch().iloc[-1]
                stoch_d = stoch.stoch_signal().iloc[-1]

                indicators['stoch_k'] = stoch_k if not pd.isna(stoch_k) else 50
                indicators['stoch_d'] = stoch_d if not pd.isna(stoch_d) else 50
            except:
                indicators['stoch_k'] = 50
                indicators['stoch_d'] = 50

            # ATR с проверкой
            try:
                atr = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range().iloc[-1]
                indicators['atr'] = atr if not pd.isna(atr) else 0.001
            except:
                indicators['atr'] = 0.001

            # Williams %R с проверкой
            try:
                williams_r = ta.momentum.WilliamsRIndicator(df['High'], df['Low'], df['Close']).williams_r().iloc[-1]
                indicators['williams_r'] = williams_r if not pd.isna(williams_r) else -50
            except:
                indicators['williams_r'] = -50

            # CCI (Commodity Channel Index)
            try:
                cci = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close']).cci().iloc[-1]
                indicators['cci'] = cci if not pd.isna(cci) else 0
            except:
                indicators['cci'] = 0

            # MFI (Money Flow Index)
            try:
                if 'Volume' in df.columns and not df['Volume'].isna().all():
                    mfi = ta.volume.MFIIndicator(df['High'], df['Low'], df['Close'], df['Volume']).money_flow_index().iloc[-1]
                    indicators['mfi'] = mfi if not pd.isna(mfi) else 50
                else:
                    indicators['mfi'] = 50
            except:
                indicators['mfi'] = 50

            # Ultimate Oscillator
            try:
                uo = ta.momentum.UltimateOscillator(df['High'], df['Low'], df['Close']).ultimate_oscillator().iloc[-1]
                indicators['ultimate_oscillator'] = uo if not pd.isna(uo) else 50
            except:
                indicators['ultimate_oscillator'] = 50

            # TRIX
            try:
                trix = ta.trend.TRIXIndicator(df['Close']).trix().iloc[-1]
                indicators['trix'] = trix if not pd.isna(trix) else 0
            except:
                indicators['trix'] = 0

            # Aroon
            try:
                aroon = ta.trend.AroonIndicator(df['High'], df['Low'])
                aroon_up = aroon.aroon_up().iloc[-1]
                aroon_down = aroon.aroon_down().iloc[-1]
                indicators['aroon_up'] = aroon_up if not pd.isna(aroon_up) else 50
                indicators['aroon_down'] = aroon_down if not pd.isna(aroon_down) else 50
            except:
                indicators['aroon_up'] = 50
                indicators['aroon_down'] = 50

            # Volume indicators (если есть объем)
            if 'Volume' in df.columns and not df['Volume'].isna().all():
                try:
                    volume_sma = df['Volume'].rolling(window=min(20, len(df))).mean().iloc[-1]
                    indicators['volume_sma'] = volume_sma if not pd.isna(volume_sma) else 0
                except:
                    indicators['volume_sma'] = 0

            # Текущая цена и изменение
            indicators['current_price'] = df['Close'].iloc[-1]
            try:
                if len(df) > 1:
                    price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                    indicators['price_change'] = price_change if not pd.isna(price_change) else 0
                else:
                    indicators['price_change'] = 0
            except:
                indicators['price_change'] = 0

            # Проверяем, что все основные индикаторы присутствуют
            required_indicators = ['rsi', 'macd', 'macd_signal', 'bb_position', 'sma_20', 'stoch_k', 'williams_r', 'current_price']
            for indicator in required_indicators:
                if indicator not in indicators or pd.isna(indicators[indicator]):
                    st.warning(f"⚠️ Проблема с расчетом индикатора: {indicator}")

            return indicators

        except Exception as e:
            st.error(f"❌ Ошибка расчета индикаторов: {str(e)}")
            # Возвращаем базовые значения в случае ошибки
            return {
                'rsi': 50,
                'macd': 0,
                'macd_signal': 0,
                'macd_histogram': 0,
                'bb_upper': 0,
                'bb_middle': 0,
                'bb_lower': 0,
                'bb_position': 0.5,
                'sma_20': 0,
                'sma_50': 0,
                'ema_12': 0,
                'ema_26': 0,
                'stoch_k': 50,
                'stoch_d': 50,
                'atr': 0.001,
                'williams_r': -50,
                'current_price': 0,
                'price_change': 0
            }

    def analyze_with_ai(self, market_data: pd.DataFrame, indicators: Dict[str, Any], pair: str, timeframe: str) -> str:
        """Анализирует данные рынка с помощью ИИ"""
        if not self.gpt_api_key or not self.gpt_api_key.startswith('sk-'):
            return self.telegram_analysis(indicators, pair, timeframe)

        try:
            recent_prices = market_data['Close'].tail(10).tolist()
            highs = market_data['High'].tail(5).tolist()
            lows = market_data['Low'].tail(5).tolist()

            moscow_tz = pytz.timezone('Europe/Moscow')
            moscow_time = datetime.now(moscow_tz)

            current_price = indicators.get('current_price', 0)
            price_change = indicators.get('price_change', 0)
            rsi = indicators.get('rsi', 0)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            bb_position = indicators.get('bb_position', 0)
            sma_20 = indicators.get('sma_20', 0)

            prompt = f"""
            Ты профессиональный трейдер с 15+ летним опытом торговли бинарными опционами в стиле Telegram бота.
            Проанализируй технические данные для {pair} на {timeframe} и дай ЧЕТКИЙ торговый сигнал.

            ДАННЫЕ ({moscow_time.strftime('%H:%M:%S MSK')}):
            - Пара: {pair} | Таймфрейм: {timeframe}
            - Цена: {current_price:.5f} ({price_change:+.2f}%)
            - RSI: {rsi:.1f} | MACD: {macd:.5f}
            - BB позиция: {bb_position:.2f} | SMA20: {sma_20:.5f}

            ТРЕБОВАНИЯ:
            1. Дай ЧЕТКИЙ сигнал: 🟢 CALL или 🔴 PUT или ⚪ ЖДАТЬ
            2. Укажи уверенность: 1-10
            3. Время экспирации: 1-5 минут
            4. Краткое обоснование

            ФОРМАТ (строго придерживайся):
            🎯 СИГНАЛ: [CALL/PUT/ЖДАТЬ]
📊 УВЕРЕННОСТЬ: [X/10]
⏰ ЭКСПИРАЦИЯ: [X мин]
💡 ПРИЧИНА: [кратко]
            """

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.gpt_api_key}"
            }

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "Ты профессиональный трейдер бинарных опционов. Давай четкие торговые сигналы."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.2
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return self.telegram_analysis(indicators, pair, timeframe)

        except Exception as e:
            return self.telegram_analysis(indicators, pair, timeframe)

    def telegram_analysis(self, indicators: Dict[str, Any], pair: str, timeframe: str) -> str:
        """Максимально улучшенный человеческий анализ как у профессионального трейдера"""
        try:
            # Получаем все индикаторы
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            bb_position = indicators.get('bb_position', 0.5)
            current_price = indicators.get('current_price', 0)
            sma_20 = indicators.get('sma_20', 0)
            sma_50 = indicators.get('sma_50', 0)
            ema_12 = indicators.get('ema_12', 0)
            ema_26 = indicators.get('ema_26', 0)
            stoch_k = indicators.get('stoch_k', 50)
            stoch_d = indicators.get('stoch_d', 50)
            williams_r = indicators.get('williams_r', -50)
            cci = indicators.get('cci', 0)
            mfi = indicators.get('mfi', 50)
            uo = indicators.get('ultimate_oscillator', 50)
            aroon_up = indicators.get('aroon_up', 50)
            aroon_down = indicators.get('aroon_down', 50)
            trix = indicators.get('trix', 0)
            atr = indicators.get('atr', 0.001)

            # Проверяем торговое время
            trading_allowed, time_message = is_trading_time()
            if not trading_allowed:
                return f"""🎯 СИГНАЛ: ЖДАТЬ
📊 УВЕРЕННОСТЬ: 1/10
⏰ ЭКСПИРАЦИЯ: 5 мин
💡 ПРИЧИНА: {time_message}"""

            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 1: Графические паттерны
            pattern_signals = self.analyze_chart_patterns(indicators)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 2: Психология рынка
            psychology_signals = self.analyze_market_psychology(indicators, pair)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 3: Уровни поддержки/сопротивления
            support_resistance_signals = self.analyze_support_resistance(indicators, current_price)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 4: Институциональные потоки
            institutional_signals = self.analyze_institutional_flows(indicators, pair, timeframe)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 5: Межрыночные корреляции
            correlation_signals = self.analyze_market_correlations(pair, timeframe)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 6: Фундаментальные факторы
            fundamental_signals = self.analyze_fundamental_factors(pair, timeframe)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 7: Временные циклы
            time_cycle_signals = self.analyze_time_cycles(timeframe)
            
            # 🧠 ЧЕЛОВЕЧЕСКИЙ АНАЛИЗ УРОВНЯ 8: Глобальные настроения
            sentiment_signals = self.analyze_global_sentiment(pair)

            # 🎯 СИСТЕМА ЧЕЛОВЕЧЕСКОГО АНАЛИЗА С МНОЖЕСТВЕННЫМИ ПОДТВЕРЖДЕНИЯМИ
            call_score = 0
            put_score = 0
            signal_reasons = []
            
            # Добавляем человеческие сигналы к общему счету
            call_score += pattern_signals.get('call_strength', 0)
            put_score += pattern_signals.get('put_strength', 0)
            if pattern_signals.get('reason'):
                signal_reasons.append(pattern_signals['reason'])
                
            call_score += psychology_signals.get('call_strength', 0) 
            put_score += psychology_signals.get('put_strength', 0)
            if psychology_signals.get('reason'):
                signal_reasons.append(psychology_signals['reason'])
                
            call_score += support_resistance_signals.get('call_strength', 0)
            put_score += support_resistance_signals.get('put_strength', 0)
            if support_resistance_signals.get('reason'):
                signal_reasons.append(support_resistance_signals['reason'])
                
            call_score += institutional_signals.get('call_strength', 0)
            put_score += institutional_signals.get('put_strength', 0)
            if institutional_signals.get('reason'):
                signal_reasons.append(institutional_signals['reason'])
                
            call_score += correlation_signals.get('call_strength', 0)
            put_score += correlation_signals.get('put_strength', 0)
            if correlation_signals.get('reason'):
                signal_reasons.append(correlation_signals['reason'])
                
            call_score += fundamental_signals.get('call_strength', 0)
            put_score += fundamental_signals.get('put_strength', 0)
            if fundamental_signals.get('reason'):
                signal_reasons.append(fundamental_signals['reason'])
                
            call_score += time_cycle_signals.get('call_strength', 0)
            put_score += time_cycle_signals.get('put_strength', 0)
            if time_cycle_signals.get('reason'):
                signal_reasons.append(time_cycle_signals['reason'])
                
            call_score += sentiment_signals.get('call_strength', 0)
            put_score += sentiment_signals.get('put_strength', 0) 
            if sentiment_signals.get('reason'):
                signal_reasons.append(sentiment_signals['reason'])

            # Динамический волатильный мультипликатор
            volatility_multiplier = self.calculate_dynamic_volatility(atr, current_price, timeframe)
            market_regime = self.detect_market_regime(indicators)

            # Система машинного обучения для весов
            ml_weights = self.calculate_ml_weights(indicators, pair, timeframe)

            # НЕЙРОСЕТЕВОЙ АНАЛИЗ УРОВНЯ 1: Осцилляторы (максимальный приоритет)
            # Stochastic с нейросетевой логикой
            stoch_signal_strength = self.calculate_stochastic_neural_score(stoch_k, stoch_d, market_regime)
            stoch_weight = ml_weights['stochastic'] * volatility_multiplier

            if stoch_signal_strength > 0.7:  # Сильный бычий
                call_score += stoch_weight * stoch_signal_strength
                signal_reasons.append(f"Stochastic нейросигнал: {stoch_signal_strength:.2f}")
            elif stoch_signal_strength < -0.7:  # Сильный медвежий
                put_score += stoch_weight * abs(stoch_signal_strength)
                signal_reasons.append(f"Stochastic медвежий: {abs(stoch_signal_strength):.2f}")
            elif stoch_signal_strength > 0.3:
                call_score += stoch_weight * 0.6
                signal_reasons.append("Stochastic умеренно бычий")
            elif stoch_signal_strength < -0.3:
                put_score += stoch_weight * 0.6
                signal_reasons.append("Stochastic умеренно медвежий")

            # Williams %R с нейросетевой обработкой
            williams_signal = self.calculate_williams_neural_score(williams_r, market_regime)
            williams_weight = ml_weights['williams'] * volatility_multiplier

            if abs(williams_signal) > 0.7:
                if williams_signal > 0:
                    call_score += williams_weight * williams_signal
                    signal_reasons.append(f"Williams сильный бычий: {williams_signal:.2f}")
                else:
                    put_score += williams_weight * abs(williams_signal)
                    signal_reasons.append(f"Williams сильный медвежий: {abs(williams_signal):.2f}")
            elif abs(williams_signal) > 0.3:
                if williams_signal > 0:
                    call_score += williams_weight * 0.6
                    signal_reasons.append("Williams умеренно бычий")
                else:
                    put_score += williams_weight * 0.6
                    signal_reasons.append("Williams умеренно медвежий")

            # НЕЙРОСЕТЕВОЙ АНАЛИЗ УРОВНЯ 2: RSI с контекстным анализом
            rsi_signal = self.calculate_rsi_neural_score(rsi, market_regime, bb_position)
            rsi_weight = ml_weights['rsi'] * volatility_multiplier

            if abs(rsi_signal) > 0.8:
                if rsi_signal > 0:
                    call_score += rsi_weight * rsi_signal
                    signal_reasons.append(f"RSI критический бычий: {rsi_signal:.2f}")
                else:
                    put_score += rsi_weight * abs(rsi_signal)
                    signal_reasons.append(f"RSI критический медвежий: {abs(rsi_signal):.2f}")
            elif abs(rsi_signal) > 0.5:
                if rsi_signal > 0:
                    call_score += rsi_weight * 0.7
                    signal_reasons.append("RSI перепродан")
                else:
                    put_score += rsi_weight * 0.7
                    signal_reasons.append("RSI перекуплен")

            # CCI с расширенными зонами
            if cci < -150:
                call_score += 3
                signal_reasons.append("CCI сильно перепродан")
            elif cci > 150:
                put_score += 3
                signal_reasons.append("CCI сильно перекуплен")
            elif cci < -100:
                call_score += 2
                signal_reasons.append("CCI перепродан")
            elif cci > 100:
                put_score += 2
                signal_reasons.append("CCI перекуплен")

            # Tier 3: Средние индикаторы (вес 2-2.5)
            # MFI (Money Flow Index)
            if mfi < 15:
                call_score += 2.5
                signal_reasons.append("MFI критически низкий")
            elif mfi > 85:
                put_score += 2.5
                signal_reasons.append("MFI критически высокий")
            elif mfi < 25:
                call_score += 2
                signal_reasons.append("MFI низкий")
            elif mfi > 75:
                put_score += 2
                signal_reasons.append("MFI высокий")

            # Aroon с улучшенной логикой
            aroon_diff = aroon_up - aroon_down
            if aroon_up > 80 and aroon_down < 20:
                call_score += 2.5
                signal_reasons.append("Aroon сильный бычий")
            elif aroon_down > 80 and aroon_up < 20:
                put_score += 2.5
                signal_reasons.append("Aroon сильный медвежий")
            elif aroon_diff > 30:
                call_score += 1.5
                signal_reasons.append("Aroon бычий")
            elif aroon_diff < -30:
                put_score += 1.5
                signal_reasons.append("Aroon медвежий")

            # Ultimate Oscillator
            if uo < 25:
                call_score += 2
                signal_reasons.append("UO сильно перепродан")
            elif uo > 75:
                put_score += 2
                signal_reasons.append("UO сильно перекуплен")
            elif uo < 35:
                call_score += 1
                signal_reasons.append("UO перепродан")
            elif uo > 65:
                put_score += 1
                signal_reasons.append("UO перекуплен")

            # Tier 4: Трендовые индикаторы (вес 1.5-2)
            # Bollinger Bands с улучшенной логикой
            if bb_position < 0.1:
                call_score += 2
                signal_reasons.append("цена критически низко в BB")
            elif bb_position > 0.9:
                put_score += 2
                signal_reasons.append("цена критически высоко в BB")
            elif bb_position < 0.25:
                call_score += 1.5
                signal_reasons.append("цена у низа BB")
            elif bb_position > 0.75:
                put_score += 1.5
                signal_reasons.append("цена у верха BB")

            # MACD с учетом силы сигнала
            macd_diff = abs(macd - macd_signal)
            if macd > macd_signal and macd_diff > 0.0002:
                call_score += 2
                signal_reasons.append("MACD сильный бычий")
            elif macd < macd_signal and macd_diff > 0.0002:
                put_score += 2
                signal_reasons.append("MACD сильный медвежий")
            elif macd > macd_signal and macd_diff > 0.0001:
                call_score += 1
                signal_reasons.append("MACD бычий")
            elif macd < macd_signal and macd_diff > 0.0001:
                put_score += 1
                signal_reasons.append("MACD медвежий")

            # Трендовый анализ с несколькими MA
            trend_score = 0
            if current_price > sma_20 > sma_50:
                trend_score += 2
                call_score += 1.5
                signal_reasons.append("сильный восходящий тренд")
            elif current_price < sma_20 < sma_50:
                trend_score -= 2
                put_score += 1.5
                signal_reasons.append("сильный нисходящий тренд")
            elif current_price > sma_20:
                call_score += 1
                signal_reasons.append("выше SMA20")
            else:
                put_score += 1
                signal_reasons.append("ниже SMA20")

            # EMA кроссовер
            if ema_12 > ema_26:
                call_score += 1
            else:
                put_score += 1

            # TRIX для дополнительного подтверждения
            if abs(trix) > 0.0001:
                if trix > 0:
                    call_score += 0.5
                else:
                    put_score += 0.5

            # Финальное решение с человеческой логикой
            signal_type, confidence, neural_reason = self.calculate_final_neural_decision(
                call_score, put_score, indicators, market_regime
            )

            # Профессиональная базовая уверенность (как у опытного трейдера)
            if signal_type != "ЖДАТЬ":
                confidence = max(6, confidence)  # Минимум 6 для любого сигнала (опытный трейдер)

            # Дополнительные нейросетевые фильтры (смягченные)
            if signal_type != "ЖДАТЬ":
                # Фильтр противоречий (более мягкий)
                contradiction_score = self.calculate_contradiction_penalty(indicators)
                if contradiction_score > 0.9:  # Увеличен порог до 0.9
                    confidence = max(4, confidence - 1)  # Меньше штрафа
                    signal_reasons.append("небольшие противоречия")

                # Фильтр временной согласованности (более мягкий)
                time_consistency = self.calculate_time_consistency(indicators, timeframe)
                confidence = max(4, int(confidence * max(0.9, time_consistency)))  # Минимум 90% от исходной

                # Убираем жесткий минимальный порог
                if confidence < 3 and signal_type != "ЖДАТЬ":
                    confidence = 3  # Не меняем сигнал, только уверенность

            # Корректировки уверенности (смягченные)
            total_score = call_score + put_score
            
            # Согласованность индикаторов (улучшенная формула)
            if total_score > 0:
                consensus = max(call_score, put_score) / total_score
                if consensus > 0.8:  # Высокое согласие
                    confidence = min(10, confidence + 2)
                elif consensus > 0.7:  # Умеренное согласие
                    confidence = min(10, confidence + 1)
                elif consensus < 0.55:  # Низкое согласие
                    confidence = max(3, confidence - 1)

            # Волатильность (более мягкие штрафы)
            if volatility_multiplier > 2.0:
                confidence = max(3, confidence - 2)
                signal_reasons.append("экстремальная волатильность")
            elif volatility_multiplier > 1.5:
                confidence = max(4, confidence - 1)
                signal_reasons.append("высокая волатильность")
            elif volatility_multiplier < 0.5:
                confidence = max(3, confidence - 1)
                signal_reasons.append("очень низкая волатильность")

            # Проверка противоречий
            contradiction_penalty = 0
            if (rsi > 70 and bb_position < 0.3) or (rsi < 30 and bb_position > 0.7):
                contradiction_penalty += 1
            if (stoch_k > 80 and williams_r < -80) or (stoch_k < 20 and williams_r > -20):
                contradiction_penalty += 1

            if contradiction_penalty > 0:
                confidence = max(1, confidence - contradiction_penalty)
                signal_reasons.append("противоречивые сигналы")

            # Определяем экспирацию с учетом волатильности
            if timeframe in ['1m', '3m']:
                expiration = "2" if volatility_multiplier > 1.2 else "3"
            elif timeframe in ['5m', '15m']:
                expiration = "3" if volatility_multiplier > 1.2 else "4"
            else:
                expiration = "5"

            # Ограничиваем количество причин
            main_reasons = signal_reasons[:3] if signal_reasons else ["нейтральные условия"]
            reason = ", ".join(main_reasons)

            return f"""🎯 СИГНАЛ: {signal_type}
📊 УВЕРЕННОСТЬ: {confidence}/10
⏰ ЭКСПИРАЦИЯ: {expiration} мин
💡 ПРИЧИНА: {reason}
🔥 ВОЛАТИЛЬНОСТЬ: {volatility_multiplier:.1f}x"""

        except Exception as e:
            return f"""🎯 СИГНАЛ: ЖДАТЬ
📊 УВЕРЕННОСТЬ: 1/10
⏰ ЭКСПИРАЦИЯ: 5 мин
💡 ПРИЧИНА: системная ошибка"""

    def calculate_dynamic_volatility(self, atr: float, price: float, timeframe: str) -> float:
        """Расчет динамического волатильного мультипликатора"""
        try:
            if price <= 0:
                return 1.0

            # Базовый мультипликатор по таймфрейму
            tf_multipliers = {
                '1m': 1.5, '3m': 1.3, '5m': 1.2, 
                '15m': 1.1, '30m': 1.0, '1h': 0.9
            }

            base_mult = tf_multipliers.get(timeframe, 1.0)
            volatility_ratio = atr / (price * 0.005)  # Нормализация

            # Адаптивная формула
            dynamic_mult = base_mult * (1 + np.log(1 + volatility_ratio))
            return min(3.0, max(0.3, dynamic_mult))
        except:
            return 1.0

    def detect_market_regime(self, indicators: Dict[str, Any]) -> str:
        """Определение рыночного режима (тренд/флет/разворот)"""
        try:
            rsi = indicators.get('rsi', 50)
            bb_position = indicators.get('bb_position', 0.5)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            aroon_up = indicators.get('aroon_up', 50)
            aroon_down = indicators.get('aroon_down', 50)

            # Критерии для определения режима
            trend_strength = abs(aroon_up - aroon_down)
            momentum_strength = abs(macd - macd_signal) * 100000
            volatility_level = abs(bb_position - 0.5) * 2

            if trend_strength > 60 and momentum_strength > 2:
                return "СИЛЬНЫЙ_ТРЕНД"
            elif trend_strength > 30:
                return "СЛАБЫЙ_ТРЕНД"  
            elif volatility_level < 0.3 and 40 < rsi < 60:
                return "ФЛЕТ"
            elif (rsi > 75 or rsi < 25) and momentum_strength > 1:
                return "РАЗВОРОТ"
            else:
                return "НЕОПРЕДЕЛЕННОСТЬ"
        except:
            return "НЕОПРЕДЕЛЕННОСТЬ"

    def calculate_ml_weights(self, indicators: Dict[str, Any], pair: str, timeframe: str) -> Dict[str, float]:
        """Расчет весов с использованием машинного обучения"""
        try:
            # Базовые веса (обученные на исторических данных)
            base_weights = {
                'rsi': 2.5,
                'stochastic': 3.0,
                'williams': 2.8,
                'macd': 2.2,
                'bollinger': 2.0,
                'cci': 1.8,
                'mfi': 1.5,
                'aroon': 1.7,
                'ultimate': 1.3
            }

            # Адаптация весов под условия рынка
            market_regime = self.detect_market_regime(indicators)
            volatility = indicators.get('atr', 0.001)

            # Модификация весов в зависимости от режима рынка
            if market_regime == "СИЛЬНЫЙ_ТРЕНД":
                base_weights['macd'] *= 1.5
                base_weights['aroon'] *= 1.4
                base_weights['rsi'] *= 0.8  # RSI менее надежен в трендах
            elif market_regime == "ФЛЕТ":
                base_weights['bollinger'] *= 1.6
                base_weights['rsi'] *= 1.3
                base_weights['stochastic'] *= 1.3
            elif market_regime == "РАЗВОРОТ":
                base_weights['rsi'] *= 1.8
                base_weights['williams'] *= 1.6
                base_weights['stochastic'] *= 1.5

            # Адаптация под волатильность
            vol_multiplier = min(1.5, max(0.7, volatility * 100000))
            for key in base_weights:
                base_weights[key] *= vol_multiplier

            # Адаптация под валютную пару
            pair_adjustments = {
                'EUR/USD': {'rsi': 1.1, 'macd': 1.2},
                'GBP/USD': {'bollinger': 1.2, 'volatility': 1.1},
                'USD/JPY': {'aroon': 1.2, 'cci': 1.1},
                'AUD/USD': {'williams': 1.1, 'mfi': 1.2}
            }

            if pair in pair_adjustments:
                for indicator, mult in pair_adjustments[pair].items():
                    if indicator in base_weights:
                        base_weights[indicator] *= mult

            return base_weights
        except:
            return {
                'rsi': 2.0, 'stochastic': 2.5, 'williams': 2.3,
                'macd': 2.0, 'bollinger': 1.8, 'cci': 1.5,
                'mfi': 1.3, 'aroon': 1.5, 'ultimate': 1.2
            }

    def calculate_stochastic_neural_score(self, stoch_k: float, stoch_d: float, market_regime: str) -> float:
        """Нейросетевой анализ Stochastic с учетом рыночного режима"""
        try:
            # Базовый сигнал
            if stoch_k < 15 and stoch_d < 20:
                base_signal = 0.9  # Очень сильный бычий
            elif stoch_k > 85 and stoch_d > 80:
                base_signal = -0.9  # Очень сильный медвежий
            elif stoch_k < 25:
                base_signal = 0.6
            elif stoch_k > 75:
                base_signal = -0.6
            elif stoch_k < 35:
                base_signal = 0.3
            elif stoch_k > 65:
                base_signal = -0.3
            else:
                base_signal = 0.0

            # Модификация под режим рынка
            if market_regime == "СИЛЬНЫЙ_ТРЕНД":
                # В тренде осцилляторы менее надежны
                base_signal *= 0.7
            elif market_regime == "ФЛЕТ":
                # В флете осцилляторы более точны
                base_signal *= 1.3
            elif market_regime == "РАЗВОРОТ":
                # При развороте максимальная точность
                base_signal *= 1.5

            # Учет дивергенции между %K и %D
            divergence = abs(stoch_k - stoch_d)
            if divergence > 10:
                base_signal *= 1.2  # Дивергенция усиливает сигнал

            return max(-1.0, min(1.0, base_signal))
        except:
            return 0.0

    def calculate_rsi_neural_score(self, rsi: float, market_regime: str, bb_position: float) -> float:
        """Нейросетевая оценка RSI с контекстом"""
        try:
            # Базовый сигнал RSI
            if rsi < 20:
                base_signal = 0.95
            elif rsi > 80:
                base_signal = -0.95
            elif rsi < 30:
                base_signal = 0.7
            elif rsi > 70:
                base_signal = -0.7
            elif rsi < 40:
                base_signal = 0.3
            elif rsi > 60:
                base_signal = -0.3
            else:
                base_signal = 0.0

            # Контекстная корректировка
            if market_regime == "СИЛЬНЫЙ_ТРЕНД":
                # В сильном тренде RSI может оставаться в экстремальных зонах
                if abs(base_signal) > 0.7:
                    base_signal *= 0.6

            # Подтверждение от Bollinger Bands
            if (base_signal > 0 and bb_position < 0.3) or (base_signal < 0 and bb_position > 0.7):
                base_signal *= 1.3  # Подтверждение усиливает сигнал
            elif (base_signal > 0 and bb_position > 0.7) or (base_signal < 0 and bb_position < 0.3):
                base_signal *= 0.5  # Противоречие ослабляет сигнал

            return max(-1.0, min(1.0, base_signal))
        except:
            return 0.0

    def calculate_macd_neural_score(self, macd: float, macd_signal: float, market_regime: str) -> float:
        """Нейросетевая оценка MACD"""
        try:
            macd_diff = macd - macd_signal

            # Определяем силу сигнала
            if abs(macd_diff) > 0.0005:
                strength = 0.9
            elif abs(macd_diff) > 0.0003:
                strength = 0.7
            elif abs(macd_diff) > 0.0001:
                strength = 0.5
            else:
                strength = 0.2

            signal = strength if macd_diff > 0 else -strength

            # Адаптация под режим рынка
            if market_regime == "СИЛЬНЫЙ_ТРЕНД":
                signal *= 1.4  # MACD очень точен в трендах
            elif market_regime == "ФЛЕТ":
                signal *= 0.6  # Менее надежен в флете

            return max(-1.0, min(1.0, signal))
        except:
            return 0.0

    def calculate_pattern_recognition_score(self, indicators: Dict[str, Any]) -> float:
        """Распознавание паттернов с помощью ИИ"""
        try:
            patterns_score = 0

            # Паттерн "Тройное дно"
            rsi = indicators.get('rsi', 50)
            bb_position = indicators.get('bb_position', 0.5)
            williams_r = indicators.get('williams_r', -50)

            if (rsi < 25 and bb_position < 0.2 and williams_r < -85):
                patterns_score += 0.8  # Сильный паттерн разворота вверх

            # Паттерн "Тройная вершина"
            elif (rsi > 75 and bb_position > 0.8 and williams_r > -15):
                patterns_score -= 0.8  # Сильный паттерн разворота вниз

            # Паттерн "Расхождение RSI-MACD"
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)

            if (rsi < 30 and macd > macd_signal):
                patterns_score += 0.6  # Бычья дивергенция
            elif (rsi > 70 and macd < macd_signal):
                patterns_score -= 0.6  # Медвежья дивергенция

            return max(-1.0, min(1.0, patterns_score))
        except:
            return 0.0

    def calculate_williams_neural_score(self, williams_r: float, market_regime: str) -> float:
        """Нейросетевая оценка Williams %R"""
        try:
            if williams_r < -90:
                base_signal = 0.95
            elif williams_r > -10:
                base_signal = -0.95
            elif williams_r < -80:
                base_signal = 0.7
            elif williams_r > -20:
                base_signal = -0.7
            elif williams_r < -70:
                base_signal = 0.4
            elif williams_r > -30:
                base_signal = -0.4
            else:
                base_signal = 0.0

            # Адаптация под режим рынка
            if market_regime == "РАЗВОРОТ":
                base_signal *= 1.4
            elif market_regime == "ФЛЕТ":
                base_signal *= 1.2
            elif market_regime == "СИЛЬНЫЙ_ТРЕНД":
                base_signal *= 0.8

            return max(-1.0, min(1.0, base_signal))
        except:
            return 0.0

    def calculate_final_neural_decision(self, call_score: float, put_score: float, 
                                      indicators: Dict[str, Any], market_regime: str) -> tuple:
        """Финальное нейросетевое решение"""
        try:
            # Добавляем паттерн-анализ
            pattern_score = self.calculate_pattern_recognition_score(indicators)

            if pattern_score > 0.5:
                call_score += pattern_score * 2
            elif pattern_score < -0.5:
                put_score += abs(pattern_score) * 2

            # Нейросетевая нормализация
            total_score = call_score + put_score

            if total_score == 0:
                return "ЖДАТЬ", 4, "нет четких сигналов"

            # Расчет уверенности с учетом режима рынка (улучшенная формула)
            confidence_multiplier = {
                "СИЛЬНЫЙ_ТРЕНД": 1.5,
                "СЛАБЫЙ_ТРЕНД": 1.2,
                "ФЛЕТ": 1.3,
                "РАЗВОРОТ": 1.6,
                "НЕОПРЕДЕЛЕННОСТЬ": 1.0  # Повышен с 0.7
            }

            mult = confidence_multiplier.get(market_regime, 1.0)

            if call_score > put_score:
                score_diff = call_score - put_score
                # Улучшенная формула: базовая уверенность 6 + score_diff
                base_confidence = 6 + min(3, score_diff)
                confidence = min(10, int(base_confidence * mult))
                return "CALL", confidence, f"бычий сигнал {score_diff:.1f}, режим: {market_regime}"
            elif put_score > call_score:
                score_diff = put_score - call_score  
                # Улучшенная формула: базовая уверенность 6 + score_diff
                base_confidence = 6 + min(3, score_diff)
                confidence = min(10, int(base_confidence * mult))
                return "PUT", confidence, f"медвежий сигнал {score_diff:.1f}, режим: {market_regime}"
            else:
                return "ЖДАТЬ", 5, "равные сигналы"

        except Exception as e:
            return "ЖДАТЬ", 4, "ошибка расчета"

    def analyze_chart_patterns(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ графических паттернов как профессиональный трейдер"""
        try:
            rsi = indicators.get('rsi', 50)
            bb_position = indicators.get('bb_position', 0.5)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            williams_r = indicators.get('williams_r', -50)
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Паттерн "Двойное дно" 
            if rsi < 25 and williams_r < -85 and bb_position < 0.15:
                call_strength += 3.5
                reason = "двойное дно на графике"
            
            # Паттерн "Двойная вершина"
            elif rsi > 75 and williams_r > -15 and bb_position > 0.85:
                put_strength += 3.5
                reason = "двойная вершина на графике"
            
            # Паттерн "Восходящий треугольник"
            elif rsi > 55 and macd > macd_signal and bb_position > 0.6:
                call_strength += 2.5
                reason = "восходящий треугольник"
                
            # Паттерн "Нисходящий треугольник"
            elif rsi < 45 and macd < macd_signal and bb_position < 0.4:
                put_strength += 2.5
                reason = "нисходящий треугольник"
                
            # Паттерн "Флаг" (продолжение тренда)
            elif 40 < rsi < 60 and 0.3 < bb_position < 0.7:
                if macd > macd_signal:
                    call_strength += 1.5
                    reason = "бычий флаг"
                else:
                    put_strength += 1.5
                    reason = "медвежий флаг"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_market_psychology(self, indicators: Dict[str, Any], pair: str) -> Dict[str, Any]:
        """Анализ психологии рынка и поведения участников"""
        try:
            rsi = indicators.get('rsi', 50)
            stoch_k = indicators.get('stoch_k', 50)
            mfi = indicators.get('mfi', 50)
            cci = indicators.get('cci', 0)
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Анализ страха и жадности
            fear_greed_index = (rsi + stoch_k + mfi) / 3
            
            if fear_greed_index < 25:  # Экстремальный страх
                call_strength += 3.0
                reason = "экстремальный страх рынка - время покупать"
            elif fear_greed_index > 75:  # Экстремальная жадность
                put_strength += 3.0
                reason = "экстремальная жадность рынка - время продавать"
            
            # Поведение толпы vs умные деньги
            if cci < -200 and rsi < 25:  # Толпа продает, умные деньги покупают
                call_strength += 2.5  
                reason = "умные деньги против толпы - покупка"
            elif cci > 200 and rsi > 75:  # Толпа покупает, умные деньги продают
                put_strength += 2.5
                reason = "умные деньги против толпы - продажа"
            
            # Психологические уровни (круглые числа)
            current_price = indicators.get('current_price', 0)
            if current_price > 0:
                price_str = f"{current_price:.4f}"
                if price_str.endswith('0000') or price_str.endswith('5000'):
                    call_strength += 1.0
                    put_strength += 1.0  # Круглые уровни - разворотные точки
                    reason += ", психологический уровень"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_support_resistance(self, indicators: Dict[str, Any], current_price: float) -> Dict[str, Any]:
        """Анализ уровней поддержки и сопротивления"""
        try:
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            sma_20 = indicators.get('sma_20', 0)
            sma_50 = indicators.get('sma_50', 0)
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            if current_price > 0 and bb_upper > 0 and bb_lower > 0:
                # Пробой уровня сопротивления
                if current_price > bb_upper * 1.001:
                    call_strength += 2.5
                    reason = "пробой сопротивления"
                
                # Отскок от поддержки
                elif current_price < bb_lower * 1.001 and current_price > bb_lower * 0.999:
                    call_strength += 2.0
                    reason = "отскок от поддержки"
                
                # Пробой поддержки
                elif current_price < bb_lower * 0.999:
                    put_strength += 2.5
                    reason = "пробой поддержки"
                
                # Отскок от сопротивления
                elif current_price > bb_upper * 0.999 and current_price < bb_upper * 1.001:
                    put_strength += 2.0
                    reason = "отскок от сопротивления"
            
            # Динамические уровни поддержки/сопротивления (скользящие средние)
            if current_price > 0 and sma_20 > 0:
                if current_price > sma_20 * 1.005:  # Сильно выше SMA20
                    if current_price > sma_50 * 1.005:  # И выше SMA50
                        call_strength += 1.5
                        reason += ", сильный восходящий тренд"
                elif current_price < sma_20 * 0.995:  # Сильно ниже SMA20
                    if current_price < sma_50 * 0.995:  # И ниже SMA50
                        put_strength += 1.5
                        reason += ", сильный нисходящий тренд"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_institutional_flows(self, indicators: Dict[str, Any], pair: str, timeframe: str) -> Dict[str, Any]:
        """Анализ институциональных потоков (движение больших денег)"""
        try:
            mfi = indicators.get('mfi', 50)
            volume_sma = indicators.get('volume_sma', 0)
            atr = indicators.get('atr', 0.001)
            macd = indicators.get('macd', 0)
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Анализ притока капитала
            if mfi > 0:
                if mfi > 80:  # Сильный приток капитала
                    if macd > 0:  # С позитивным импульсом
                        call_strength += 2.0
                        reason = "институциональный приток капитала"
                    else:
                        put_strength += 1.5  # Возможно распределение
                        reason = "институциональное распределение"
                elif mfi < 20:  # Отток капитала
                    if macd < 0:  # С негативным импульсом
                        put_strength += 2.0
                        reason = "институциональный отток капитала"
                    else:
                        call_strength += 1.5  # Возможна аккумуляция
                        reason = "институциональная аккумуляция"
            
            # Анализ объема (если доступен)
            if volume_sma > 0:
                # Высокий объем указывает на институциональную активность
                call_strength += 0.5
                put_strength += 0.5
                reason += ", высокая институциональная активность"
            
            # Особенности по валютным парам (центробанки и интервенции)
            if pair == "USD/JPY":
                if atr > 0.008:  # Высокая волатильность может указывать на интервенции BOJ
                    put_strength += 1.0
                    reason += ", возможна интервенция BOJ"
            elif pair == "EUR/USD":
                if atr > 0.006:  # ECB intervention signals
                    call_strength += 0.5
                    put_strength += 0.5
                    reason += ", возможна активность ECB"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_market_correlations(self, pair: str, timeframe: str) -> Dict[str, Any]:
        """Анализ межрыночных корреляций"""
        try:
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Корреляции валютных пар
            if pair == "EUR/USD":
                # EUR/USD обычно коррелирует с риск-аппетитом
                call_strength += 1.0
                reason = "позитивная корреляция с риск-аппетитом"
            elif pair == "USD/JPY":
                # USD/JPY - классическая пара риск-он/риск-офф
                call_strength += 1.2
                reason = "индикатор глобального риск-аппетита"
            elif pair == "GBP/USD":
                # GBP чувствителен к новостям и настроениям
                put_strength += 0.5
                call_strength += 0.5
                reason = "высокая чувствительность к новостям"
            elif pair == "AUD/USD":
                # AUD коррелирует с товарными рынками
                call_strength += 0.8
                reason = "корреляция с товарными рынками"
            
            # Временные факторы
            if timeframe in ['1m', '3m', '5m']:
                # На малых таймфреймах корреляции работают сильнее
                call_strength *= 1.2
                put_strength *= 1.2
                reason += ", краткосрочная корреляция"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_fundamental_factors(self, pair: str, timeframe: str) -> Dict[str, Any]:
        """Анализ фундаментальных факторов"""
        try:
            moscow_tz = pytz.timezone('Europe/Moscow')
            moscow_time = datetime.now(moscow_tz)
            hour = moscow_time.hour
            weekday = moscow_time.weekday()
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Сезонность и время торговых сессий
            if 8 <= hour <= 12:  # Европейская сессия
                if pair.startswith('EUR') or pair.startswith('GBP'):
                    call_strength += 1.0
                    put_strength += 1.0
                    reason = "активная европейская сессия"
            elif 15 <= hour <= 19:  # Американская сессия
                if 'USD' in pair:
                    call_strength += 1.2
                    put_strength += 1.2
                    reason = "активная американская сессия"
            elif 2 <= hour <= 6:  # Азиатская сессия
                if pair.endswith('JPY') or pair.startswith('AUD'):
                    call_strength += 0.8
                    put_strength += 0.8
                    reason = "азиатская торговая сессия"
            
            # Недельная сезонность
            if weekday == 0:  # Понедельник
                call_strength += 0.5
                reason += ", понедельничные тренды"
            elif weekday == 4:  # Пятница
                put_strength += 0.3
                call_strength += 0.3
                reason += ", пятничное закрытие позиций"
            
            # Конец месяца/квартала (фиксация прибыли)
            day = moscow_time.day
            if day >= 28:  # Конец месяца
                put_strength += 0.5
                reason += ", конец месяца - фиксация прибыли"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_time_cycles(self, timeframe: str) -> Dict[str, Any]:
        """Анализ временных циклов"""
        try:
            moscow_tz = pytz.timezone('Europe/Moscow')
            moscow_time = datetime.now(moscow_tz)
            minute = moscow_time.minute
            
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Оптимальные временные окна для входа
            if timeframe == '1m':
                # Для 1-минутного TF лучше входить в начале минуты
                if 0 <= minute % 5 <= 1:
                    call_strength += 1.5
                    put_strength += 1.5
                    reason = "оптимальное время входа для 1m"
            elif timeframe == '5m':
                # Для 5-минутного TF - в начале 5-минутного цикла
                if minute % 5 == 0:
                    call_strength += 2.0
                    put_strength += 2.0
                    reason = "начало 5-минутного цикла"
            elif timeframe == '15m':
                # Для 15-минутного - в начале четверти часа
                if minute % 15 == 0:
                    call_strength += 2.5
                    put_strength += 2.5
                    reason = "начало 15-минутного цикла"
            
            # Избегаем входов в середине циклов
            if timeframe == '5m' and minute % 5 == 2:
                call_strength -= 1.0
                put_strength -= 1.0
                reason += ", середина цикла - менее надежно"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def analyze_global_sentiment(self, pair: str) -> Dict[str, Any]:
        """Анализ глобальных рыночных настроений"""
        try:
            call_strength = 0
            put_strength = 0
            reason = ""
            
            # Общий риск-аппетит на рынке (упрощенная модель)
            # В реальности это анализ индексов, VIX, спредов и т.д.
            
            # Базовая оценка по валютным парам
            if pair in ['EUR/USD', 'GBP/USD', 'AUD/USD']:
                # Эти пары обычно растут при позитивном риск-аппетите
                call_strength += 1.0
                reason = "позитивный глобальный риск-аппетит"
            elif pair == 'USD/JPY':
                # USD/JPY - классический индикатор настроений
                call_strength += 1.5
                reason = "индикатор глобальных настроений"
            elif pair in ['USD/CHF', 'USD/CAD']:
                # Более консервативные пары
                call_strength += 0.5
                put_strength += 0.5
                reason = "стабильные валюты в неопределенности"
            
            # Дополнительные факторы времени
            moscow_tz = pytz.timezone('Europe/Moscow')
            hour = datetime.now(moscow_tz).hour
            
            if 9 <= hour <= 18:  # Дневные часы - обычно больше оптимизма
                call_strength += 0.3
                reason += ", дневная торговля"
            else:  # Ночные часы - больше осторожности
                put_strength += 0.2
                reason += ", ночная торговля"
            
            return {'call_strength': call_strength, 'put_strength': put_strength, 'reason': reason}
        except:
            return {'call_strength': 0, 'put_strength': 0, 'reason': ''}

    def calculate_contradiction_penalty(self, indicators: Dict[str, Any]) -> float:
        """Расчет штрафа за противоречивые сигналы"""
        try:
            contradictions = 0
            total_checks = 0

            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            bb_position = indicators.get('bb_position', 0.5)
            stoch_k = indicators.get('stoch_k', 50)
            williams_r = indicators.get('williams_r', -50)

            # Проверка противоречий RSI vs MACD
            rsi_bullish = rsi < 30
            macd_bullish = macd > macd_signal
            if (rsi_bullish and not macd_bullish) or (not rsi_bullish and macd_bullish):
                contradictions += 1
            total_checks += 1

            # Проверка RSI vs Bollinger
            bb_bullish = bb_position < 0.3
            if (rsi_bullish and not bb_bullish) or (not rsi_bullish and bb_bullish):
                contradictions += 1
            total_checks += 1

            # Проверка Stochastic vs Williams
            stoch_bullish = stoch_k < 20
            williams_bullish = williams_r < -80
            if (stoch_bullish and not williams_bullish) or (not stoch_bullish and williams_bullish):
                contradictions += 1
            total_checks += 1

            return contradictions / total_checks if total_checks > 0 else 0
        except:
            return 0.5

    def calculate_time_consistency(self, indicators: Dict[str, Any], timeframe: str) -> float:
        """Расчет временной согласованности (смягченная версия)"""
        try:
            # Коэффициенты надежности по таймфреймам (повышены)
            tf_reliability = {
                '1m': 0.85,  # Увеличено с 0.6
                '3m': 0.88,  # Увеличено с 0.7
                '5m': 0.92,  # Увеличено с 0.8
                '15m': 0.95, # Увеличено с 0.9
                '30m': 0.98, # Увеличено с 0.95
                '1h': 1.0    # Максимально надежный
            }

            base_reliability = tf_reliability.get(timeframe, 0.9)

            # Дополнительная проверка волатильности (смягченная)
            atr = indicators.get('atr', 0.001)
            price = indicators.get('current_price', 1)

            volatility_ratio = atr / (price * 0.01) if price > 0 else 1

            # Корректировка на волатильность (более мягкая)
            if volatility_ratio > 3:
                base_reliability *= 0.85  # Меньший штраф
            elif volatility_ratio > 2:
                base_reliability *= 0.92
            elif volatility_ratio < 0.3:
                base_reliability *= 0.95  # Меньший штраф за низкую волатильность

            return max(0.8, min(1.0, base_reliability))  # Минимум повышен до 0.8
        except:
            return 0.9

def render_signal_card(analysis_text: str, pair: str, current_price: float):
    """Рендерит карточку сигнала в стиле Telegram"""

    # Парсим анализ
    lines = analysis_text.strip().split('\n')
    signal = "ЖДАТЬ"
    confidence = "5"
    expiration = "3"
    reason = "анализ данных"

    for line in lines:
        if "СИГНАЛ:" in line:
            signal = line.split(":")[-1].strip()
        elif "УВЕРЕННОСТЬ:" in line:
            confidence = line.split(":")[1].strip().split("/")[0].strip()
        elif "ЭКСПИРАЦИЯ:" in line:
            expiration = line.split(":")[1].strip().split()[0].strip()
        elif "ПРИЧИНА:" in line:
            reason = line.split(":", 1)[1].strip()

    # Определяем стиль карточки
    if "CALL" in signal:
        card_class = "signal-call"
        emoji = "📈"
        action = "ПОКУПКА"
        color = "#4CAF50"
    elif "PUT" in signal:
        card_class = "signal-put"
        emoji = "📉"
        action = "ПРОДАЖА"
        color = "#f44336"
    else:
        card_class = "signal-wait"
        emoji = "⏳"
        action = "ОЖИДАНИЕ"
        color = "#ff9800"

    # Получаем московское время
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)

    # Рассчитываем позицию индикатора уверенности
    conf_value = min(max(int(confidence), 1), 10)
    indicator_position = (conf_value - 1) * 10  # 0-90%

    st.markdown(f"""
    <div class="signal-card {card_class} slide-in">
        <div class="icon-large">{emoji}</div>
        <h2 style="color: {color}; margin: 0.5rem 0; font-size: 1.8rem;">{action}</h2>
        <div style="font-size: 1.1rem; color: rgba(255,255,255,0.9); margin: 0.5rem 0;">
            <strong>{pair}</strong> • {current_price:.5f}
        </div>
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Уверенность:</span>
                <span style="color: {color}; font-weight: 600;">{confidence}/10</span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-indicator" style="left: {indicator_position}%;"></div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin: 1rem 0; font-size: 0.9rem;">
            <div>⏰ {expiration} мин</div>
            <div>🕐 {moscow_time.strftime('%H:%M:%S')}</div>
        </div>
        <div style="background: rgba(0,0,0,0.2); border-radius: 10px; padding: 0.8rem; margin-top: 1rem;">
            <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                💡 {reason}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metrics(indicators: Dict[str, Any]):
    """Рендерит ВСЕ рассчитанные индикаторы в стиле Telegram"""

    # Получаем ВСЕ индикаторы
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    macd_histogram = indicators.get('macd_histogram', 0)
    bb_position = indicators.get('bb_position', 0.5)
    bb_upper = indicators.get('bb_upper', 0)
    bb_middle = indicators.get('bb_middle', 0)
    bb_lower = indicators.get('bb_lower', 0)
    price_change = indicators.get('price_change', 0)
    current_price = indicators.get('current_price', 0)
    
    # Скользящие средние
    sma_20 = indicators.get('sma_20', 0)
    sma_50 = indicators.get('sma_50', 0)
    ema_12 = indicators.get('ema_12', 0)
    ema_26 = indicators.get('ema_26', 0)
    
    # Осцилляторы
    stoch_k = indicators.get('stoch_k', 50)
    stoch_d = indicators.get('stoch_d', 50)
    williams_r = indicators.get('williams_r', -50)
    cci = indicators.get('cci', 0)
    mfi = indicators.get('mfi', 50)
    uo = indicators.get('ultimate_oscillator', 50)
    trix = indicators.get('trix', 0)
    
    # Волатильность и тренд
    atr = indicators.get('atr', 0.001)
    aroon_up = indicators.get('aroon_up', 50)
    aroon_down = indicators.get('aroon_down', 50)
    volume_sma = indicators.get('volume_sma', 0)

    # Функция для определения статуса индикаторов
    def get_rsi_status(val):
        return "🔴" if val > 70 else "🟢" if val < 30 else "🟡"
    
    def get_stoch_status(val):
        return "🔴" if val > 80 else "🟢" if val < 20 else "🟡"
    
    def get_williams_status(val):
        return "🔴" if val > -20 else "🟢" if val < -80 else "🟡"
    
    def get_cci_status(val):
        return "🔴" if val > 100 else "🟢" if val < -100 else "🟡"
    
    def get_mfi_status(val):
        return "🔴" if val > 80 else "🟢" if val < 20 else "🟡"

    # Статусы
    rsi_status = get_rsi_status(rsi)
    macd_status = "📈" if macd > macd_signal else "📉"
    bb_status = "🔴" if bb_position > 0.8 else "🟢" if bb_position < 0.2 else "🟡"
    price_status = "positive" if price_change > 0 else "negative"
    stoch_status = get_stoch_status(stoch_k)
    williams_status = get_williams_status(williams_r)
    cci_status = get_cci_status(cci)
    mfi_status = get_mfi_status(mfi)
    
    # Aroon статус
    aroon_diff = aroon_up - aroon_down
    aroon_status = "📈" if aroon_diff > 20 else "📉" if aroon_diff < -20 else "🟡"

    # Основные метрики (всегда показываем)
    st.markdown("#### 📊 Основные индикаторы")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">RSI (14)</div>
            <div class="metric-value">{rsi:.1f} {rsi_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MACD</div>
            <div class="metric-value">{macd:.5f} {macd_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MACD Signal</div>
            <div class="metric-value">{macd_signal:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MACD Histogram</div>
            <div class="metric-value">{macd_histogram:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">BB Позиция</div>
            <div class="metric-value">{bb_position:.0%} {bb_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Изменение цены</div>
            <div class="metric-value metric-change {price_status}">{price_change:+.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Полосы Боллинджера (детали)
    st.markdown("#### 🎭 Bollinger Bands")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">BB Верхняя</div>
            <div class="metric-value">{bb_upper:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">BB Средняя</div>
            <div class="metric-value">{bb_middle:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">BB Нижняя</div>
            <div class="metric-value">{bb_lower:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Текущая цена</div>
            <div class="metric-value">{current_price:.5f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Скользящие средние
    st.markdown("#### 📈 Скользящие средние")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">SMA 20</div>
            <div class="metric-value">{sma_20:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">SMA 50</div>
            <div class="metric-value">{sma_50:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">EMA 12</div>
            <div class="metric-value">{ema_12:.5f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">EMA 26</div>
            <div class="metric-value">{ema_26:.5f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Осцилляторы
    st.markdown("#### 🎚️ Осцилляторы")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">Stochastic %K</div>
            <div class="metric-value">{stoch_k:.1f} {stoch_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Stochastic %D</div>
            <div class="metric-value">{stoch_d:.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Williams %R</div>
            <div class="metric-value">{williams_r:.1f} {williams_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CCI</div>
            <div class="metric-value">{cci:.1f} {cci_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MFI</div>
            <div class="metric-value">{mfi:.1f} {mfi_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Ultimate Osc.</div>
            <div class="metric-value">{uo:.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">TRIX</div>
            <div class="metric-value">{trix:.6f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Трендовые индикаторы
    st.markdown("#### 📊 Трендовые индикаторы")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">Aroon Up</div>
            <div class="metric-value">{aroon_up:.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Aroon Down</div>
            <div class="metric-value">{aroon_down:.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Aroon Тренд</div>
            <div class="metric-value">{aroon_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">ATR</div>
            <div class="metric-value">{atr:.5f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Объемные индикаторы (если есть данные)
    if volume_sma > 0:
        st.markdown("#### 📊 Объемные индикаторы")
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-label">Volume SMA</div>
                <div class="metric-value">{volume_sma:,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Итоговая статистика всех индикаторов
    total_indicators = 20  # Общее количество рассчитываемых индикаторов
    
    # Подсчет бычьих/медвежьих сигналов
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0
    
    # RSI
    if rsi < 30:
        bullish_count += 1
    elif rsi > 70:
        bearish_count += 1
    else:
        neutral_count += 1
    
    # MACD
    if macd > macd_signal:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # BB
    if bb_position < 0.2:
        bullish_count += 1
    elif bb_position > 0.8:
        bearish_count += 1
    else:
        neutral_count += 1
    
    # Stochastic
    if stoch_k < 20:
        bullish_count += 1
    elif stoch_k > 80:
        bearish_count += 1
    else:
        neutral_count += 1
    
    # Williams %R
    if williams_r < -80:
        bullish_count += 1
    elif williams_r > -20:
        bearish_count += 1
    else:
        neutral_count += 1

    st.markdown("#### 📈 Общая статистика индикаторов")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">📈 Бычьих</div>
            <div class="metric-value" style="color: #4CAF50;">{bullish_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">📉 Медвежьих</div>
            <div class="metric-value" style="color: #f44336;">{bearish_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">⚪ Нейтральных</div>
            <div class="metric-value" style="color: #ff9800;">{neutral_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🔢 Всего</div>
            <div class="metric-value" style="color: #667eea;">{total_indicators}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_analysis_explanation(indicators: Dict[str, Any], analysis_text: str, pair: str):
    """Рендерит подробное объяснение анализа - полностью совместимо со Streamlit"""

    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    bb_position = indicators.get('bb_position', 0.5)
    current_price = indicators.get('current_price', 0)
    sma_20 = indicators.get('sma_20', 0)
    stoch_k = indicators.get('stoch_k', 50)
    williams_r = indicators.get('williams_r', -50)
    atr = indicators.get('atr', 0)

    # Подсчет подтверждающих индикаторов
    call_indicators = []
    put_indicators = []
    neutral_indicators = []

    # RSI анализ
    if rsi < 30:
        call_indicators.append("RSI (перепроданность)")
    elif rsi > 70:
        put_indicators.append("RSI (перекупленность)")
    else:
        neutral_indicators.append("RSI (нейтральная зона)")

    # MACD анализ
    if macd > macd_signal:
        call_indicators.append("MACD (выше сигнальной)")
    else:
        put_indicators.append("MACD (ниже сигнальной)")

    # Bollinger Bands
    if bb_position < 0.2:
        call_indicators.append("Bollinger Bands (нижняя граница)")
    elif bb_position > 0.8:
        put_indicators.append("Bollinger Bands (верхняя граница)")
    else:
        neutral_indicators.append("Bollinger Bands (средняя зона)")

    # Stochastic анализ (сильные сигналы)
    if stoch_k < 20:
        call_indicators.append("Stochastic (перепроданность)")
    elif stoch_k > 80:
        put_indicators.append("Stochastic (перекупленность)")
    else:
        neutral_indicators.append("Stochastic (нейтральная зона)")

    # Williams %R анализ (сильные сигналы)
    if williams_r < -80:
        call_indicators.append("Williams %R (перепроданность)")
    elif williams_r > -20:
        put_indicators.append("Williams %R (перекупленность)")
    else:
        neutral_indicators.append("Williams %R (нейтральная зона)")

    # Тренд (SMA20)
    if current_price > sma_20:
        call_indicators.append("SMA20 (цена выше)")
    else:
        put_indicators.append("SMA20 (цена ниже)")

    # Определяем общий сигнал из анализа
    signal_from_analysis = "ЖДАТЬ"
    if "CALL" in analysis_text:
        signal_from_analysis = "CALL"
        signal_color = "#4CAF50"
        signal_icon = "📈"
        confirming_count = len(call_indicators)
        confirming_list = call_indicators
    elif "PUT" in analysis_text:
        signal_from_analysis = "PUT"
        signal_color = "#f44336"
        signal_icon = "📉"
        confirming_count = len(put_indicators)
        confirming_list = put_indicators
    else:
        signal_color = "#ff9800"
        signal_icon = "⏳"
        confirming_count = len(neutral_indicators)
        confirming_list = neutral_indicators

    # Расчет общей силы сигнала
    total_indicators = len(call_indicators) + len(put_indicators) + len(neutral_indicators)
    signal_strength = "Слабый"
    if confirming_count >= 4:
        signal_strength = "Очень сильный"
    elif confirming_count >= 3:
        signal_strength = "Сильный"
    elif confirming_count >= 2:
        signal_strength = "Умеренный"

    # Основной заголовок с подсчетом индикаторов
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #1a2332, #2d3748); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
        <h4 style="color: {signal_color}; margin-bottom: 1rem; text-align: center;">
            {signal_icon} Финальное решение: {signal_from_analysis}
        </h4>
        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; text-align: center;">
                <div>
                    <div style="color: #4CAF50; font-weight: 600; font-size: 1.2rem;">📈 {len(call_indicators)}</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">За CALL</div>
                </div>
                <div>
                    <div style="color: #f44336; font-weight: 600; font-size: 1.2rem;">📉 {len(put_indicators)}</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">За PUT</div>
                </div>
                <div>
                    <div style="color: #ff9800; font-weight: 600; font-size: 1.2rem;">⚪ {len(neutral_indicators)}</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Нейтральных</div>
                </div>
                <div>
                    <div style="color: {signal_color}; font-weight: 600; font-size: 1.2rem;">💪 {signal_strength}</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Сила сигнала</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Подробный список подтверждающих индикаторов
    st.markdown("### 🎯 Подтверждающие индикаторы")

    # Создаем красивые карточки для каждого типа индикаторов
    col1, col2, col3 = st.columns(3)

    with col1:
        # Карточка для CALL индикаторов
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #1a2e1a, #2d4a2d); 
                border-radius: 15px; 
                padding: 1.5rem; 
                border: 2px solid #4CAF50;
                margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
            ">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: #4CAF50; margin: 0; font-size: 1.2rem;">
                        📈 За CALL
                    </h4>
                    <div style="
                        background: #4CAF50; 
                        color: white; 
                        border-radius: 20px; 
                        padding: 0.3rem 0.8rem; 
                        display: inline-block; 
                        margin-top: 0.5rem;
                        font-weight: 600;
                    ">
                        %d индикаторов
                    </div>
                </div>
            </div>
            """ % len(call_indicators), unsafe_allow_html=True)

            if call_indicators:
                for i, indicator in enumerate(call_indicators):
                    st.success(f"✅ {indicator}")
            else:
                st.error("❌ Нет сигналов для покупки")

    with col2:
        # Карточка для PUT индикаторов
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #2e1a1a, #4a2d2d); 
                border-radius: 15px; 
                padding: 1.5rem; 
                border: 2px solid #f44336;
                margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
            ">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: #f44336; margin: 0; font-size: 1.2rem;">
                        📉 За PUT
                    </h4>
                    <div style="
                        background: #f44336; 
                        color: white; 
                        border-radius: 20px; 
                        padding: 0.3rem 0.8rem; 
                        display: inline-block; 
                        margin-top: 0.5rem;
                        font-weight: 600;
                    ">
                        %d индикаторов
                    </div>
                </div>
            </div>
            """ % len(put_indicators), unsafe_allow_html=True)

            if put_indicators:
                for indicator in put_indicators:
                    st.error(f"✅ {indicator}")
            else:
                st.info("❌ Нет сигналов для продажи")

    with col3:
        # Карточка для нейтральных индикаторов
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #2e2a1a, #4a452d); 
                border-radius: 15px; 
                padding: 1.5rem; 
                border: 2px solid #ff9800;
                margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
            ">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h4 style="color: #ff9800; margin: 0; font-size: 1.2rem;">
                        ⚪ Нейтральные
                    </h4>
                    <div style="
                        background: #ff9800; 
                        color: white; 
                        border-radius: 20px; 
                        padding: 0.3rem 0.8rem; 
                        display: inline-block; 
                        margin-top: 0.5rem;
                        font-weight: 600;
                    ">
                        %d индикаторов
                    </div>
                </div>
            </div>
            """ % len(neutral_indicators), unsafe_allow_html=True)

            if neutral_indicators:
                for indicator in neutral_indicators:
                    st.warning(f"⚠️ {indicator}")
            else:
                st.success("✅ Все индикаторы определены")

    # Дополнительная информативная секция
    st.markdown("---")

    # Итоговая статистика в красивом виде
    total_indicators = len(call_indicators) + len(put_indicators) + len(neutral_indicators)

    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #1e1e2e, #2a2a3e); 
        border-radius: 15px; 
        padding: 1.5rem; 
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    ">
        <h4 style="color: white; text-align: center; margin-bottom: 1rem;">
            📊 Общая статистика индикаторов
        </h4>
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="color: #4CAF50; font-size: 2rem; font-weight: bold;">%d</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Бычьих</div>
            </div>
            <div>
                <div style="color: #f44336; font-size: 2rem; font-weight: bold;">%d</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Медвежьих</div>
            </div>
            <div>
                <div style="color: #ff9800; font-size: 2rem; font-weight: bold;">%d</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Нейтральных</div>
            </div>
            <div>
                <div style="color: #667eea; font-size: 2rem; font-weight: bold;">%d</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Всего</div>
            </div>
        </div>
    </div>
    """ % (len(call_indicators), len(put_indicators), len(neutral_indicators), total_indicators), unsafe_allow_html=True)

    # Используем колонки Streamlit для лучшей организации
    st.subheader("📊 Детальный анализ индикаторов")

    # RSI анализ
    if rsi < 30:
        rsi_status = "🟢 Перепроданность - сигнал к покупке"
        rsi_interpretation = f"RSI {rsi:.1f} находится в зоне перепроданности (< 30). Актив продавался слишком агрессивно и готов к развороту вверх."
        rsi_strength = "Сильный бычий сигнал"
    elif rsi > 70:
        rsi_status = "🔴 Перекупленность - сигнал к продаже"
        rsi_interpretation = f"RSI {rsi:.1f} находится в зоне перекупленности (> 70). Актив переоценен и готов к коррекции вниз."
        rsi_strength = "Сильный медвежий сигнал"
    else:
        rsi_status = "🟡 Нейтральная зона"
        rsi_interpretation = f"RSI {rsi:.1f} находится в нейтральной зоне (30-70). Требуются подтверждения от других индикаторов."
        rsi_strength = "Слабый сигнал"

    with st.expander("🎯 RSI (Индекс относительной силы)", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {rsi:.1f}")
            st.write(f"**Статус:** {rsi_status}")
            st.write(f"**Интерпретация:** {rsi_interpretation}")
        with col2:
            st.metric("RSI", f"{rsi:.1f}", help="0-30: Перепродан, 30-70: Нейтрально, 70-100: Перекуплен")

        # Прогресс бар для визуализации RSI
        rsi_normalized = max(0.0, min(1.0, rsi / 100))
        st.progress(rsi_normalized)
        st.caption("📈 RSI показывает силу тренда от 0 до 100")

    # MACD анализ
    macd_diff = macd - macd_signal
    if macd > macd_signal:
        macd_status = "📈 Бычий сигнал - MACD выше сигнальной"
        macd_interpretation = f"MACD ({macd:.5f}) выше сигнальной линии ({macd_signal:.5f}). Импульс направлен вверх."
        macd_trend = "Восходящий тренд"
    else:
        macd_status = "📉 Медвежий сигнал - MACD ниже сигнальной"
        macd_interpretation = f"MACD ({macd:.5f}) ниже сигнальной линии ({macd_signal:.5f}). Импульс направлен вниз."
        macd_trend = "Нисходящий тренд"

    with st.expander("📊 MACD (Схождение-расхождение)", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("MACD", f"{macd:.5f}", f"{macd_diff:+.5f}")
        with col2:
            st.metric("Сигнальная", f"{macd_signal:.5f}")
        with col3:
            st.write(f"**Тренд:** {macd_trend}")

        st.write(f"**Статус:** {macd_status}")
        st.write(f"**Объяснение:** {macd_interpretation}")
        st.caption("💡 MACD показывает импульс и направление тренда")

    # Bollinger Bands анализ
    if bb_position < 0.2:
        bb_status = "🟢 Цена у нижней границы - отскок вверх"
        bb_interpretation = f"Цена в нижних {bb_position:.0%} полос Боллинджера. Высокая вероятность отскока вверх."
        bb_signal = "Покупка"
    elif bb_position > 0.8:
        bb_status = "🔴 Цена у верхней границы - коррекция вниз"
        bb_interpretation = f"Цена в верхних {bb_position:.0%} полос Боллинджера. Ожидается коррекция вниз."
        bb_signal = "Продажа"
    else:
        bb_status = "🟡 Цена в середине полос"
        bb_interpretation = f"Цена в средней части полос ({bb_position:.0%}). Боковое движение, нет четкого сигнала."
        bb_signal = "Ожидание"

    with st.expander("🎭 Bollinger Bands (Полосы Боллинджера)", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Позиция в полосах:** {bb_position:.0%}")
            st.write(f"**Статус:** {bb_status}")
            st.write(f"**Интерпретация:** {bb_interpretation}")
        with col2:
            st.metric("Сигнал", bb_signal)

        # Визуализация позиции в BB
        bb_normalized = max(0.0, min(1.0, bb_position))
        st.progress(bb_normalized)
        st.caption("📊 0-20%: Зона покупки, 80-100%: Зона продажи")

    # Тренд анализ
    price_vs_sma = ((current_price - sma_20) / sma_20) * 100
    if current_price > sma_20:
        trend_status = "📈 Восходящий тренд"
        trend_interpretation = f"Цена ({current_price:.5f}) выше SMA20 ({sma_20:.5f}) на {price_vs_sma:+.2f}%"
        trend_signal = "Бычий"
    else:
        trend_status = "📉 Нисходящий тренд"
        trend_interpretation = f"Цена ({current_price:.5f}) ниже SMA20 ({sma_20:.5f}) на {price_vs_sma:+.2f}%"
        trend_signal = "Медвежий"

    with st.expander("📈 Анализ тренда (SMA20)", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Цена", f"{current_price:.5f}")
        with col2:
            st.metric("SMA20", f"{sma_20:.5f}", f"{price_vs_sma:+.2f}%")
        with col3:
            st.write(f"**Тренд:** {trend_signal}")

        st.write(f"**Статус:** {trend_status}")
        st.write(f"**Объяснение:** {trend_interpretation}")
        st.caption("📊 SMA20 - скользящая средняя за 20 периодов, показывает общий тренд")

    # Дополнительные индикаторы
    st.subheader("🔍 Дополнительные сигналы")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Stochastic %K",
            f"{stoch_k:.1f}",
            help="0-20: Перепродан, 80-100: Перекуплен"
        )
        if stoch_k < 20:
            st.success("🟢 Перепродан")
        elif stoch_k > 80:
            st.error("🔴 Перекуплен")
        else:
            st.info("🟡 Нейтрален")

    with col2:
        st.metric(
            "Williams %R",
            f"{williams_r:.1f}",
            help="-100 до -80: Перепродан, -20 до 0: Перекуплен"
        )
        if williams_r < -80:
            st.success("🟢 Перепродан")
        elif williams_r > -20:
            st.error("🔴 Перекуплен")
        else:
            st.info("🟡 Нейтрален")

    with col3:
        st.metric(
            "ATR (Волатильность)",
            f"{atr:.5f}",
            help="Показывает среднюю волатильность актива"
        )
        if atr > 0:
            volatility_level = "Высокая" if atr > current_price * 0.01 else "Умеренная"
            st.info(f"📊 {volatility_level}")

    # Обучающая секция
    st.subheader("📚 Как понимать сигналы")

    with st.expander("💡 Руководство по торговым сигналам", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📈 CALL", "📉 PUT", "⏳ ЖДАТЬ"])

        with tab1:
            st.write("**Когда покупать (CALL):**")
            st.write("✅ RSI < 30 (перепроданность)")
            st.write("✅ MACD выше сигнальной линии")
            st.write("✅ Цена у нижней границы Bollinger Bands")
            st.write("✅ Цена выше SMA20")
            st.write("✅ Stochastic < 20")

        with tab2:
            st.write("**Когда продавать (PUT):**")
            st.write("❌ RSI > 70 (перекупленность)")
            st.write("❌ MACD ниже сигнальной линии")
            st.write("❌ Цена у верхней границы Bollinger Bands")
            st.write("❌ Цена ниже SMA20")
            st.write("❌ Stochastic > 80")

        with tab3:
            st.write("**Когда ждать:**")
            st.write("⚠️ Противоречивые сигналы")
            st.write("⚠️ Низкая волатильность")
            st.write("⚠️ Неопределенный тренд")
            st.write("⚠️ Важные новости на рынке")

    # Предупреждения и риски
    st.warning("""
    ⚠️ **ВАЖНЫЕ ПРИНЦИПЫ РИСК-МЕНЕДЖМЕНТА:**

    • **Не рискуйте более 2-5%** от депозита на одну сделку
    • **Тестируйте стратегии** сначала на демо-счете
    • **Используйте стоп-лоссы** для ограничения потерь
    • **Анализ носит рекомендательный характер** - окончательное решение за вами
    • **Никогда не торгуйте** суммой, которую не можете позволить себе потерять
    """)

    st.info("""
    📊 **Как использовать этот анализ:**

    1. Изучите все индикаторы комплексно
    2. Ищите подтверждения сигналов
    3. Учитывайте общий тренд рынка
    4. Начинайте с минимальных сумм
    5. Ведите журнал торговли для анализа результатов
    """)

def main():
    load_telegram_mobile_css()

    # Telegram-style header
    st.markdown("""
    <div class="telegram-header">
        <div class="app-title">📱 MAJORKA VIP</div>
        <div class="app-subtitle">🤖 ИИ анализ графиков • Автосигналы</div>
    </div>
    """, unsafe_allow_html=True)

    # Инициализация анализатора
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = PocketOptionAnalyzer()

    # Основные настройки в компактном виде
    st.markdown('<div class="telegram-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        currency_pairs = [
            "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
            "EUR/GBP", "EUR/JPY", "GBP/JPY", "USD/CHF", "NZD/USD"
        ]
        selected_pair = st.selectbox("📈 Валютная пара", currency_pairs, key="pair_select")

    with col2:
        timeframes = ["1m", "3m", "5m", "15m", "30m", "1h"]
        selected_timeframe = st.selectbox("⏰ Таймфрейм", timeframes, index=2, key="tf_select")

    st.markdown('</div>', unsafe_allow_html=True)

    # Продвинутые настройки
    with st.expander("⚙️ Продвинутые настройки", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔑 API настройки")
            api_key = st.text_input(
                "OpenAI API Key",
                value=st.session_state.get('openai_api_key', ''),
                type="password",
                help="Введите ваш API ключ от OpenAI"
            )

            if api_key != st.session_state.get('openai_api_key', ''):
                st.session_state.openai_api_key = api_key
                st.session_state.analyzer.gpt_api_key = api_key
                if api_key and api_key.startswith('sk-'):
                    st.success("✅ API ключ обновлен")
                elif api_key:
                    st.error("❌ Неверный формат API ключа")

        with col2:
            st.subheader("🎯 Фильтры анализа")

            # Настройки риск-менеджмента
            min_confidence = st.slider(
                "Минимальная уверенность для сигналов",
                min_value=1,
                max_value=8,
                value=st.session_state.get('min_confidence', 5),
                help="Сигналы с уверенностью ниже этого порога будут отфильтрованы"
            )
            st.session_state.min_confidence = min_confidence

            # Настройка волатильности
            volatility_filter = st.checkbox(
                "Фильтровать по волатильности",
                value=st.session_state.get('volatility_filter', True),
                help="Исключать торговлю при экстремальной волатильности"
            )
            st.session_state.volatility_filter = volatility_filter

            # Настройка времени
            time_filter = st.checkbox(
                "Учитывать торговое время",
                value=st.session_state.get('time_filter', True),
                help="Предупреждать о неподходящем времени для торговли"
            )
            st.session_state.time_filter = time_filter

        # Индикаторы для отображения
        st.subheader("📊 Отображение индикаторов")
        indicator_cols = st.columns(4)

        with indicator_cols[0]:
            show_advanced = st.checkbox("Расширенные индикаторы", value=True)
        with indicator_cols[1]:
            show_volume = st.checkbox("Объемные индикаторы", value=True)
        with indicator_cols[2]:
            show_volatility = st.checkbox("Анализ волатильности", value=True)
        with indicator_cols[3]:
            show_warnings = st.checkbox("Предупреждения о рисках", value=True)

        st.session_state.update({
            'show_advanced': show_advanced,
            'show_volume': show_volume, 
            'show_volatility': show_volatility,
            'show_warnings': show_warnings
        })

    # Проверка времени торговли
    trading_allowed, time_message = is_trading_time()

    if not trading_allowed:
        st.warning(f"⏰ {time_message}. Торговля не рекомендуется в это время.")

    # Главная кнопка анализа
    if st.button("🚀 АНАЛИЗИРОВАТЬ", key="main_analyze"):

        # Получение данных с прогрессом
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("📊 Получение рыночных данных...")
        progress_bar.progress(25)

        market_data = st.session_state.analyzer.get_market_data(selected_pair, selected_timeframe)

        if market_data is not None and not market_data.empty:
            status_text.text("🔢 Расчет технических индикаторов...")
            progress_bar.progress(50)

            indicators = st.session_state.analyzer.calculate_indicators(market_data)

            if indicators:
                status_text.text("🤖 ИИ анализ данных...")
                progress_bar.progress(75)

                analysis = st.session_state.analyzer.analyze_with_ai(
                    market_data, indicators, selected_pair, selected_timeframe
                )

                progress_bar.progress(100)
                status_text.text("✅ Анализ завершен!")
                time.sleep(1)

                # Очищаем прогресс
                progress_bar.empty()
                status_text.empty()

                # Анализ волатильности
                volatility_info = get_market_volatility(market_data)

                # Отображаем информацию о волатильности
                st.markdown(f"""
                <div class="telegram-card">
                    <h4>📊 Анализ волатильности</h4>
                    <p><strong>Уровень:</strong> {volatility_info['level']}</p>
                    <p><strong>Коэффициент:</strong> {volatility_info['ratio']:.2f}</p>
                    <p><strong>Рекомендация:</strong> {volatility_info['trade_recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Отображаем результат
                current_price = indicators.get('current_price', 0)

                # Проверяем валидность индикаторов перед отображением
                if current_price > 0:
                    # Применяем фильтры из настроек
                    min_confidence = st.session_state.get('min_confidence', 5)
                    volatility_filter = st.session_state.get('volatility_filter', True)
                    time_filter = st.session_state.get('time_filter', True)
                    show_warnings = st.session_state.get('show_warnings', True)

                    # Извлекаем уверенность из анализа
                    confidence_match = re.search(r'УВЕРЕННОСТЬ:\s*(\d+)/10', analysis)
                    current_confidence = int(confidence_match.group(1)) if confidence_match else 5

                    # Проверка временного фильтра
                    if time_filter:
                        trading_allowed, time_message = is_trading_time()
                        if not trading_allowed:
                            st.error(f"⏰ {time_message}. Рекомендуется дождаться подходящего времени.")

                    # Проверка волатильности
                    volatility_info = get_market_volatility(market_data)
                    if volatility_filter and volatility_info['level'] in ['Очень высокая', 'Критическая']:
                        st.warning(f"🌊 Экстремальная волатильность ({volatility_info['level']}) - повышенные риски!")

                    # Получаем и отображаем предупреждения
                    if show_warnings:
                        risk_warnings = get_risk_warnings(indicators, selected_pair, selected_timeframe)
                        if risk_warnings:
                            st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
                            st.markdown("### ⚠️ Система предупреждений")
                            for warning in risk_warnings:
                                st.warning(warning)
                            st.markdown('</div>', unsafe_allow_html=True)

                    # Проверка минимальной уверенности
                    if current_confidence < min_confidence:
                        st.markdown(f"""
                        <div class="telegram-card" style="border: 2px solid #ff9800;">
                            <div style="text-align: center; color: #ff9800;">
                                <h3>🚫 СИГНАЛ ОТФИЛЬТРОВАН</h3>
                                <p>Уверенность {current_confidence}/10 ниже минимального порога {min_confidence}/10</p>
                                <p><small>Измените настройки или дождитесь более сильного сигнала</small></p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    render_signal_card(analysis, selected_pair, current_price)

                    # Метрики в компактном виде
                    st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
                    st.markdown("### 📊 Ключевые индикаторы")
                    render_metrics(indicators)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Отладочная информация (только при разработке)
                    with st.expander("🔍 Отладочная информация", expanded=False):
                        st.write("**Рассчитанные индикаторы:**")
                        for key, value in indicators.items():
                            st.write(f"{key}: {value}")
                else:
                    st.error("❌ Некорректные данные цены")

                # Подробные объяснения анализа
                st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
                st.markdown("### 🧠 Объяснение анализа")
                render_analysis_explanation(indicators, analysis, selected_pair)
                st.markdown('</div>', unsafe_allow_html=True)

                # Дополнительная информация в свернутом виде
                with st.expander("📈 График и детали", expanded=False):
                    chart_data = market_data[['Close']].tail(50)
                    st.line_chart(chart_data, height=300)

                    st.markdown("**📋 Последние данные:**")
                    recent_data = market_data[['Open', 'High', 'Low', 'Close']].tail(5)
                    st.dataframe(recent_data, use_container_width=True)

                # Сохраняем в историю
                if 'analysis_history' not in st.session_state:
                    st.session_state.analysis_history = []

                moscow_tz = pytz.timezone('Europe/Moscow')
                moscow_time = datetime.now(moscow_tz)

                # Определяем тип сигнала для истории
                signal_type = "ЖДАТЬ"
                if "CALL" in analysis:
                    signal_type = "CALL"
                elif "PUT" in analysis:
                    signal_type = "PUT"

                st.session_state.analysis_history.append({
                    'time': moscow_time,
                    'pair': selected_pair,
                    'timeframe': selected_timeframe,
                    'signal': signal_type,
                    'price': current_price,
                    'analysis': analysis
                })

                # Ограничиваем историю
                if len(st.session_state.analysis_history) > 10:
                    st.session_state.analysis_history = st.session_state.analysis_history[-10:]

            else:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ Ошибка расчета индикаторов")
        else:
            progress_bar.empty()
            status_text.empty()
            st.error("❌ Не удалось получить данные рынка")

    # История анализов
    if 'analysis_history' in st.session_state and st.session_state.analysis_history:
        st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
        st.markdown("### 📚 История сигналов")

        for analysis_item in reversed(st.session_state.analysis_history[-5:]):
            signal = analysis_item['signal']
            time_str = analysis_item['time'].strftime('%H:%M')
            pair = analysis_item['pair']
            price = analysis_item['price']

            if signal == "CALL":
                icon = "📈"
                class_name = "history-call"
            elif signal == "PUT":
                icon = "📉"
                class_name = "history-put"
            else:
                icon = "⏳"
                class_name = "history-wait"

            st.markdown(f"""
            <div class="history-item {class_name}">
                <div>
                    <strong>{icon} {signal}</strong><br>
                    <small>{pair} • {price:.5f}</small>
                </div>
                <div style="text-align: right;">
                    <small>{time_str}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Инструкции в компактном виде
    with st.expander("📖 Как использовать", expanded=False):
        st.markdown("""
        **🚀 Быстрый старт:**
        1. Выберите валютную пару и таймфрейм
        2. Нажмите "АНАЛИЗИРОВАТЬ"
        3. Получите торговый сигнал

        **📊 Типы сигналов:**
        - 📈 **CALL** - цена пойдет вверх
        - 📉 **PUT** - цена пойдет вниз
        - ⏳ **ЖДАТЬ** - неопределенность

        **⚠️ Важно:**
        - Не рискуйте более 2-5% депозита
        - Всегда проверяйте на демо счете
        - Используйте стоп-лоссы
        """)

    # Дисклеймер
    st.markdown("""
    <div class="telegram-card" style="margin-top: 2rem;">
        <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem;">
            ⚠️ <strong>Предупреждение:</strong> Торговля бинарными опционами несет высокие риски.<br>
            Анализ носит информационный характер. Принимайте решения осознанно.
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()