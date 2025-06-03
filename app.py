import streamlit as st
import time
import io
import base64
from datetime import datetime
import pytz
import requests
import json
import pandas as pd
import numpy as np
from typing import Dict, Any
import yfinance as yf
import ta

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

class PocketOptionAnalyzer:
    def __init__(self):
        self.gpt_api_key = None
        if 'openai_api_key' in st.session_state:
            self.gpt_api_key = st.session_state.openai_api_key

    def get_market_data(self, pair: str, timeframe: str) -> pd.DataFrame:
        """Получает данные рынка через Yahoo Finance с улучшенной обработкой - минимум 500 свечей"""
        try:
            if "/" in pair:
                symbol = pair.replace("/", "") + "=X"
            else:
                symbol = pair

            # Увеличиваем периоды для получения минимум 500 свечей
            period_map = {
                "1m": "5d", "3m": "10d", "5m": "1mo", "15m": "2mo",
                "30m": "3mo", "1h": "6mo", "4h": "1y", "1d": "2y"
            }

            interval_map = {
                "1m": "1m", "3m": "5m", "5m": "5m", "15m": "15m",
                "30m": "30m", "1h": "1h", "4h": "1h", "1d": "1d"
            }

            period = period_map.get(timeframe, "6mo")
            interval = interval_map.get(timeframe, "1h")

            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if data.empty:
                st.error(f"❌ Не удалось получить данные для {pair}")
                return None

            # Проверяем на валидность данных и убираем бесконечные значения
            data = data.replace([np.inf, -np.inf], np.nan)
            data = data.dropna()

            # Проверяем наличие основных колонок
            required_columns = ['Open', 'High', 'Low', 'Close']
            if not all(col in data.columns for col in required_columns):
                st.error(f"❌ Неполные данные для {pair}")
                return None

            # Проверяем достаточность данных - требуем минимум 500 свечей
            if len(data) < 500:
                st.warning(f"⚠️ Получено {len(data)} свечей для {pair}. Рекомендуется минимум 500 для точного анализа.")
                if len(data) < 100:
                    st.error(f"❌ Критически мало данных для анализа {pair}")
                    return None

            # Дополнительная валидация данных
            if data['Close'].isna().all() or (data['Close'] <= 0).all():
                st.error(f"❌ Некорректные ценовые данные для {pair}")
                return None

            # Сортируем по времени для корректности
            data = data.sort_index()

            return data

        except Exception as e:
            st.error(f"❌ Ошибка получения данных: {str(e)}")
            return None

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Рассчитывает расширенные технические индикаторы - 15+ индикаторов"""
        try:
            indicators = {}

            # Проверяем достаточность данных для всех индикаторов
            if len(df) < 200:
                st.warning(f"⚠️ Получено {len(df)} свечей. Для точного расчета всех 15+ индикаторов рекомендуется минимум 500 свечей.")
            
            st.info(f"📊 Анализируем {len(df)} свечей для максимальной точности")

            # RSI с проверкой
            try:
                rsi_indicator = ta.momentum.RSIIndicator(df['Close'])
                rsi_value = rsi_indicator.rsi().iloc[-1]
                indicators['rsi'] = rsi_value if not pd.isna(rsi_value) else 50
            except:
                indicators['rsi'] = 50

            # MFI (Money Flow Index) - НОВЫЙ
            try:
                mfi_indicator = ta.volume.MFIIndicator(df['High'], df['Low'], df['Close'], df['Volume'] if 'Volume' in df.columns else df['Close'])
                mfi_value = mfi_indicator.money_flow_index().iloc[-1]
                indicators['mfi'] = mfi_value if not pd.isna(mfi_value) else 50
            except:
                indicators['mfi'] = 50

            # CCI (Commodity Channel Index) - НОВЫЙ
            try:
                cci_indicator = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close'])
                cci_value = cci_indicator.cci().iloc[-1]
                indicators['cci'] = cci_value if not pd.isna(cci_value) else 0
            except:
                indicators['cci'] = 0

            # ADX (Average Directional Index) - НОВЫЙ
            try:
                adx_indicator = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'])
                adx_value = adx_indicator.adx().iloc[-1]
                indicators['adx'] = adx_value if not pd.isna(adx_value) else 25
            except:
                indicators['adx'] = 25

            # Parabolic SAR - НОВЫЙ
            try:
                psar_indicator = ta.trend.PSARIndicator(df['High'], df['Low'], df['Close'])
                psar_value = psar_indicator.psar().iloc[-1]
                indicators['psar'] = psar_value if not pd.isna(psar_value) else df['Close'].iloc[-1]
            except:
                indicators['psar'] = df['Close'].iloc[-1]

            # Ultimate Oscillator - НОВЫЙ
            try:
                uo_indicator = ta.momentum.UltimateOscillator(df['High'], df['Low'], df['Close'])
                uo_value = uo_indicator.ultimate_oscillator().iloc[-1]
                indicators['ultimate_oscillator'] = uo_value if not pd.isna(uo_value) else 50
            except:
                indicators['ultimate_oscillator'] = 50

            # Aroon Oscillator - НОВЫЙ ИНДИКАТОР
            try:
                aroon_indicator = ta.trend.AroonIndicator(df['High'], df['Low'])
                aroon_up = aroon_indicator.aroon_up().iloc[-1]
                aroon_down = aroon_indicator.aroon_down().iloc[-1]
                aroon_oscillator = aroon_up - aroon_down
                indicators['aroon_up'] = aroon_up if not pd.isna(aroon_up) else 50
                indicators['aroon_down'] = aroon_down if not pd.isna(aroon_down) else 50
                indicators['aroon_oscillator'] = aroon_oscillator if not pd.isna(aroon_oscillator) else 0
            except:
                indicators['aroon_up'] = 50
                indicators['aroon_down'] = 50
                indicators['aroon_oscillator'] = 0

            # Keltner Channel - НОВЫЙ ИНДИКАТОР
            try:
                keltner = ta.volatility.KeltnerChannel(df['High'], df['Low'], df['Close'])
                kc_upper = keltner.keltner_channel_hband().iloc[-1]
                kc_middle = keltner.keltner_channel_mband().iloc[-1]
                kc_lower = keltner.keltner_channel_lband().iloc[-1]
                indicators['kc_upper'] = kc_upper if not pd.isna(kc_upper) else df['Close'].iloc[-1] * 1.02
                indicators['kc_middle'] = kc_middle if not pd.isna(kc_middle) else df['Close'].iloc[-1]
                indicators['kc_lower'] = kc_lower if not pd.isna(kc_lower) else df['Close'].iloc[-1] * 0.98
                
                # Позиция в Keltner Channel
                if indicators['kc_upper'] != indicators['kc_lower']:
                    indicators['kc_position'] = (df['Close'].iloc[-1] - indicators['kc_lower']) / (indicators['kc_upper'] - indicators['kc_lower'])
                else:
                    indicators['kc_position'] = 0.5
            except:
                indicators['kc_upper'] = df['Close'].iloc[-1] * 1.02
                indicators['kc_middle'] = df['Close'].iloc[-1]
                indicators['kc_lower'] = df['Close'].iloc[-1] * 0.98
                indicators['kc_position'] = 0.5

            # TSI (True Strength Index) - НОВЫЙ ИНДИКАТОР
            try:
                tsi_indicator = ta.momentum.TSIIndicator(df['Close'])
                tsi_value = tsi_indicator.tsi().iloc[-1]
                indicators['tsi'] = tsi_value if not pd.isna(tsi_value) else 0
            except:
                indicators['tsi'] = 0

            # VWAP (Volume Weighted Average Price) - НОВЫЙ ИНДИКАТОР
            try:
                if 'Volume' in df.columns and not df['Volume'].isna().all():
                    vwap_indicator = ta.volume.VolumeSMAIndicator(df['Close'], df['Volume'])
                    vwap_value = vwap_indicator.volume_sma().iloc[-1]
                    indicators['vwap'] = vwap_value if not pd.isna(vwap_value) else df['Close'].iloc[-1]
                else:
                    indicators['vwap'] = df['Close'].iloc[-1]
            except:
                indicators['vwap'] = df['Close'].iloc[-1]

            # ROC (Rate of Change) - НОВЫЙ ИНДИКАТОР
            try:
                roc_indicator = ta.momentum.ROCIndicator(df['Close'], window=min(12, len(df)-1))
                roc_value = roc_indicator.roc().iloc[-1]
                indicators['roc'] = roc_value if not pd.isna(roc_value) else 0
            except:
                indicators['roc'] = 0

            # Ichimoku Cloud - НОВЫЙ ИНДИКАТОР
            try:
                ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'])
                ichimoku_a = ichimoku.ichimoku_a().iloc[-1]
                ichimoku_b = ichimoku.ichimoku_b().iloc[-1]
                indicators['ichimoku_a'] = ichimoku_a if not pd.isna(ichimoku_a) else df['Close'].iloc[-1]
                indicators['ichimoku_b'] = ichimoku_b if not pd.isna(ichimoku_b) else df['Close'].iloc[-1]
                
                # Позиция относительно облака
                current_price = df['Close'].iloc[-1]
                if current_price > max(ichimoku_a, ichimoku_b):
                    indicators['ichimoku_position'] = 1  # Выше облака
                elif current_price < min(ichimoku_a, ichimoku_b):
                    indicators['ichimoku_position'] = -1  # Ниже облака
                else:
                    indicators['ichimoku_position'] = 0  # В облаке
            except:
                indicators['ichimoku_a'] = df['Close'].iloc[-1]
                indicators['ichimoku_b'] = df['Close'].iloc[-1]
                indicators['ichimoku_position'] = 0

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
        """ПОЛНОСТЬЮ переработанный анализ с использованием всех 15+ индикаторов"""
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
            
            # Расширенные индикаторы
            mfi = indicators.get('mfi', 50)
            cci = indicators.get('cci', 0)
            adx = indicators.get('adx', 25)
            psar = indicators.get('psar', current_price)
            ultimate_oscillator = indicators.get('ultimate_oscillator', 50)
            aroon_up = indicators.get('aroon_up', 50)
            aroon_down = indicators.get('aroon_down', 50)
            aroon_oscillator = indicators.get('aroon_oscillator', 0)
            kc_position = indicators.get('kc_position', 0.5)
            tsi = indicators.get('tsi', 0)
            vwap = indicators.get('vwap', current_price)
            roc = indicators.get('roc', 0)
            ichimoku_position = indicators.get('ichimoku_position', 0)

            # Система подсчета сигналов с весами (максимум 100 баллов)
            call_score = 0
            put_score = 0
            signal_reasons = []
            total_weight = 0

            # 1. RSI - Ключевой осциллятор (вес 8)
            total_weight += 8
            if rsi < 25:
                call_score += 8
                signal_reasons.append("RSI экстремально перепродан")
            elif rsi < 35:
                call_score += 6
                signal_reasons.append("RSI перепродан")
            elif rsi > 75:
                put_score += 8
                signal_reasons.append("RSI экстремально перекуплен")
            elif rsi > 65:
                put_score += 6
                signal_reasons.append("RSI перекуплен")

            # 2. Stochastic - Ключевой осциллятор (вес 7)
            total_weight += 7
            if stoch_k < 15 and stoch_d < 15:
                call_score += 7
                signal_reasons.append("Stochastic экстремально перепродан")
            elif stoch_k < 25:
                call_score += 5
                signal_reasons.append("Stochastic перепродан")
            elif stoch_k > 85 and stoch_d > 85:
                put_score += 7
                signal_reasons.append("Stochastic экстремально перекуплен")
            elif stoch_k > 75:
                put_score += 5
                signal_reasons.append("Stochastic перекуплен")

            # 3. Williams %R - Ключевой осциллятор (вес 7)
            total_weight += 7
            if williams_r < -85:
                call_score += 7
                signal_reasons.append("Williams %R экстремально перепродан")
            elif williams_r < -75:
                call_score += 5
                signal_reasons.append("Williams %R перепродан")
            elif williams_r > -15:
                put_score += 7
                signal_reasons.append("Williams %R экстремально перекуплен")
            elif williams_r > -25:
                put_score += 5
                signal_reasons.append("Williams %R перекуплен")

            # 4. MFI - Денежный поток (вес 6)
            total_weight += 6
            if mfi < 15:
                call_score += 6
                signal_reasons.append("MFI экстремально перепродан")
            elif mfi < 25:
                call_score += 4
                signal_reasons.append("MFI перепродан")
            elif mfi > 85:
                put_score += 6
                signal_reasons.append("MFI экстремально перекуплен")
            elif mfi > 75:
                put_score += 4
                signal_reasons.append("MFI перекуплен")

            # 5. CCI - Канальный индекс (вес 6)
            total_weight += 6
            if cci < -150:
                call_score += 6
                signal_reasons.append("CCI экстремально перепродан")
            elif cci < -100:
                call_score += 4
                signal_reasons.append("CCI перепродан")
            elif cci > 150:
                put_score += 6
                signal_reasons.append("CCI экстремально перекуплен")
            elif cci > 100:
                put_score += 4
                signal_reasons.append("CCI перекуплен")

            # 6. Ultimate Oscillator - Составной осциллятор (вес 5)
            total_weight += 5
            if ultimate_oscillator < 25:
                call_score += 5
                signal_reasons.append("UO перепродан")
            elif ultimate_oscillator > 75:
                put_score += 5
                signal_reasons.append("UO перекуплен")

            # 7. TSI - Истинная сила (вес 5)
            total_weight += 5
            if tsi < -20:
                call_score += 5
                signal_reasons.append("TSI медвежий экстремум")
            elif tsi > 20:
                put_score += 5
                signal_reasons.append("TSI бычий экстремум")

            # 8. Aroon Oscillator - Трендовый индикатор (вес 4)
            total_weight += 4
            if aroon_oscillator > 70:
                call_score += 4
                signal_reasons.append("Aroon сильный восходящий тренд")
            elif aroon_oscillator < -70:
                put_score += 4
                signal_reasons.append("Aroon сильный нисходящий тренд")

            # 9. MACD - Трендовый индикатор (вес 4)
            total_weight += 4
            macd_diff = macd - macd_signal
            if macd > macd_signal and macd_diff > 0.0001:
                if macd > 0:
                    call_score += 4
                    signal_reasons.append("MACD сильный бычий")
                else:
                    call_score += 2
                    signal_reasons.append("MACD слабый бычий")
            elif macd < macd_signal and abs(macd_diff) > 0.0001:
                if macd < 0:
                    put_score += 4
                    signal_reasons.append("MACD сильный медвежий")
                else:
                    put_score += 2
                    signal_reasons.append("MACD слабый медвежий")

            # 10. ROC - Скорость изменения (вес 3)
            total_weight += 3
            if roc > 2:
                call_score += 3
                signal_reasons.append("ROC сильный рост")
            elif roc < -2:
                put_score += 3
                signal_reasons.append("ROC сильное падение")

            # 11. Bollinger Bands - Волатильность (вес 6)
            total_weight += 6
            if bb_position < 0.1:
                call_score += 6
                signal_reasons.append("BB экстремально низ")
            elif bb_position < 0.25:
                call_score += 4
                signal_reasons.append("BB нижняя граница")
            elif bb_position > 0.9:
                put_score += 6
                signal_reasons.append("BB экстремально верх")
            elif bb_position > 0.75:
                put_score += 4
                signal_reasons.append("BB верхняя граница")

            # 12. Keltner Channel - Альтернативная волатильность (вес 4)
            total_weight += 4
            if kc_position < 0.15:
                call_score += 4
                signal_reasons.append("KC нижняя граница")
            elif kc_position > 0.85:
                put_score += 4
                signal_reasons.append("KC верхняя граница")

            # 13. Parabolic SAR - Тренд и развороты (вес 3)
            total_weight += 3
            psar_diff = abs(current_price - psar) / current_price
            if current_price > psar and psar_diff > 0.001:
                call_score += 3
                signal_reasons.append("PSAR бычий тренд")
            elif current_price < psar and psar_diff > 0.001:
                put_score += 3
                signal_reasons.append("PSAR медвежий тренд")

            # 14. Ichimoku Cloud - Комплексный анализ (вес 5)
            total_weight += 5
            if ichimoku_position == 1:
                call_score += 5
                signal_reasons.append("Ichimoku выше облака")
            elif ichimoku_position == -1:
                put_score += 5
                signal_reasons.append("Ichimoku ниже облака")

            # 15. ADX - Сила тренда (вес 3)
            total_weight += 3
            if adx > 35:
                # Сильный тренд - усиливаем основной сигнал
                if call_score > put_score:
                    call_score += 3
                    signal_reasons.append("ADX сильный тренд")
                elif put_score > call_score:
                    put_score += 3
                    signal_reasons.append("ADX сильный тренд")

            # 16. VWAP - Объемный анализ (вес 2)
            total_weight += 2
            vwap_diff = (current_price - vwap) / vwap
            if vwap_diff > 0.005:
                call_score += 2
                signal_reasons.append("цена выше VWAP")
            elif vwap_diff < -0.005:
                put_score += 2
                signal_reasons.append("цена ниже VWAP")

            # 17. Скользящие средние - Базовый тренд (вес 4)
            total_weight += 4
            ma_signals = 0
            if current_price > sma_20:
                ma_signals += 1
            if current_price > sma_50:
                ma_signals += 1
            if ema_12 > ema_26:
                ma_signals += 1
            if sma_20 > sma_50:
                ma_signals += 1
            
            if ma_signals >= 3:
                call_score += 4
                signal_reasons.append("MA восходящий тренд")
            elif ma_signals <= 1:
                put_score += 4
                signal_reasons.append("MA нисходящий тренд")

            # Продвинутый расчет финального сигнала на основе всех индикаторов
            if total_weight == 0:
                total_weight = 1  # Избегаем деления на ноль
            
            # Нормализуем счет по максимально возможному весу
            call_percentage = (call_score / total_weight) * 100
            put_percentage = (put_score / total_weight) * 100
            
            # Определяем силу сигнала
            signal_strength = max(call_percentage, put_percentage)
            
            # Финальное решение на основе процентного превосходства
            score_difference = abs(call_score - put_score)
            percentage_difference = abs(call_percentage - put_percentage)
            
            if percentage_difference < 5:  # Слишком близкие сигналы
                signal_type = "ЖДАТЬ"
                confidence = max(2, min(4, int(signal_strength / 10)))
            elif call_score > put_score:
                signal_type = "CALL"
                # Более точный расчет уверенности
                if signal_strength > 50:
                    confidence = min(10, 7 + int(percentage_difference / 10))
                elif signal_strength > 30:
                    confidence = min(8, 5 + int(percentage_difference / 15))
                else:
                    confidence = min(6, 3 + int(percentage_difference / 20))
            elif put_score > call_score:
                signal_type = "PUT"
                if signal_strength > 50:
                    confidence = min(10, 7 + int(percentage_difference / 10))
                elif signal_strength > 30:
                    confidence = min(8, 5 + int(percentage_difference / 15))
                else:
                    confidence = min(6, 3 + int(percentage_difference / 20))
            else:
                signal_type = "ЖДАТЬ"
                confidence = 3

            # Дополнительные проверки и корректировки
            
            # Если слишком много противоречивых сигналов
            if len(signal_reasons) > 10 and percentage_difference < 15:
                confidence = max(2, confidence - 2)
                signal_reasons.append("противоречивые сигналы")
            
            # Усиление при экстремальных значениях ключевых индикаторов
            extreme_count = 0
            if rsi < 20 or rsi > 80:
                extreme_count += 1
            if stoch_k < 15 or stoch_k > 85:
                extreme_count += 1
            if williams_r < -85 or williams_r > -15:
                extreme_count += 1
            if mfi < 15 or mfi > 85:
                extreme_count += 1
            
            if extreme_count >= 3:
                confidence = min(10, confidence + 2)
                signal_reasons.append("экстремальные значения")
            
            # Проверка согласованности трендовых индикаторов
            trend_agreement = 0
            if (ichimoku_position == 1 and aroon_oscillator > 50 and 
                current_price > sma_20 and ema_12 > ema_26):
                trend_agreement = 1  # Бычий консенсус
            elif (ichimoku_position == -1 and aroon_oscillator < -50 and 
                  current_price < sma_20 and ema_12 < ema_26):
                trend_agreement = -1  # Медвежий консенсус
                
            if trend_agreement != 0:
                confidence = min(10, confidence + 1)
                if trend_agreement == 1:
                    signal_reasons.append("бычий консенсус")
                else:
                    signal_reasons.append("медвежий консенсус")

            # Определяем экспирацию
            if timeframe in ['1m', '3m']:
                expiration = "2"
            elif timeframe in ['5m', '15m']:
                expiration = "3"
            else:
                expiration = "5"

            # Берем главные причины
            main_reasons = signal_reasons[:2] if signal_reasons else ["смешанные сигналы"]
            reason = ", ".join(main_reasons)

            return f"""🎯 СИГНАЛ: {signal_type}
