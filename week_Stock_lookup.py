# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 23:11:17 2025

@author: 28211
"""

import requests
from datetime import datetime, timedelta
import pandas as pd

class week_StockData:
    def __init__(self):
        self.base_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://finance.eastmoney.com/"
        }

    # # 获取指定周的起始日期和结束日期
    def get_week_range(self, week_num, year):
        """
        获取指定周的起始日期和结束日期
        :param week_num: 周数
        :param year: 年份
        :return: 起始日期和结束日期的字符串
        """
        # 获取该年的第一天
        first_day_of_year = datetime(year, 1, 1)
        
        # 获取第一天是星期几 (0=Monday, 6=Sunday)
        first_day_weekday = first_day_of_year.weekday()
        
        # 计算目标周的起始日期
        # 将日期调整到该年的第一个星期一
        start_date = first_day_of_year + timedelta(days=-first_day_weekday, weeks=week_num-1)
        
        # 计算该周的结束日期
        end_date = start_date + timedelta(days=6)
        
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    
    def get_weekly_sse_index(self, year: int, week: int):
        """
        获取指定年份和周数的上证指数周数据
        :param year: 年份（如2023）
        :param week: 周数（如1~52）
        :return: 包含周数据的列表，格式为 [日期, 开盘价, 收盘价, 最高价, 最低价, 成交量]
        """
        try:
            date_str = f"{year}-W{week:02d}-1"  # 周一作为周起始日（ISO标准）
            start_date = datetime.strptime(date_str, "%Y-W%W-%w").date()
            end_date = start_date + timedelta(days=4)
        except ValueError:
            print("日期转换错误，请检查年份和周数是否合法")
            return []

        params = {
            "secid": "1.000001",  # 上证指数代码（1代表上海市场）
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",  # 字段含义：日期-开盘-收盘-最高-最低-成交量-成交额
            "klt": "101",  # 周期类型：101=周线
            "fqt": "0",  # 复权类型：0=不复权
            "beg": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d")
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return []

        if data.get("data") and "klines" in data["data"]:
            weekly_data = []
            for kline in data["data"]["klines"]:
                items = kline.split(",")
                if len(items) >= 6:
                    weekly_data.append({
                        "日期": items[0],  # 日期（格式：YYYY-MM-DD）
                        "开盘价": float(items[1]),  # 开盘价
                        "收盘价": float(items[2]),  # 收盘价
                        "最高价": float(items[3]),  # 最高价
                        "最低价": float(items[4]),  # 最低价
                        "成交量": int(items[5])  # 成交量（手）
                    })
            return weekly_data
        else:
            print("未找到有效数据，请检查参数或API变动")
            return []

    def get_weekly_index_data(self, year: int, week: int, index_code: str = "399001"):
        """
        获取指定年份和周数的指数周数据（支持上证指数、深证成指等）
        :param year: 年份（如2023）
        :param week: 周数（如1~52）
        :param index_code: 指数代码（默认深证成指399001，上证指数需设为000001）
        :return: 包含周数据的列表，格式为 [日期, 开盘价, 收盘价, 最高价, 最低价, 成交量]
        """
        try:
            if index_code.startswith("000001"):
                secid = f"1.{index_code}"  # 上证指数
            else:
                secid = f"0.{index_code}"  # 深证成指（如399001）、创业板指等

            date_str = f"{year}-W{week:02d}-1"
            start_date = datetime.strptime(date_str, "%Y-W%W-%w").date()
            end_date = start_date + timedelta(days=4)
        except ValueError:
            print("日期或指数代码错误，请检查输入合法性")
            return []

        params = {
            "secid": secid,  # 指数代码（格式：市场前缀.代码）
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",  # 字段含义：日期-开盘-收盘-最高-最低-成交量-成交额
            "klt": "101",  # 周期类型：101=周线
            "fqt": "0",  # 不复权
            "beg": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d")
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return []

        if data.get("data") and "klines" in data["data"]:
            weekly_data = []
            for kline in data["data"]["klines"]:
                items = kline.split(",")
                if len(items) >= 6:
                    weekly_data.append({
                        "日期": items[0],
                        "开盘价": float(items[1]),
                        "收盘价": float(items[2]),
                        "最高价": float(items[3]),
                        "最低价": float(items[4]),
                        "成交量": int(items[5])  # 单位：手
                    })
            return weekly_data
        else:
            print("未找到有效数据，请检查参数或API变动")
            return []

    def get_dji_weekly_data(self, year: int, week: int):
        """
        获取道琼斯指数(^DJI)指定年份和周数的周数据
        :param year: 年份（如2023）
        :param week: 周数（如1~52）
        :return: 包含周数据的列表，格式为 [日期, 开盘价, 收盘价, 最高价, 最低价]
        """
        try:
            start_date, end_date = self.get_week_range(week, year)
            start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("日期转换错误，请检查年份和周数是否合法")
            return []

        params = {
            "secid": "100.DJIA",  # 道琼斯指数代码（100代表美股市场）
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",  # 字段含义：日期-开盘-收盘-最高-最低-成交量-成交额
            "klt": "101",  # 周期类型：101=周线
            "fqt": "0",  # 不复权
            "beg": start_date_dt.strftime("%Y%m%d"),
            "end": end_date_dt.strftime("%Y%m%d")
        }
        

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return []

        if data.get("data") and "klines" in data["data"]:
            weekly_data = []
            for kline in data["data"]["klines"]:
                items = kline.split(",")
                if len(items) >= 6:  # 确保包含成交量字段
                    weekly_data.append({
                        "日期": items[0],          # 日期（格式：YYYY-MM-DD）
                        "开盘价": float(items[1]), # 开盘价
                        "收盘价": float(items[2]), # 收盘价
                        "最高价": float(items[3]), # 最高价
                        "最低价": float(items[4]), # 最低价
                        "成交量": int(items[5])    # 成交量（添加此行）
                    })
            return weekly_data
        else:
            print("未找到有效数据，请检查参数或API变动")
            return []