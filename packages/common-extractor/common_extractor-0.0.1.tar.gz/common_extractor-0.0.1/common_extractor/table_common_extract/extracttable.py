# coding=utf-8
from .cell import Cell
from .cell_iterator import CellIterator
from .utils import utils

"""
通用参数说明：
            text: 需要匹配的cell的文本，支持正则，和列表 eg: text="姓.*名" 和 text=['姓.*名', '性.*命'] 均支持
            col_idx：限定列的索引
            row_idx：限定行的索引
            start_col_idx：限定列的起始索引（设定范围时候使用，优先级低于限定行列的索引，终止值大于起始值）
            end_col_idx：限定列的终止索引（设定范围时候使用，优先级低于限定行列的索引，终止值大于起始值）
            start_row_idx：限定行的终止索引（设定范围时候使用，优先级低于限定行列的索引，终止值大于起始值）
            end_row_idx：限定行的终止索引（设定范围时候使用，优先级低于限定行列的索引，终止值大于起始值）

"""


class ExtractTable(object):
    def __init__(self):
        self._table_name = ""
        self._cells = []
        self._row_num = 0
        self._col_num = 0

    @property
    def cells(self):
        return self._cells
    @property
    def row_num(self):
        return self._row_num

    @property
    def col_num(self):
        return self._col_num

    def incr_col_num(self, n=1):
        self._col_num += n

    def incr_row_num(self, n=1):
        self._row_num += n

    def from_object(self, td_array):
        '''
        将常见的二维数组
        :param obj:
        :return:
        '''
        for row in td_array:
            li = []
            for cl in row:
                c = Cell()
                c.from_dict(cl)
                li.append(c)
            self.cells.append(li)

    def from_idps_cells(self, all_cells):
        '''
        将IDPS Table 中的all_cells反序列化成本对象
        :param all_cells:
        :return:
        '''
        row_idx = col_idx = 0
        for row in all_cells:
            col_idx += 1
            li = []
            for cl in row:
                row_idx += 1
                li.append(Cell(text=cl.text, col_idx=col_idx, row_idx=row_idx))
            self.cells.append(li)

    def extract_right_one(self, text, **kwargs):
        '''
        :param text:  需要匹配的cell的文本，支持正则，和列表 eg: text="姓.*名" 和 text=['姓.*名', '性.*命'] 均支持
        :param kwargs: 传入的控制参数，见通用参数说明
        :return: cell
        '''
        kwargs["num"] = 1
        result = self.extract_right_all(text, **kwargs)
        return result[0] if result else None

    def extract_right_all(self, text, **kwargs):
        '''
        :param text:  需要匹配的cell的文本，支持正则，和列表 eg: text="姓.*名" 和 text=['姓.*名', '性.*命'] 均支持
        :param kwargs:传入的控制参数，见通用参数说明
        :return: Cell 列表
        '''
        matched_cells = self.find_all_cell(text, **kwargs)
        ci = CellIterator(self.cells, **kwargs)
        # 通过查找到的cell 查找右侧的值
        matched_results = []
        for mcell in matched_cells:
            for cell in ci.visit_row_cells(row_idx=mcell.row_idx, start_row_idx=mcell.row_idx):
                if utils.is_empty(cell) and kwargs.get('ignore_empty_cell'):
                    ci.decr_visit_num()
                if kwargs.get("num") and len(matched_results) > kwargs.get("num"):
                    break
                matched_results.append(cell)
        return matched_results

    def extract_down_one(self, text, **kwargs):
        '''

        :param text:需要匹配的cell的文本，支持正则，和列表 eg: text="姓.*名" 和 text=['姓.*名', '性.*命'] 均支持
        :param kwargs:传入的控制参数，见通用参数说明
        :return: Cell
        '''
        kwargs["num"] = 1
        result = self.extract_down_all(text, **kwargs)
        return result[0] if result else None

    def extract_down_all(self, text, **kwargs):
        '''
        :param text: 需要匹配的cell的文本，支持正则，和列表 eg: text="姓.*名" 和 text=['姓.*名', '性.*命'] 均支持
        :param kwargs: 传入的控制参数，见通用参数说明
        :return: Cell 列表
        '''
        matched_cells = self.find_all_cell(text, **kwargs)
        ci = CellIterator(self.cells, **kwargs)
        # 通过查找到的cell 查找下面的值
        matched_results = []
        for mcell in matched_cells:
            for cell in ci.visit_col_cells(col_idx=mcell.col_idx, start_col_idx=mcell.col_idx):
                if utils.is_empty(cell) and kwargs.get('ignore_empty_cell'):
                    ci.decr_visit_num()
                if kwargs.get("num") and len(matched_results) > kwargs.get("num"):
                    break
                matched_results.append(cell)
        return matched_results

    def find_one_cell(self, text, **kwargs):
        '''
        定位一个cell
        :return:
        '''
        kwargs["num"] = 1
        result = self.find_all_cell(text, **kwargs)
        return result[0] if result else None

    def find_all_cell(self, text, **kwargs):
        '''
        定位一批cell
        :param text:
        :param kwargs:
        :return:
        '''
        matched_cells = []
        ci = CellIterator(self.cells, **kwargs)
        # 先全局查找匹配的cell
        for cell in ci.visit():
            if utils.is_match(cell.text, text):
                matched_cells.append(cell)
        return matched_cells





