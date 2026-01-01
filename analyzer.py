import pandas as pd
import numpy as np

def calculate_trend(df):
    """
    计算渔盆模型趋势信号和临界值
    df: 包含 'close' 列的 DataFrame
    """
    if len(df) < 20:
        return None, None, None
    
    # 计算 20 日均线
    df['ma20'] = df['close'].rolling(window=20).mean()
    
    # 当前收盘价
    current_close = df['close'].iloc[-1]
    current_ma20 = df['ma20'].iloc[-1]
    
    # 信号: Yes (收盘 > MA20), No (收盘 < MA20)
    signal = "YES" if current_close >= current_ma20 else "NO"
    
    # 计算明天的临界值
    # 明天的 MA20 = (Sum(过去19天) + 明天收盘价) / 20
    # 临界点是 明天收盘价 = 明天 MA20
    # 即: 明天收盘价 = (Sum(过去19天) + 明天收盘价) / 20
    # 20 * 明天收盘价 = Sum(过去19天) + 明天收盘价
    # 19 * 明天收盘价 = Sum(过去19天)
    # 明天收盘价 = Sum(过去19天) / 19
    
    last_19_days_sum = df['close'].iloc[-19:].sum()
    critical_value = last_19_days_sum / 19
    
    return signal, current_ma20, critical_value

def calculate_percentile(val_df, current_pe):
    """
    计算当前 PE 在历史数据中的分位值
    """
    if val_df is None or val_df.empty:
        return None
    
    # 提取历史 PE 数据 (市盈率1)
    history_pe = val_df['市盈率1'].dropna().astype(float)
    
    if len(history_pe) == 0:
        return None
    
    # 计算分位值
    percentile = (history_pe < current_pe).mean() * 100
    return percentile
