import pandas as pd
from data_fetcher import fetch_all_indices
from analyzer import calculate_trend, calculate_percentile
from datetime import datetime

def generate_report():
    data = fetch_all_indices()
    report_date = datetime.now().strftime("%Y-%m-%d")
    
    report_lines = []
    report_lines.append(f"# 渔盆模型投资指导报告 ({report_date})")
    report_lines.append("\n## 核心指数趋势与估值分析")
    report_lines.append("\n| 指数名称 | 代码 | 趋势信号 | 当前价格 | 20日均线 | 明日临界值 | PE(TTM) | 估值分位 |")
    report_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    
    for item in data:
        info = item['info']
        price_df = item['price_df']
        val_df = item['val_df']
        
        if price_df is not None and not price_df.empty:
            signal, ma20, cv = calculate_trend(price_df)
            current_price = price_df['close'].iloc[-1]
        else:
            signal, ma20, cv, current_price = "N/A", 0, 0, 0
            
        if val_df is not None and not val_df.empty:
            current_pe = float(val_df['市盈率1'].iloc[0])
            percentile = calculate_percentile(val_df, current_pe)
        else:
            current_pe, percentile = 0, 0
            
        report_lines.append(f"| {info['name']} | {info['symbol']} | **{signal}** | {current_price:.2f} | {ma20:.2f} | {cv:.2f} | {current_pe:.2f} | {percentile:.2f}% |")
    
    report_lines.append("\n\n**说明：**")
    report_lines.append("1. **趋势信号**：YES 表示收盘价在 20 日均线上方，NO 表示在下方。")
    report_lines.append("2. **明日临界值**：若明日收盘价高于此值，信号为 YES，否则为 NO。")
    report_lines.append("3. **估值分位**：当前 PE 在历史数据中的百分比位置，越低表示越便宜。")
    report_lines.append("4. 本工具仅供参考，不构成投资建议。")
    
    report_content = "\n".join(report_lines)
    
    with open("investment_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print("\n报告已生成: investment_report.md")
    print(report_content)

if __name__ == "__main__":
    generate_report()
