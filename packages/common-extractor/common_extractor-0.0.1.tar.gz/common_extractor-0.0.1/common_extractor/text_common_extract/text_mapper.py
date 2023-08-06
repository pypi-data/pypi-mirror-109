# coding=utf-8


class TextMapper(object):
    '''
        文本映射类
    '''

    def __init__(self, source, ignore_chars=[' ']):
        self.source = source
        self.target = ""
        self.ignore_chars = ignore_chars
        self.source_mapper = []
        self.target_mapper = []

    def get_target_text(self):
        self.init()
        return self.target

    def init(self):
        '''
        计算Mapperr
        '''
        source_idx = 0
        target_idx = 0
        source_len = len(self.source)
        last_char_ignored = False
        while source_idx < source_len:
            char = self.source[source_idx]
            source_idx += 1
            if char in self.ignore_chars:
                last_char_ignored = True
            else:
                self.target += char
                target_idx += 1
                if last_char_ignored:
                    last_char_ignored = False
                    continue
                self.source_mapper.append(source_idx)
                self.target_mapper.append(target_idx)

    def get_index(self, target_text, target_index):
        '''
        将目标的text 转化成
        :param target_text: 目标文本
        :param target_index: index
        :return: string, int :source text ， source text index
        '''

        return

    def _get_mapper_index(self, index):
        '''
         获取index 所在mapper 里面的位置
        :param index:
        :return: idx ， 在mapper 中的位置
        :todo 查找算法待优化！
        '''
        idx = 0
        mapper_len = len(self.target_mapper)
        while idx < mapper_len:

            if self.target_mapper[idx] <= index \
                    <= self.target_mapper[idx+1]:
                break
            idx += 1
        return idx


if __name__ == "__main__":
    sm = TextMapper("我爱,中,,国,我是,中国人", ignore_chars=[','])
    print (sm.get_target_text())
    print (sm.source_mapper, sm.target_mapper)


