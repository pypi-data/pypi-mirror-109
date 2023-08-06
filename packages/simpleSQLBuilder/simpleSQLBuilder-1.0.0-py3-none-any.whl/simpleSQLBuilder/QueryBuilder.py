class QueryBuilder:
 
    def __init__(self) -> None:
        self.select_list = []
        self.select_from = None
        self.where_list = []
        self.result = ''

    def from_(self, select_from):
        self.select_from = select_from
        return self

    def where(self, *args):
        self.where_list += list(args)
        return self

    def select(self, *args):
        self.select_list += list(args)
        return self

    def build(self) -> str:
        self.result = ''
        self.result += 'SELECT '

        if not len(self.select_list):
            self.result += '*'
        else:
            self.result += ','.join(self.select_list)    

        if self.select_from is None:
            raise Exception('You have not chosen where to get the data from')
        else:
            self.result += ' FROM ' + self.select_from
        
        if len(self.where_list):
            self.result +=  ' WHERE ' + ' AND '.join(self.where_list)

        return self

