# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 19:07:09 2025

@author: 28211
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 23:11:17 2025

@author: 28211
"""

import requests
from datetime import datetime
import pandas as pd

class Day_StockData:
    def __init__(self):
        self.base_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://finance.eastmoney.com/"
        }

    def get_daily_sse_index(self, date: str):
        """
        获取指定日期的上证指数日数据
        :param date: 日期字符串（格式：YYYY-MM-DD）
        :return: 包含日数据的字典
        """
        try:
            date_dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("日期格式错误，请使用YYYY-MM-DD格式")
            return {}

        params = {
            "secid": "1.000001",  # 上证指数代码
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",  # 日期-开盘-收盘-最高-最低-成交量-成交额
            "klt": "101",   # 日线
            "fqt": "0",   # 不复权
            "beg": date_dt.strftime("%Y%m%d"),
            "end": date_dt.strftime("%Y%m%d")
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return {}

        if data.get("data") and "klines" in data["data"] and len(data["data"]["klines"]) > 0:
            items = data["data"]["klines"][0].split(",")
            return {
                "日期": items[0],
                "开盘价": float(items[1]),
                "收盘价": float(items[2]),
                "最高价": float(items[3]),
                "最低价": float(items[4]),
                "成交量": int(items[5])
            }
        else:
            print("未找到有效数据")
            return {}

    def get_daily_index_data(self, date: str, index_code: str = "399001"):
        """
        获取指定日期的指数数据（支持上证、深证等）
        :param date: 日期字符串（YYYY-MM-DD）
        :param index_code: 指数代码（默认深证成指）
        :return: 包含日数据的字典
        """
        try:
            date_dt = datetime.strptime(date, "%Y-%m-%d")
            if index_code.startswith("000001"):
                secid = f"1.{index_code}"  # 上证指数
            else:
                secid = f"0.{index_code}"  # 深市指数
        except ValueError:
            print("日期或指数代码错误")
            return {}

        params = {
            "secid": secid,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",
            "klt": "101",
            "fqt": "0",
            "beg": date_dt.strftime("%Y%m%d"),
            "end": date_dt.strftime("%Y%m%d")
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return {}

        if data.get("data") and "klines" in data["data"] and len(data["data"]["klines"]) > 0:
            items = data["data"]["klines"][0].split(",")
            return {
                "日期": items[0],
                "开盘价": float(items[1]),
                "收盘价": float(items[2]),
                "最高价": float(items[3]),
                "最低价": float(items[4]),
                "成交量": int(items[5])
            }
        else:
            print("未找到有效数据")
            return {}

    # 修改Day_Stock_lookup.py中的get_dji_daily_data方法
    def get_dji_daily_data(self, date: str):
        try:
            date_dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("日期格式错误")
            return {}

        params = {
        "secid": "100.DJIA",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",  # 字段顺序：日期,开盘,收盘,最高,最低,成交量,成交额
        "klt": "101",
        "fqt": "0",
        "beg": date_dt.strftime("%Y%m%d"),
        "end": date_dt.strftime("%Y%m%d")
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return {}

        if data.get("data") and "klines" in data["data"] and len(data["data"]["klines"]) > 0:
            items = data["data"]["klines"][0].split(",")
        # 检查返回的日期是否与请求的日期一致
            if items[0].split(" ")[0] != date:
                print(f"返回的日期与请求的日期不一致: 请求日期={date}, 返回日期={items[0].split(' ')[0]}")
                return {}
            return {
            "日期": items[0].split(" ")[0],  # 直接使用返回的日期
            "开盘价": float(items[1]),
            "收盘价": float(items[2]),
            "最高价": float(items[3]),
            "最低价": float(items[4]),
            "成交量": int(items[5])
            }
        else:
            print("未找到有效数据")
            return {}