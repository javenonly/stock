import sys
from PyQt5 import QtWidgets
from window_exec1 import Ui_Form
from PyQt5.QtCore import QDate, Qt
import tushare as ts
import datetime
import tushare as ts
import pandas as pd
import os

class MyWindow_exec1(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(MyWindow_exec1,self).__init__()
        # 文件夹日期 yyyymmdd
        # now = datetime.datetime.now()
        # var_date = now.strftime('%Y-%m-%d')
        # self.historyDate.setDate(var_date)
        self.setupUi(self)
        self.historyDate.setDate(QDate.currentDate())
        # self.sBeginDate = self.historyDate.date().toString(Qt.ISODate)
        # sBeginDate = self.historyDate.date().toString()
        # self.textEdit.setText(sBeginDate)

    #实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def pushButton_click(self):
        # df = ts.get_today_all()
        stock_data_path = 'C:\\stock_data\\'
        df_all_code_file = 'all_code.csv'
        sBeginDate = self.historyDate.date().toString(Qt.ISODate)
        #文件日期文件夹路径
        path = stock_data_path + sBeginDate

        isExists = os.path.exists(path)

        #如果不存在的话
        if not isExists:
            os.makedirs(path)

        self.textEdit.setText('开始获取[' + sBeginDate +']历史数据')

        df = pd.DataFrame(pd.read_csv(stock_data_path + df_all_code_file, index_col=None))

        for code_item in df.code:

            try:
                print('code:' + "%06d" % code_item + '>>>>>>>>begin')
                self.textEdit.append( "%06d" % code_item )
                # 一次性获取全部日k线数据
                df_stock = ts.get_hist_data("%06d" % code_item)

                df_stock.to_csv(stock_data_path + sBeginDate + '/' + "%06d" % code_item + '.csv')

                print('code:' + "%06d" % code_item + '<<<<<<<<end')
                # self.textEdit.setText('code:' + "%06d" % code_item + '<<<<<<<<end')

            except AttributeError:
                print('code:' + "%06d" % code_item + '-------Error------')
                # self.textEdit.setText('code:' + "%06d" % code_item + '-------Error------')
                continue

        # print('OVER')

        # self.textEdit.setText("你点击了按钮")

    #实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def date_init(self):
        # df = ts.get_today_all()
        pass
        # sBeginDate = self.historyDate.date().toString(Qt.ISODate)
        # self.textEdit.setText(self.sBeginDate)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_window_exec1 = MyWindow_exec1()
    my_window_exec1.show()
    sys.exit(app.exec_())