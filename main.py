# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:30:34 2025

@author: 28211
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:30:24 2025

@author: 28211
"""
from Day_Stock_lookup import Day_StockData
if __name__ == "__main__":
    stock = Day_StockData()
    print(stock.get_dji_daily_data("2019-10-21"))