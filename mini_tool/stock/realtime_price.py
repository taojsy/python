from tkinter import *
import sys
import time
import tushare as ts
import numpy as np
import pandas as pd

count = 0
root = Tk()
title = Label(root, text='stock code')
title.pack()
stock_no = Entry(root)
stock_no.pack()
#content = Label(root, text='xxxxx')
#content.pack()


class StockMonitor(Frame):
    msec = 1000

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._running = False
        self.c_date = StringVar()
        self.c_time = StringVar()
        self.stockinfo = StringVar()
        self.flag = True
        self.makewidget()

    def makewidget(self):
        label_date = Label(self, textvariable=self.c_date)
        label_date.pack()
        label_time = Label(self, textvariable=self.c_time)
        label_time.pack()
        label_stock = Label(self, textvariable=self.stockinfo)
        label_stock.pack()

        btn_start = Button(self, text='start', command=self.start)
        btn_start.pack(side=LEFT)
        btn_end = Button(self, text='end', command=self.quit)
        btn_end.pack(side=LEFT)

    def get_stock_info(self, stock_no, num_retries=2):
        df = ts.get_realtime_quotes(stock_no)
        # convert DataFrame to array
        realtime_data_tmp = np.array(df)
        # covert array to list
        realtime_data = realtime_data_tmp.tolist()
        stock_name = realtime_data[0][0]
        pre_close = realtime_data[0][2]
        price = realtime_data[0][3]
        change_percent = str((float(price) - float(pre_close))*100/float(pre_close))[:4] + '%'
        output = stock_name + ' ' + price + ' ' + change_percent
        return output

    def _update(self):
        self._set_content()
        self.timer = self.after(self.msec, self._update)

    def _set_content(self):
        stock_info = self.get_stock_info(stock_no.get())
        current_today = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        current_time = str(time.strftime('%H:%M:%S', time.localtime(time.time())))
        self.stockinfo.set(stock_info)
        self.c_date.set(current_today)
        self.c_time.set(current_time)

    def start(self):
        self._update()
        self.pack(side=TOP)


def main():
    stock = StockMonitor(root)
    stock.pack(side=BOTTOM)
    root.mainloop()
    root.geometry('350x250')


if __name__ == '__main__':
    main()