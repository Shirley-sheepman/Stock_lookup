# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 10:30:50 2025

@author: 28211
"""

import mplfinance as mpf
import pandas as pd
from week_Stock_lookup import week_StockData
from datetime import datetime
import warnings
import matplotlib.pyplot as plt  # 新增导入

# 设置全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

warnings.filterwarnings("ignore")  # 忽略mplfinance的样式警告

class StockPlotter:
    def __init__(self):
        self.week_getter = week_StockData()
        self.index_names = {  # 新增指数名称映射
            "DJIA": "Dow Jones Industrial Average",
            "000001": "SSE Composite Index",
            "399001": "SZSE Component Index"
        }
        
    def _fetch_weekly_data(self, year: int, index_code: str) -> pd.DataFrame:
        """获取全年周线数据"""
        data = []
        max_week = 53 if datetime(year, 12, 31).isocalendar()[1] == 53 else 52
        
        for week in range(1, max_week + 1):
            try:
                if index_code == "DJIA":
                    weekly = self.week_getter.get_dji_weekly_data(year, week)
                elif index_code == "000001":
                    weekly = self.week_getter.get_weekly_sse_index(year, week)
                else:
                    weekly = self.week_getter.get_weekly_index_data(year, week, index_code)
                data.extend(weekly)
            except Exception as e:
                print(f"WARN: 第{week}周数据获取失败 ({e})")
        
        return self._format_data(data)

    def _format_data(self, data: list) -> pd.DataFrame:
        """格式化数据为DataFrame"""
        if not data:
            return pd.DataFrame()
        
        # 确保包含成交量字段
        df = pd.DataFrame(data, columns=["日期", "开盘价", "收盘价", "最高价", "最低价", "成交量"])
        df["日期"] = pd.to_datetime(df["日期"])
        return df.set_index("日期").sort_index()

    def plot_weekly_chart(self, year: int, index_code: str):
        weekly_df = self._fetch_weekly_data(year, index_code)
        if not weekly_df.empty:
            title = f"{year} {self.index_names[index_code]} Weekly Chart"
            self._plot(weekly_df, title)

    def _plot(self, df: pd.DataFrame, title: str):
        df = df.rename(columns={
            "开盘价": "Open",
            "收盘价": "Close", 
            "最高价": "High",
            "最低价": "Low",
            "成交量": "Volume"
        })
        df.index = pd.to_datetime(df.index)

        mpf.plot(df,
                 type='candle',
                 title=title,
                 ylabel='Price',
                 ylabel_lower='Volume',
                 volume=True,
                 style='binance',
                 figratio=(18, 8),
                 datetime_format='%Y-%m',
                 show_nontrading=False)



if __name__ == "__main__":
    plotter = StockPlotter()
    
    # 示例：绘制道琼斯指数2023年周线图
    #plotter.plot_weekly_chart(2023, "DJIA")
    
    # 示例：绘制上证指数2023年周线图
    #plotter.plot_weekly_chart(2010, "000001")
    
    # 示例：绘制深证成指2023年周线图
    plotter.plot_weekly_chart(2008, "399001")