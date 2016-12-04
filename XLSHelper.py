# -*- coding: utf-8 -*
import xlwt


class XLSHelper(object):

    def __init__(self):
        self.coding = 'utf8'
        self.datas = []

    def XLSWriter(self, data, sheetname, filename):
        wbk = xlwt.Workbook(self.coding)
        sheet1 = wbk.add_sheet(sheetname)
        # current 记录的是当前行数
        current = 1
        # print(data)
        for user in data:
            for i in range(0, len(data[user])):
                # 输出当前行数据
                sheet1.write(current, i, data[user][i])
            current += 1
        wbk.save(filename)

    def write_in_line(self, data, sheetname):
        wbk = xlwt.Workbook(self.coding)
        sheet1 = wbk.add_sheet(sheetname)
        current = 1
        for user in data:
            for twitter in user:
                for i in range(0, len(twitter)):
                    # 输出当前行数据
                    print(twitter[i])
                    # sheet1.write(current, i, twitter[i])
            current += 1
        return wbk

    @staticmethod
    def write_a_line(data, sheet, line):
        row = 0
        while row < len(data):
            sheet.write(line, row, data[row])
            row += 1

    def save(self, wbk, filename):
        wbk.save(filename)