📊 УВЕРЕННОСТЬ: {confidence}/10
⏰ ЭКСПИРАЦИЯ: {expiration} мин
💡 ПРИЧИНА: {reason}

📈 CALL: {call_score} баллов ({call_percentage:.1f}%)
📉 PUT: {put_score} баллов ({put_percentage:.1f}%)
🔍 АНАЛИЗ: {len(signal_reasons)} сигналов из {total_weight} возможных"""

        except Exception as e:
            return f"""🎯 СИГНАЛ: ЖДАТЬ
📊 УВЕРЕННОСТЬ: 3/10
⏰ ЭКСПИРАЦИЯ: 3 мин
💡 ПРИЧИНА: ошибка анализа"""

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
    """Рендерит расширенные метрики в стиле Telegram"""

    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    bb_position = indicators.get('bb_position', 0.5)
    price_change = indicators.get('price_change', 0)
    
    # Все новые индикаторы
    mfi = indicators.get('mfi', 50)
    cci = indicators.get('cci', 0)
    adx = indicators.get('adx', 25)
    stoch_k = indicators.get('stoch_k', 50)
    ultimate_oscillator = indicators.get('ultimate_oscillator', 50)
    aroon_oscillator = indicators.get('aroon_oscillator', 0)
    tsi = indicators.get('tsi', 0)
    roc = indicators.get('roc', 0)

    # Определяем статусы для всех индикаторов
    rsi_status = "🔴" if rsi > 75 else "🟢" if rsi < 25 else "🟡"
    macd_status = "📈" if macd > 0 else "📉"
    bb_status = "🔴" if bb_position > 0.8 else "🟢" if bb_position < 0.2 else "🟡"
    price_status = "positive" if price_change > 0 else "negative"
    
    # Статусы новых индикаторов
    mfi_status = "🔴" if mfi > 85 else "🟢" if mfi < 15 else "🟡"
    cci_status = "🔴" if cci > 150 else "🟢" if cci < -150 else "🟡"
    adx_status = "💪" if adx > 35 else "😴"
    stoch_status = "🔴" if stoch_k > 85 else "🟢" if stoch_k < 15 else "🟡"
    uo_status = "🔴" if ultimate_oscillator > 75 else "🟢" if ultimate_oscillator < 25 else "🟡"
    aroon_status = "📈" if aroon_oscillator > 70 else "📉" if aroon_oscillator < -70 else "🟡"
    tsi_status = "📈" if tsi > 20 else "📉" if tsi < -20 else "🟡"
    roc_status = "📈" if roc > 2 else "📉" if roc < -2 else "🟡"

    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">RSI (14)</div>
            <div class="metric-value">{rsi:.1f} {rsi_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MFI</div>
            <div class="metric-value">{mfi:.1f} {mfi_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CCI</div>
            <div class="metric-value">{cci:.0f} {cci_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Stochastic</div>
            <div class="metric-value">{stoch_k:.1f} {stoch_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Ultimate Osc</div>
            <div class="metric-value">{ultimate_oscillator:.1f} {uo_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Aroon Osc</div>
            <div class="metric-value">{aroon_oscillator:.0f} {aroon_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">TSI</div>
            <div class="metric-value">{tsi:.1f} {tsi_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">ROC</div>
            <div class="metric-value">{roc:.1f}% {roc_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">ADX (Сила)</div>
            <div class="metric-value">{adx:.1f} {adx_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">BB Позиция</div>
            <div class="metric-value">{bb_position:.0%} {bb_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MACD</div>
            <div class="metric-value">{macd:.4f} {macd_status}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Изменение</div>
            <div class="metric-value metric-change {price_status}">{price_change:+.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_analysis_explanation(indicators: Dict[str, Any], analysis_text: str, pair: str):
    """Рендерит подробное объяснение анализа с ВСЕМИ 15+ индикаторами"""

    # Получаем ВСЕ индикаторы
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
    atr = indicators.get('atr', 0)
    
    # НОВЫЕ РАСШИРЕННЫЕ ИНДИКАТОРЫ
    mfi = indicators.get('mfi', 50)
    cci = indicators.get('cci', 0)
    adx = indicators.get('adx', 25)
    psar = indicators.get('psar', current_price)
    ultimate_oscillator = indicators.get('ultimate_oscillator', 50)
    aroon_up = indicators.get('aroon_up', 50)
    aroon_down = indicators.get('aroon_down', 50)
    aroon_oscillator = indicators.get('aroon_oscillator', 0)
    kc_position = indicators.get('kc_position', 0.5)
    kc_upper = indicators.get('kc_upper', 0)
    kc_middle = indicators.get('kc_middle', 0)
    kc_lower = indicators.get('kc_lower', 0)
    tsi = indicators.get('tsi', 0)
    vwap = indicators.get('vwap', current_price)
    roc = indicators.get('roc', 0)
    ichimoku_position = indicators.get('ichimoku_position', 0)
    ichimoku_a = indicators.get('ichimoku_a', current_price)
    ichimoku_b = indicators.get('ichimoku_b', current_price)

    # Подсчет подтверждающих индикаторов - ПОЛНЫЙ АНАЛИЗ ВСЕХ 15+ ИНДИКАТОРОВ
    call_indicators = []
    put_indicators = []
    neutral_indicators = []

    # 1. RSI анализ
    if rsi < 25:
        call_indicators.append("RSI экстремально перепродан")
    elif rsi < 35:
        call_indicators.append("RSI перепродан")
    elif rsi > 75:
        put_indicators.append("RSI экстремально перекуплен")
    elif rsi > 65:
        put_indicators.append("RSI перекуплен")
    else:
        neutral_indicators.append("RSI нейтральная зона")

    # 2. MFI анализ (НОВЫЙ)
    if mfi < 15:
        call_indicators.append("MFI экстремально перепродан")
    elif mfi < 25:
        call_indicators.append("MFI перепродан")
    elif mfi > 85:
        put_indicators.append("MFI экстремально перекуплен")
    elif mfi > 75:
        put_indicators.append("MFI перекуплен")
    else:
        neutral_indicators.append("MFI нейтральная зона")

    # 3. CCI анализ (НОВЫЙ)
    if cci < -150:
        call_indicators.append("CCI экстремально перепродан")
    elif cci < -100:
        call_indicators.append("CCI перепродан")
    elif cci > 150:
        put_indicators.append("CCI экстремально перекуплен")
    elif cci > 100:
        put_indicators.append("CCI перекуплен")
    else:
        neutral_indicators.append("CCI нейтральная зона")

    # 4. Ultimate Oscillator анализ (НОВЫЙ)
    if ultimate_oscillator < 25:
        call_indicators.append("Ultimate Oscillator перепродан")
    elif ultimate_oscillator > 75:
        put_indicators.append("Ultimate Oscillator перекуплен")
    else:
        neutral_indicators.append("Ultimate Oscillator нейтрален")

    # 5. TSI анализ (НОВЫЙ)
    if tsi < -20:
        call_indicators.append("TSI медвежий экстремум")
    elif tsi > 20:
        put_indicators.append("TSI бычий экстремум")
    else:
        neutral_indicators.append("TSI нейтральная зона")

    # 6. Aroon Oscillator анализ (НОВЫЙ)
    if aroon_oscillator > 70:
        call_indicators.append("Aroon сильный восходящий тренд")
    elif aroon_oscillator < -70:
        put_indicators.append("Aroon сильный нисходящий тренд")
    elif aroon_oscillator > 30:
        call_indicators.append("Aroon слабый восходящий тренд")
    elif aroon_oscillator < -30:
        put_indicators.append("Aroon слабый нисходящий тренд")
    else:
        neutral_indicators.append("Aroon боковой тренд")

    # 7. ROC анализ (НОВЫЙ)
    if roc > 2:
        call_indicators.append("ROC сильный рост")
    elif roc > 0.5:
        call_indicators.append("ROC умеренный рост")
    elif roc < -2:
        put_indicators.append("ROC сильное падение")
    elif roc < -0.5:
        put_indicators.append("ROC умеренное падение")
    else:
        neutral_indicators.append("ROC стабильность")

    # 8. ADX анализ силы тренда (НОВЫЙ)
    if adx > 35:
        if call_indicators and len(call_indicators) > len(put_indicators):
            call_indicators.append("ADX подтверждает сильный восходящий тренд")
        elif put_indicators and len(put_indicators) > len(call_indicators):
            put_indicators.append("ADX подтверждает сильный нисходящий тренд")
        else:
            neutral_indicators.append("ADX показывает сильный тренд")
    elif adx > 25:
        neutral_indicators.append("ADX умеренная сила тренда")
    else:
        neutral_indicators.append("ADX слабый тренд")

    # 9. Parabolic SAR анализ (НОВЫЙ)
    psar_diff = abs(current_price - psar) / current_price
    if current_price > psar and psar_diff > 0.001:
        call_indicators.append("PSAR бычий тренд")
    elif current_price < psar and psar_diff > 0.001:
        put_indicators.append("PSAR медвежий тренд")
    else:
        neutral_indicators.append("PSAR нейтральная зона")

    # 10. Ichimoku Cloud анализ (НОВЫЙ)
    if ichimoku_position == 1:
        call_indicators.append("Ichimoku выше облака")
    elif ichimoku_position == -1:
        put_indicators.append("Ichimoku ниже облака")
    else:
        neutral_indicators.append("Ichimoku в облаке")

    # 11. VWAP анализ (НОВЫЙ)
    vwap_diff = (current_price - vwap) / vwap
    if vwap_diff > 0.01:
        call_indicators.append("VWAP цена значительно выше")
    elif vwap_diff > 0.003:
        call_indicators.append("VWAP цена выше")
    elif vwap_diff < -0.01:
        put_indicators.append("VWAP цена значительно ниже")
    elif vwap_diff < -0.003:
        put_indicators.append("VWAP цена ниже")
    else:
        neutral_indicators.append("VWAP цена близко")

    # 12. Keltner Channel анализ (НОВЫЙ)
    if kc_position < 0.15:
        call_indicators.append("Keltner Channel нижняя граница")
    elif kc_position > 0.85:
        put_indicators.append("Keltner Channel верхняя граница")
    elif kc_position < 0.35:
        call_indicators.append("Keltner Channel нижняя треть")
    elif kc_position > 0.65:
        put_indicators.append("Keltner Channel верхняя треть")
    else:
        neutral_indicators.append("Keltner Channel средняя зона")

    # 13. MACD анализ (улучшенный)
    macd_diff = macd - macd_signal
    if macd > macd_signal and macd_diff > 0.0001:
        if macd > 0:
            call_indicators.append("MACD сильный бычий сигнал")
        else:
            call_indicators.append("MACD слабый бычий сигнал")
    elif macd < macd_signal and abs(macd_diff) > 0.0001:
        if macd < 0:
            put_indicators.append("MACD сильный медвежий сигнал")
        else:
            put_indicators.append("MACD слабый медвежий сигнал")
    else:
        neutral_indicators.append("MACD нейтральный сигнал")

    # 14. Bollinger Bands анализ (улучшенный)
    if bb_position < 0.1:
        call_indicators.append("Bollinger Bands экстремально низ")
    elif bb_position < 0.25:
        call_indicators.append("Bollinger Bands нижняя граница")
    elif bb_position > 0.9:
        put_indicators.append("Bollinger Bands экстремально верх")
    elif bb_position > 0.75:
        put_indicators.append("Bollinger Bands верхняя граница")
    else:
        neutral_indicators.append("Bollinger Bands средняя зона")

    # 15. Stochastic анализ (улучшенный)
    if stoch_k < 15 and stoch_d < 15:
        call_indicators.append("Stochastic экстремально перепродан")
    elif stoch_k < 25:
        call_indicators.append("Stochastic перепродан")
    elif stoch_k > 85 and stoch_d > 85:
        put_indicators.append("Stochastic экстремально перекуплен")
    elif stoch_k > 75:
        put_indicators.append("Stochastic перекуплен")
    else:
        neutral_indicators.append("Stochastic нейтральная зона")

    # 16. Williams %R анализ (улучшенный)
    if williams_r < -85:
        call_indicators.append("Williams %R экстремально перепродан")
    elif williams_r < -75:
        call_indicators.append("Williams %R перепродан")
    elif williams_r > -15:
        put_indicators.append("Williams %R экстремально перекуплен")
    elif williams_r > -25:
        put_indicators.append("Williams %R перекуплен")
    else:
        neutral_indicators.append("Williams %R нейтральная зона")

    # 17. Анализ скользящих средних (расширенный)
    ma_signals = 0
    ma_explanations = []
    
    if current_price > sma_20:
        ma_signals += 1
        ma_explanations.append("цена выше SMA20")
    else:
        ma_explanations.append("цена ниже SMA20")
        
    if current_price > sma_50:
        ma_signals += 1
        ma_explanations.append("цена выше SMA50")
    else:
        ma_explanations.append("цена ниже SMA50")
        
    if ema_12 > ema_26:
        ma_signals += 1
        ma_explanations.append("EMA12 выше EMA26")
    else:
        ma_explanations.append("EMA12 ниже EMA26")
        
    if sma_20 > sma_50:
        ma_signals += 1
        ma_explanations.append("SMA20 выше SMA50")
    else:
        ma_explanations.append("SMA20 ниже SMA50")
    
    if ma_signals >= 3:
        call_indicators.append(f"Скользящие средние восходящий тренд ({ma_signals}/4)")
    elif ma_signals <= 1:
        put_indicators.append(f"Скользящие средние нисходящий тренд ({ma_signals}/4)")
    else:
        neutral_indicators.append(f"Скользящие средние смешанные сигналы ({ma_signals}/4)")

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

    # РАСШИРЕННЫЕ ИНДИКАТОРЫ - ВСЕ 15+ НОВЫХ
    st.subheader("🔍 Расширенный анализ всех 15+ индикаторов")

    # MFI анализ (НОВЫЙ)
    with st.expander("💰 MFI (Money Flow Index) - Денежный поток", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {mfi:.1f}")
            if mfi < 15:
                st.success("🟢 Экстремально перепродан - сильный сигнал покупки")
                mfi_interpretation = f"MFI {mfi:.1f} показывает экстремальную перепроданность. Деньги покидают актив слишком быстро."
            elif mfi < 25:
                st.success("🟢 Перепродан - сигнал покупки")
                mfi_interpretation = f"MFI {mfi:.1f} указывает на перепроданность. Возможен отскок."
            elif mfi > 85:
                st.error("🔴 Экстремально перекуплен - сильный сигнал продажи")
                mfi_interpretation = f"MFI {mfi:.1f} показывает экстремальную перекупленность. Деньги входят слишком агрессивно."
            elif mfi > 75:
                st.error("🔴 Перекуплен - сигнал продажи")
                mfi_interpretation = f"MFI {mfi:.1f} указывает на перекупленность. Возможна коррекция."
            else:
                st.info("🟡 Нейтральная зона")
                mfi_interpretation = f"MFI {mfi:.1f} находится в нейтральной зоне. Денежный поток сбалансирован."
            st.write(f"**Интерпретация:** {mfi_interpretation}")
        with col2:
            st.metric("MFI", f"{mfi:.1f}", help="0-20: Перепродан, 80-100: Перекуплен")
        mfi_normalized = max(0.0, min(1.0, mfi / 100))
        st.progress(mfi_normalized)
        st.caption("💰 MFI учитывает объем торгов и показывает приток/отток денег")

    # CCI анализ (НОВЫЙ)
    with st.expander("📊 CCI (Commodity Channel Index) - Канальный индекс", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {cci:.1f}")
            if cci < -150:
                st.success("🟢 Экстремально перепродан")
                cci_interpretation = f"CCI {cci:.1f} показывает экстремальную перепроданность. Цена далеко от средних значений."
            elif cci < -100:
                st.success("🟢 Перепродан")
                cci_interpretation = f"CCI {cci:.1f} указывает на перепроданность."
            elif cci > 150:
                st.error("🔴 Экстремально перекуплен")
                cci_interpretation = f"CCI {cci:.1f} показывает экстремальную перекупленность."
            elif cci > 100:
                st.error("🔴 Перекуплен")
                cci_interpretation = f"CCI {cci:.1f} указывает на перекупленность."
            else:
                st.info("🟡 Нейтральная зона")
                cci_interpretation = f"CCI {cci:.1f} в нормальном диапазоне."
            st.write(f"**Интерпретация:** {cci_interpretation}")
        with col2:
            st.metric("CCI", f"{cci:.1f}", help="-200 до +200, экстремумы за ±100")
        st.caption("📊 CCI измеряет отклонение цены от статистического среднего")

    # Ultimate Oscillator анализ (НОВЫЙ)
    with st.expander("🎯 Ultimate Oscillator - Составной осциллятор", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {ultimate_oscillator:.1f}")
            if ultimate_oscillator < 25:
                st.success("🟢 Перепродан")
                uo_interpretation = f"UO {ultimate_oscillator:.1f} показывает перепроданность на трех таймфреймах."
            elif ultimate_oscillator > 75:
                st.error("🔴 Перекуплен")
                uo_interpretation = f"UO {ultimate_oscillator:.1f} показывает перекупленность на трех таймфреймах."
            else:
                st.info("🟡 Нейтральная зона")
                uo_interpretation = f"UO {ultimate_oscillator:.1f} показывает сбалансированность."
            st.write(f"**Интерпретация:** {uo_interpretation}")
        with col2:
            st.metric("UO", f"{ultimate_oscillator:.1f}", help="Комбинирует 3 периода: 7, 14, 28")
        uo_normalized = max(0.0, min(1.0, ultimate_oscillator / 100))
        st.progress(uo_normalized)
        st.caption("🎯 Ultimate Oscillator использует 3 периода для снижения ложных сигналов")

    # TSI анализ (НОВЫЙ)
    with st.expander("⚡ TSI (True Strength Index) - Истинная сила", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {tsi:.1f}")
            if tsi < -20:
                st.success("🟢 Медвежий экстремум - возможен разворот вверх")
                tsi_interpretation = f"TSI {tsi:.1f} показывает медвежий экстремум. Сильное давление продавцов."
            elif tsi > 20:
                st.error("🔴 Бычий экстремум - возможен разворот вниз")
                tsi_interpretation = f"TSI {tsi:.1f} показывает бычий экстремум. Сильное давление покупателей."
            else:
                st.info("🟡 Нейтральная зона")
                tsi_interpretation = f"TSI {tsi:.1f} показывает сбалансированные силы."
            st.write(f"**Интерпретация:** {tsi_interpretation}")
        with col2:
            st.metric("TSI", f"{tsi:.1f}", help="Двойное сглаживание импульса")
        st.caption("⚡ TSI показывает истинную силу тренда с двойным сглаживанием")

    # Aroon анализ (НОВЫЙ)
    with st.expander("🌊 Aroon Oscillator - Трендовый анализ", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.metric("Aroon Up", f"{aroon_up:.1f}")
        with col2:
            st.metric("Aroon Down", f"{aroon_down:.1f}")
        with col3:
            st.metric("Oscillator", f"{aroon_oscillator:.1f}")
        
        if aroon_oscillator > 70:
            st.success("🟢 Сильный восходящий тренд")
            aroon_interpretation = f"Aroon показывает сильный восходящий тренд. Up={aroon_up:.1f}, Down={aroon_down:.1f}"
        elif aroon_oscillator < -70:
            st.error("🔴 Сильный нисходящий тренд")
            aroon_interpretation = f"Aroon показывает сильный нисходящий тренд. Up={aroon_up:.1f}, Down={aroon_down:.1f}"
        elif aroon_oscillator > 30:
            st.info("📈 Слабый восходящий тренд")
            aroon_interpretation = f"Aroon показывает слабый восходящий тренд."
        elif aroon_oscillator < -30:
            st.info("📉 Слабый нисходящий тренд")
            aroon_interpretation = f"Aroon показывает слабый нисходящий тренд."
        else:
            st.warning("🟡 Боковой тренд")
            aroon_interpretation = f"Aroon показывает боковое движение."
        
        st.write(f"**Интерпретация:** {aroon_interpretation}")
        st.caption("🌊 Aroon измеряет время с момента последних максимумов и минимумов")

    # ROC анализ (НОВЫЙ)
    with st.expander("🚀 ROC (Rate of Change) - Скорость изменения", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {roc:.2f}%")
            if roc > 2:
                st.success("🟢 Сильный рост")
                roc_interpretation = f"ROC {roc:.2f}% показывает сильное ускорение роста цены."
            elif roc > 0.5:
                st.info("📈 Умеренный рост")
                roc_interpretation = f"ROC {roc:.2f}% показывает умеренный рост."
            elif roc < -2:
                st.error("🔴 Сильное падение")
                roc_interpretation = f"ROC {roc:.2f}% показывает сильное ускорение падения."
            elif roc < -0.5:
                st.warning("📉 Умеренное падение")
                roc_interpretation = f"ROC {roc:.2f}% показывает умеренное падение."
            else:
                st.info("🟡 Стабильность")
                roc_interpretation = f"ROC {roc:.2f}% показывает стабильность цены."
            st.write(f"**Интерпретация:** {roc_interpretation}")
        with col2:
            st.metric("ROC", f"{roc:.2f}%", help="Изменение цены в процентах")
        st.caption("🚀 ROC показывает скорость изменения цены за период")

    # ADX анализ (НОВЫЙ)
    with st.expander("💪 ADX (Average Directional Index) - Сила тренда", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Текущее значение:** {adx:.1f}")
            if adx > 35:
                st.success("💪 Очень сильный тренд")
                adx_interpretation = f"ADX {adx:.1f} показывает очень сильный тренд. Трендовые стратегии предпочтительны."
            elif adx > 25:
                st.info("📈 Умеренный тренд")
                adx_interpretation = f"ADX {adx:.1f} показывает умеренную силу тренда."
            else:
                st.warning("😴 Слабый тренд")
                adx_interpretation = f"ADX {adx:.1f} показывает слабый тренд. Боковое движение."
            st.write(f"**Интерпретация:** {adx_interpretation}")
        with col2:
            st.metric("ADX", f"{adx:.1f}", help="25+ сильный тренд, <25 слабый")
        adx_normalized = max(0.0, min(1.0, adx / 60))
        st.progress(adx_normalized)
        st.caption("💪 ADX не показывает направление, только силу тренда")

    # Parabolic SAR анализ (НОВЫЙ)
    with st.expander("🎯 Parabolic SAR - Стоп и разворот", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Цена", f"{current_price:.5f}")
        with col2:
            st.metric("PSAR", f"{psar:.5f}")
        with col3:
            psar_diff = abs(current_price - psar) / current_price * 100
            st.metric("Расстояние", f"{psar_diff:.2f}%")
        
        if current_price > psar:
            st.success("📈 Бычий тренд - цена выше PSAR")
            psar_interpretation = f"Цена {current_price:.5f} выше PSAR {psar:.5f}. Восходящий тренд."
        elif current_price < psar:
            st.error("📉 Медвежий тренд - цена ниже PSAR")
            psar_interpretation = f"Цена {current_price:.5f} ниже PSAR {psar:.5f}. Нисходящий тренд."
        else:
            st.info("🟡 Точка разворота")
            psar_interpretation = f"Цена близко к PSAR. Возможный разворот тренда."
        
        st.write(f"**Интерпретация:** {psar_interpretation}")
        st.caption("🎯 PSAR следует за ценой и показывает точки разворота тренда")

    # Ichimoku анализ (НОВЫЙ)
    with st.expander("☁️ Ichimoku Cloud - Облако Ишимоку", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Senkou A", f"{ichimoku_a:.5f}")
        with col2:
            st.metric("Senkou B", f"{ichimoku_b:.5f}")
        with col3:
            if ichimoku_position == 1:
                st.success("☁️ Выше")
            elif ichimoku_position == -1:
                st.error("☁️ Ниже")
            else:
                st.warning("☁️ В облаке")
        
        if ichimoku_position == 1:
            st.success("📈 Цена выше облака - сильный бычий сигнал")
            ichimoku_interpretation = f"Цена находится выше облака Ишимоку. Сильный восходящий тренд."
        elif ichimoku_position == -1:
            st.error("📉 Цена ниже облака - сильный медвежий сигнал")
            ichimoku_interpretation = f"Цена находится ниже облака Ишимоку. Сильный нисходящий тренд."
        else:
            st.warning("☁️ Цена в облаке - неопределенность")
            ichimoku_interpretation = f"Цена находится внутри облака. Неопределенный тренд."
        
        st.write(f"**Интерпретация:** {ichimoku_interpretation}")
        st.caption("☁️ Ichimoku - комплексная система анализа тренда")

    # VWAP анализ (НОВЫЙ)
    with st.expander("📊 VWAP (Volume Weighted Average Price) - Объемная цена", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Цена", f"{current_price:.5f}")
        with col2:
            st.metric("VWAP", f"{vwap:.5f}")
        with col3:
            vwap_diff_percent = ((current_price - vwap) / vwap) * 100
            st.metric("Разница", f"{vwap_diff_percent:+.2f}%")
        
        if vwap_diff_percent > 1:
            st.success("📈 Цена значительно выше VWAP")
            vwap_interpretation = f"Цена на {vwap_diff_percent:.2f}% выше VWAP. Сильное давление покупателей."
        elif vwap_diff_percent > 0.3:
            st.info("📈 Цена выше VWAP")
            vwap_interpretation = f"Цена выше VWAP. Умеренное давление покупателей."
        elif vwap_diff_percent < -1:
            st.error("📉 Цена значительно ниже VWAP")
            vwap_interpretation = f"Цена на {abs(vwap_diff_percent):.2f}% ниже VWAP. Сильное давление продавцов."
        elif vwap_diff_percent < -0.3:
            st.warning("📉 Цена ниже VWAP")
            vwap_interpretation = f"Цена ниже VWAP. Умеренное давление продавцов."
        else:
            st.info("🟡 Цена близко к VWAP")
            vwap_interpretation = f"Цена близко к VWAP. Сбалансированный рынок."
        
        st.write(f"**Интерпретация:** {vwap_interpretation}")
        st.caption("📊 VWAP показывает среднюю цену с учетом объемов торгов")

    # Keltner Channel анализ (НОВЫЙ)
    with st.expander("📈 Keltner Channel - Канал Кельтнера", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Верх", f"{kc_upper:.5f}")
        with col2:
            st.metric("Низ", f"{kc_lower:.5f}")
        with col3:
            st.metric("Позиция", f"{kc_position:.0%}")
        
        if kc_position < 0.15:
            st.success("📈 Нижняя граница - сигнал покупки")
            kc_interpretation = f"Цена у нижней границы Keltner Channel ({kc_position:.0%}). Возможен отскок вверх."
        elif kc_position > 0.85:
            st.error("📉 Верхняя граница - сигнал продажи")
            kc_interpretation = f"Цена у верхней границы Keltner Channel ({kc_position:.0%}). Возможна коррекция вниз."
        elif kc_position < 0.35:
            st.info("📈 Нижняя треть")
            kc_interpretation = f"Цена в нижней трети канала ({kc_position:.0%})."
        elif kc_position > 0.65:
            st.warning("📉 Верхняя треть")
            kc_interpretation = f"Цена в верхней трети канала ({kc_position:.0%})."
        else:
            st.info("🟡 Средняя зона")
            kc_interpretation = f"Цена в средней зоне канала ({kc_position:.0%})."
        
        st.write(f"**Интерпретация:** {kc_interpretation}")
        kc_normalized = max(0.0, min(1.0, kc_position))
        st.progress(kc_normalized)
        st.caption("📈 Keltner Channel основан на ATR и показывает волатильность")

    # Стандартные индикаторы с улучшенным отображением
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Stochastic %K",
            f"{stoch_k:.1f}",
            help="0-20: Перепродан, 80-100: Перекуплен"
        )
        if stoch_k < 15:
            st.success("🟢 Экстремально перепродан")
        elif stoch_k < 25:
            st.success("🟢 Перепродан")
        elif stoch_k > 85:
            st.error("🔴 Экстремально перекуплен")
        elif stoch_k > 75:
            st.error("🔴 Перекуплен")
        else:
            st.info("🟡 Нейтрален")

    with col2:
        st.metric(
            "Williams %R",
            f"{williams_r:.1f}",
            help="-100 до -80: Перепродан, -20 до 0: Перекуплен"
        )
        if williams_r < -85:
            st.success("🟢 Экстремально перепродан")
        elif williams_r < -75:
            st.success("🟢 Перепродан")
        elif williams_r > -15:
            st.error("🔴 Экстремально перекуплен")
        elif williams_r > -25:
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

    # Анализ скользящих средних
    with st.expander("📈 Анализ скользящих средних", expanded=False):
        st.write("**Анализ всех скользящих средних:**")
        for explanation in ma_explanations:
            if "выше" in explanation:
                st.success(f"✅ {explanation}")
            else:
                st.error(f"❌ {explanation}")
        
        st.write(f"**Общий сигнал скользящих средних:** {ma_signals}/4 бычьих сигналов")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("SMA20", f"{sma_20:.5f}")
        with col2:
            st.metric("SMA50", f"{sma_50:.5f}")
        with col3:
            st.metric("EMA12", f"{ema_12:.5f}")
        with col4:
            st.metric("EMA26", f"{ema_26:.5f}")
        
        st.caption("📈 Скользящие средние показывают общее направление тренда")

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

    # API ключ в компактном виде
    with st.expander("🔑 Настройки API", expanded=False):
        api_key = st.text_input(
            "OpenAI API Key (для ИИ анализа)",
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

                # Отображаем результат
                current_price = indicators.get('current_price', 0)
                
                # Проверяем валидность индикаторов перед отображением
                if current_price > 0:
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