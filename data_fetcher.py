import akshare as ak
import pandas as pd
from datetime import datetime

def get_index_data(symbol, name):
    """
    获取指数价格数据
    """
    try:
        # 转换代码格式，akshare 的 stock_zh_index_daily 需要 sh/sz 前缀
        if symbol.startswith('000'):
            ak_symbol = f"sh{symbol}"
        elif symbol.startswith('399'):
            ak_symbol = f"sz{symbol}"
        else:
            ak_symbol = symbol
            
        df = ak.stock_zh_index_daily(symbol=ak_symbol)
        return df
    except Exception as e:
        print(f"获取指数 {name}({symbol}) 价格数据失败: {e}")
        return None

def get_valuation_data(symbol, name):
    """
    获取指数估值数据
    """
    try:
        # 去掉前缀，只保留数字
        clean_symbol = ''.join(filter(str.isdigit, symbol))
        # 尝试中证指数接口
        try:
            df = ak.stock_zh_index_value_csindex(symbol=clean_symbol)
            if df is not None and not df.empty:
                return df
        except:
            pass
            
        # 如果失败，尝试乐咕乐股接口 (如果 akshare 支持)
        # 或者直接返回 None
        return None
    except Exception as e:
        print(f"获取指数 {name}({symbol}) 估值数据失败: {e}")
        return None

def fetch_all_indices():
    indices = [
        {"symbol": "000016", "name": "上证50"},
        {"symbol": "000300", "name": "沪深300"},
        {"symbol": "000905", "name": "中证500"},
        {"symbol": "000852", "name": "中证1000"},
        {"symbol": "399006", "name": "创业板指"},
    ]
    
    results = []
    for idx in indices:
        print(f"正在获取 {idx['name']} 数据...")
        price_df = get_index_data(idx['symbol'], idx['name'])
        val_df = get_valuation_data(idx['symbol'], idx['name'])
        
        results.append({
            "info": idx,
            "price_df": price_df,
            "val_df": val_df
        })
    return results
