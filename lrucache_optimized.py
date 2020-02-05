
class Node(object):
    def __init__(self, key=None, value=None):
        self.next = None
        self.previous = None
        self.key = key
        self.value = value

class DoublyLinkedList(object):
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.previous = self.head
        self.head.previous = None
        self.tail.next = None

    def add_to_head(self, node: Node):
        node.next = self.head.next
        node.next.previous = node
        node.previous = self.head
        self.head.next = node

class LRUCache(DoublyLinkedList):
    def __init__(self, maxsize=100):
        super(LRUCache, self).__init__()
        self.maxsize = maxsize
        self.dicts = dict()

    def put(self, key, value):
        if key not in self.dicts:
            # check dictionary size if it exceeds the given size
            if len(self.dicts) >= self.maxsize:
                # get tail key: least recently item and update the dictionary
                if self.tail.previous.key in self.dicts: del self.dicts[self.tail.previous.key]
                self.evict(self.tail.previous) # remove tail

            item = Node(key, value)
            self.add_to_head(item)
            self.dicts[key] = item
        else:
            item = self.dicts.get(key)
            item.value = value
            # update the recent by moving to head
            self.evict(item)
            self.add_to_head(item)

    def get(self, key):
        if key not in self.dicts:
            return None

        # we hold the linked list as the value of dictionary
        item = self.dicts.get(key)
        self.evict(item)
        self.add_to_head(item)

        return item.value

    def evict(self, item: Node):
        item.previous.next = item.next
        item.next.previous = item.previous

    # the current size
    def size(self):
        return len(self.dicts)

# tests
if __name__ == '__main__':
    maxsize = 2
    lru_cache = LRUCache(maxsize)
    print('start with maxsize: %s' % maxsize)
    lru_cache.put('a', '1')
    lru_cache.put('b', 2)
    # evict key a and store c
    lru_cache.put('c', '3')
    assert lru_cache.size() == maxsize
    print('exceeds maxsize')
    assert lru_cache.get('a') == None
    print('evicted key a')

    # evict key b
    lru_cache.put(1, 'a')
    assert lru_cache.get('b') == None
    print('evicted key b')

    # evict key c
    lru_cache.put(2, 'b')
    assert lru_cache.get('c') == None
    print('evicted key c')

    # re-order
    print('update least recently used to most used: key:%s-value:%s' % (1, lru_cache.get(1)))

    # will evit 2
    lru_cache.put(3, 'c')
    print('gonna evicts key 2')
    assert lru_cache.get('2') == None

