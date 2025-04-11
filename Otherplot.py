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
import matplotlib.pyplot as plt

# 设置全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

warnings.filterwarnings("ignore")

class StockPlotter:
    def __init__(self):
        self.week_getter = week_StockData()
        self.index_names = {
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
        
        df = pd.DataFrame(data, columns=["日期", "开盘价", "收盘价", "最高价", "最低价", "成交量"])
        df["日期"] = pd.to_datetime(df["日期"])
        return df.set_index("日期").sort_index()

    def _resample_monthly(self, weekly_df: pd.DataFrame) -> pd.DataFrame:
        """将周数据重采样为月数据"""
        return weekly_df.resample('M').agg({
            '开盘价': 'first',
            '收盘价': 'last',
            '最高价': 'max',
            '最低价': 'min',
            '成交量': 'sum'
        })

    def plot_monthly_chart(self, year: int, index_code: str):
        """绘制月线图"""
        weekly_df = self._fetch_weekly_data(year, index_code)
        if not weekly_df.empty:
            monthly_df = self._resample_monthly(weekly_df)
            title = f"{year} {self.index_names[index_code]} Monthly Chart"
            self._plot(monthly_df, title, chart_type='candle')

    def plot_area_chart(self, year: int, index_code: str):
        """绘制面积图"""
        weekly_df = self._fetch_weekly_data(year, index_code)
        if not weekly_df.empty:
            title = f"{year} {self.index_names[index_code]} Area Chart"
            self._plot(weekly_df, title, chart_type='area')

    def _plot(self, df: pd.DataFrame, title: str, chart_type: str = 'candle'):
        """通用绘图方法"""
        df = df.rename(columns={
            "开盘价": "Open",
            "收盘价": "Close", 
            "最高价": "High",
            "最低价": "Low",
            "成交量": "Volume"
        })
        df.index = pd.to_datetime(df.index)

        plot_args = {
            'type': chart_type,
            'title': title,
            'ylabel': 'Price',
            'ylabel_lower': 'Volume',
            'volume': True if chart_type == 'candle' else False,
            'style': 'binance',
            'figratio': (18, 8),
            'datetime_format': '%Y-%m' if chart_type == 'candle' else '%Y-%m-%d',
            'show_nontrading': False
        }

        if chart_type == 'area':
            plot_args.update({
                'type': 'line',
                'fill_between': {'y1': df['Close'].values},
                'volume': False
            })

        mpf.plot(df, **plot_args)

if __name__ == "__main__":
    plotter = StockPlotter()
    
    # 绘制上证指数2023年月线图
    plotter.plot_monthly_chart(2023, "DJIA")
    
    # 绘制深证成指2023年面积图
    #plotter.plot_area_chart(2023, "399001")