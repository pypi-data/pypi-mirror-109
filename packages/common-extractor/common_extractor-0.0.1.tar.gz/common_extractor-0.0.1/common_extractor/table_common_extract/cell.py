# coding=utf-8

from .base import Base


class Cell(object):
    def __init__(self, text=None, col_idx=None, row_idx=None, other=None):
        self._text = text
        self._row_idx = col_idx
        self._col_idx = row_idx
        self._other = other

    def from_dict(self, dict_obj):
        '''
        :param dict_obj:  带对象化dict
        :return:
        '''
        assert "text" in dict_obj and "col_idx" in dict_obj and "row_idx" in dict_obj, "text，col_idx, row_idx为必填项！"
        self.set_text(dict_obj.get("text"))
        self.set_col_idx(dict_obj.get("col_idx"))
        self.set_row_idx(dict_obj.get("row_idx"))

    @property
    def text(self):
        return self._text

    @property
    def row_idx(self):
        return self._row_idx

    @property
    def col_idx(self):
        return self._col_idx

    def set_text(self, text):
        self._text = text

    def set_row_idx(self, row_idx):
        self._row_idx = row_idx

    def set_col_idx(self, col_idx):
        self._col_idx = col_idx

    def from_idps_cell(self, ic, row_idx, col_idx):
        '''
        从IDPS 进行序列化
        :param ic:
        :return:
        '''
        self.set_text(ic.text)
        self.set_row_idx(row_idx)
        self.set_col_idx(col_idx)


if __name__ == "__main__":
    c = Cell()
    c.from_dict({"text": "张三", "row_idx": 1, "col_idx": 2})
    print(c)


