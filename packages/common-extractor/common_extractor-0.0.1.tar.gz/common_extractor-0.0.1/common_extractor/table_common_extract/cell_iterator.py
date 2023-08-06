# coding=utf-8

from .utils import utils
from .utils.mdict import Mdict


class CellIterator(object):
    '''
    Cell 迭代器
    '''

    def __init__(self, cells, **kwargs):
        self._cells = cells
        self.visit_num = 0
        self.row_idx = kwargs.get('row_idx')
        self.col_idx = kwargs.get('col_idx')
        self.start_col_idx = kwargs.get('start_col_idx')
        self.start_row_idx = kwargs.get('start_row_idx')
        self.end_col_idx = kwargs.get('end_col_idx')
        self.end_row_idx = kwargs.get('end_row_idx')
        self.num = kwargs.get('num')

    def visit(self):
        if self.row_idx is not None and self.col_idx is not None:
            return self._cells[self.row_idx][self.col_idx]
        if self.row_idx is not None and self.col_idx is None:
            return self.visit_row_cells(self.row_idx)
        if self.row_idx is None and self.col_idx is not None:
            return self.visit_col_cells(self.col_idx)
        # row idx 和 col idx 都为空则表名未指明特定的行或者列
        return self.visit_area_cells(self.start_col_idx, self.start_row_idx, self.end_col_idx, self.end_row_idx)

    def incr_visit_num(self, n=1):
        self.visit_num += n

    def decr_visit_num(self, n=-1):
        self.visit_num += n

    def visit_row_cells(self, row_idx, start_row_idx=0):
        '''
        :param row_idx:
        :param start_row_idx:
        :return:
        '''
        row_items = self._cells[row_idx]
        visit_num = 0
        visit_col_idx = 0
        for item in row_items:
            visit_col_idx += 1
            if start_row_idx and start_row_idx > visit_col_idx:
                continue
            if self.num is None:
                yield item
            if self.num and self.num > visit_num:
                visit_num += 1
                yield item

    def visit_col_cells(self, col_idx, start_col_idx=0):
        '''
        :param col_idx:
        :param start_col_idx:
        :return:
        '''
        visit_num = 0
        visit_col_idx = 0
        for row_items in self._cells:
            visit_col_idx += 1
            if start_col_idx and start_col_idx > visit_col_idx:
                continue
            if self.num is None:
                yield row_items[col_idx]
            if self.num and self.num > visit_num:
                visit_num += 1
                yield row_items[col_idx]

    def visit_area_cells(self, start_col_idx=None, start_row_idx=None, end_col_idx=None, end_row_idx=None):
        '''
        二维数组遍历一个区域
        :param start_col_idx:
        :param start_row_idx:
        :param end_col_idx:
        :param end_row_idx:
        :param items:  待遍历元素
        :param num:
        :return:
        '''
        start_col_idx = start_col_idx or 0
        start_row_idx = start_row_idx or 0
        end_col_idx = end_col_idx or len(self._cells[0])
        end_row_idx = end_row_idx or len(self._cells)
        visit_num = 0
        for row_items in self._cells[start_row_idx:end_row_idx]:
            for item in row_items[start_col_idx:end_col_idx]:
                if self.num is None:
                    yield item
                if self.num and self.num > visit_num:
                    visit_num += 1
                    yield item

    def locate_cell(self, cell):
        end_col_idx = start_col_idx = cell.col_idx
        end_row_idx = start_row_idx = cell.row_idx
        for tc in self.visit_row_cells(row_idx=cell.row_idx):
            if not utils.is_empty(tc.text):
                break
            if tc.row_idx > end_row_idx:
                end_row_idx = tc.row_idx
        for tc in self.visit_col_cells(col_idx=cell.col_idx):
            if not utils.is_empty(tc.text):
                break
            if tc.col_idx > end_col_idx:
                end_col_idx = tc.col_idx
        return start_col_idx, start_row_idx, end_col_idx, end_row_idx


if __name__ == "__main__":

    bi_nums = [
        [Mdict(text="1", row_idx=1, col_idx=1), Mdict(text="", row_idx=1, col_idx=2),Mdict(text="", row_idx=1, col_idx=3)],
        [Mdict(text="", row_idx=2, col_idx=1), Mdict(text="", row_idx=2, col_idx=2),Mdict(text="1", row_idx=2, col_idx=3)],
        [Mdict(text="1", row_idx=3, col_idx=1), Mdict(text="1", row_idx=3, col_idx=2),Mdict(text="1", row_idx=3, col_idx=3)],
    ]
    ci = CellIterator(bi_nums)
    rst = ci.locate_cell(Mdict(text="1", row_idx=1, col_idx=1))
    print(rst)
    for rst in ci.visit_area_cells():
        print("----")
        print(rst)

