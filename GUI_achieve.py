# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Day_Stock_lookup import Day_StockData
from Otherplot import StockPlotter as MonthlyPlotter
from StockPlotter_week import StockPlotter as WeeklyPlotter
from datetime import datetime

class StockGUI:
    def __init__(self, master):
        self.master = master
        master.title("股票指数分析系统")
        master.geometry("800x600")

        # 初始化数据获取类
        self.day_getter = Day_StockData()
        self.monthly_plotter = MonthlyPlotter()
        self.weekly_plotter = WeeklyPlotter()

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = ttk.Label(self.master, text="股票指数分析系统", font=("黑体", 20))
        title_label.pack(pady=10)

        # 国家选择
        country_frame = ttk.Frame(self.master)
        country_frame.pack(pady=5)
        
        ttk.Label(country_frame, text="选择国家:").pack(side=tk.LEFT)
        self.country_var = tk.StringVar()
        self.country_cb = ttk.Combobox(
            country_frame, 
            textvariable=self.country_var,
            values=["中国", "美国"],
            state="readonly"
        )
        self.country_cb.current(0)
        self.country_cb.pack(side=tk.LEFT, padx=5)
        self.country_cb.bind("<<ComboboxSelected>>", self.update_index_types)

        # 指数类型选择
        index_frame = ttk.Frame(self.master)
        index_frame.pack(pady=5)
        
        ttk.Label(index_frame, text="选择指数:").pack(side=tk.LEFT)
        self.index_var = tk.StringVar()
        self.index_cb = ttk.Combobox(
            index_frame,
            textvariable=self.index_var,
            state="readonly"
        )
        self.index_cb.pack(side=tk.LEFT, padx=5)
        self.update_index_types()

        # 日期查询部分
        date_frame = ttk.Frame(self.master)
        date_frame.pack(pady=10)
        
        ttk.Label(date_frame, text="日期查询 (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.date_entry = ttk.Entry(date_frame, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(date_frame, text="查询", command=self.daily_query).pack(side=tk.LEFT)

        # 结果显示区域
        self.result_text = tk.Text(self.master, height=10, width=70)
        self.result_text.pack(pady=10)

        # 图表类型选择
        chart_frame = ttk.Frame(self.master)
        chart_frame.pack(pady=5)
        
        ttk.Label(chart_frame, text="图表类型:").pack(side=tk.LEFT)
        self.chart_var = tk.StringVar()
        self.chart_cb = ttk.Combobox(
            chart_frame,
            textvariable=self.chart_var,
            values=["周线图", "月线图", "面积图"],
            state="readonly"
        )
        self.chart_cb.current(0)
        self.chart_cb.pack(side=tk.LEFT, padx=5)
        
        # 年份输入部分
        year_frame = ttk.Frame(self.master)
        year_frame.pack(pady=5)
        
        ttk.Label(year_frame, text="输入年份 (YYYY):").pack(side=tk.LEFT)
        self.year_entry = ttk.Entry(year_frame, width=10)
        self.year_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(chart_frame, text="绘制图表", command=self.plot_chart).pack(side=tk.LEFT)

    def update_index_types(self, event=None):
        country = self.country_var.get()
        if country == "中国":
            indices = [("上证指数", "000001"), ("深证成指", "399001")]
        else:
            indices = [("道琼斯指数", "DJIA")]
        
        display_values = [f"{name} ({code})" for name, code in indices]
        self.index_cb["values"] = display_values
        self.index_cb.current(0)
        self.indices_mapping = {display: code for display, (name, code) in zip(display_values, indices)}

    def get_selected_index_code(self):
        display = self.index_var.get()
        return self.indices_mapping.get(display, "000001")

    def daily_query(self):
        date_str = self.date_entry.get()
        index_code = self.get_selected_index_code()
        
        try:
            # 验证日期格式
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用YYYY-MM-DD格式")
            return

        # 根据指数类型调用不同方法
        if index_code == "DJIA":
            data = self.day_getter.get_dji_daily_data(date_str)
        elif index_code == "000001":
            data = self.day_getter.get_daily_sse_index(date_str)
        else:
            data = self.day_getter.get_daily_index_data(date_str, index_code)
        
        # 显示结果
        self.result_text.delete(1.0, tk.END)
        if data:
            for key, value in data.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
        else:
            self.result_text.insert(tk.END, "未找到数据")

    def plot_chart(self):
        chart_type = self.chart_var.get()
        index_code = self.get_selected_index_code()
        year_str = self.year_entry.get()

        # 验证年份输入
        if not year_str.isdigit() or len(year_str) != 4:
            messagebox.showerror("错误", "年份格式不正确，请输入四位数字（如2023）")
            return

        year = int(year_str)
        
        try:
            if chart_type == "周线图":
                self.weekly_plotter.plot_weekly_chart(year, index_code)
            elif chart_type == "月线图":
                self.monthly_plotter.plot_monthly_chart(year, index_code)
            elif chart_type == "面积图":
                self.monthly_plotter.plot_area_chart(year, index_code)
        except Exception as e:
            messagebox.showerror("错误", f"绘图失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockGUI(root)
    root.mainloop()