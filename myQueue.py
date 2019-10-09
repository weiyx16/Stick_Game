class myQueue:
    def __init__(self, init=[]):
        self.content = []
        if init:
            self.inqueue(init) 
    def outqueue(self):
        assert self.length() > 0, 'Queue Length is not enough'
        return self.content.pop(0)
    def queuehead(self):
        return self.content[0]
    def inqueue(self, inQueue):
        self._inqueue_single(inQueue)
    def _inqueue_single(self, element):
        try:
            self.content.append(element)
        except:
            print(' Error during insert queue')
    def isEmpty(self):
        if self.content:
            return False
        else:
            return True
    def length(self):
        return len(self.content)
    
    # ref: https://www.programiz.com/python-programming/iterator
    def __iter__(self):
        self._iter_count = 0
        self._len = self.length()
        return self

    def __next__(self):
        if self._iter_count < self._len:
            result = self.content[self._iter_count]
            self._iter_count += 1
            return result
        else:
            raise StopIteration
            
    def show(self):
        print('For now, queue is {}' .format(self.content))