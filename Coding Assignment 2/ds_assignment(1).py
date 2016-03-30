"""
This file provides implementation of Singly Linked List, Chained Hash Dictionary,
Open Addressed Hash Dictionary and Binary Search Tree.
All these functions allow only unique inputs as the nodes or keys.
Non unique nodes or keys are not added to the information sets represented by these classes.
"""
#from decimal import Decimal
from decimal import *
import random


class SinglyLinkedNode(object):
    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):
    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        # Setting head to none to indicate the list is empty.
        self._head = None
        self._length = 0

    def __len__(self):
        """
        Gives the length of the Linked List
        :return: Length
        >>> len(slist)
        1
        """
        return self._length

    def __iter__(self):
        """
        Loops through the content of the Linked list and yields the item values.
        :return: Yields item values of each node
        """
        temp_node = self._head
        while temp_node:
            yield str(temp_node.item)
            temp_node = temp_node.next

    def contains_element(self, item):
        """
        Checks if the given item is present in the linked list
        :param item: Value to be searched in the list
        :return: Boolean value based on the search result
        """
        for temp_node_item in self:
            if temp_node_item == item:
                return True
        return False

    def __contains__(self, item):
        """
        Converts the given element to string and checks if it is present
        in the linked list using contains_element method
        :param item: Value to be searched in the list
        :return: Boolean value from the contains_element method
        >>> slist.prepend(10)
        >>> slist.__contains__(10)
        True
        """
        return self.contains_element(str(item))

    def getnode(self):
        """
        Loops through the list to yields the nodes.
        :return: Node
        """
        temp_node = self._head
        while temp_node:
            yield temp_node
            temp_node = temp_node.next

    def remove(self, item):
        """
        Deletes an item from the linked List if present.
        :param item: Value to be deleted
        :return: None
        >>> slist.remove(10)
        >>> len(slist)
        1
        """
        previous = None
        found = False
        for temp_node in self.getnode():  # searches to see if item is present
            if temp_node.item == item:
                found = True
                break
            else:
                previous = temp_node  # holds previous node in case item not found
        if found:
            if previous is None:
                self._head = temp_node.next
            else:
                previous.next = temp_node.next  # removing the item
            self._length -= 1

    def prepend(self, item):
        """
        Adds new item to the Linked List at the beginning if not already present.
        :param item: Value to be added
        :return: None
        >>> slist.prepend(20)
        >>> len(slist)
        2
        """
        new_node = SinglyLinkedNode(item)
        if not self.__contains__(item):  # check if item already present
            if self._head is not None:
                new_node.next = self._head
            self._head = new_node
            self._length += 1

    def __repr__(self):
        s = "List:" + "->".join([item for item in self])
        return s


class ChainedHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        # Construct a new table
        self.max_bin_capacity = bin_count
        self.max_load_factor = max_load
        self.hashing_func = hashfunc
        self.length = 0
        self.hash_array = [None]*bin_count

    @property
    def load_factor(self):
        """
        Gives the load factor of the hash table.
        :return: load factor
        >>> chained.load_factor
        Decimal('0.3')
        """
        return Decimal(self.length)/Decimal(self.bin_count)

    @property
    def bin_count(self):
        """
        Gives the capacity of the hash table.
        :return: Maximum bin capacity
        >>> chained.bin_count
        10
        """
        return self.max_bin_capacity

    def rebuild(self, bincount):
        """
        Doubles the size of the hash table and rearranges the contents based on new bin size.
        :param bincount: New Bin size
        :return: None
        >>> chained[0] = 10
        >>> chained.rebuild(20)
        >>> print chained.display()
        0:(0, 10)
        1:None
        2:(2, 10)
        3:None
        4:None
        5:None
        6:None
        7:None
        8:None
        9:None
        10:(10, 20)
        11:None
        12:None
        13:None
        14:None
        15:None
        16:None
        17:None
        18:None
        19:None
        """
        self.length = 0
        temp_hash_array = [None]*bincount  # create a temporary array that will be of new bin size.
        for i in range(self.bin_count):
            sll1 = self.hash_array[i]
            if sll1 is not None:
                for list_node in sll1.getnode():
                    new_hash_index = self.hashing_func(list_node.item[0], bincount)
                    sll2 = SinglyLinkedList()
                    if temp_hash_array[new_hash_index] is not None:
                        sll2 = temp_hash_array[new_hash_index]
                    sll2.prepend(list_node.item)
                    temp_hash_array[new_hash_index] = sll2  # moving nodes to the temporary hash array
                    self.length += 1
        self.hash_array = []
        self.hash_array = list(temp_hash_array)  # populating the hash array with new arrangement.
        self.max_bin_capacity = bincount

    def __getitem__(self, key):
        """
        Gives the value associated with a key
        :param key: key to a particular value in the hash array
        :return: Value corresponding to key or message indicating key not present
        >>> chained[0] = 10
        >>> chained[0]
        10
        """
        hash_index = self.hashing_func(key, self.bin_count)
        sll = self.hash_array[hash_index]
        if sll is not None:
            for node in sll.getnode():
                return node.item[1]
        else:
            return "Value not present."

    def __setitem__(self, key, value):
        """
        Inserting the given key, value pair into the hash array
        :param key: key to a particular value
        :param value: the actual value
        :return: None
        >>> chained[10] = 20
        >>> print chained[10]
        20
        """
        if not self.__contains__(key):
            if self.load_factor >= self.max_load_factor:  # if load factor greater than maximum load factor
                self.rebuild(self.bin_count*2)  # Rebuilding the hash array
            hash_index = self.hashing_func(key, self.bin_count)  # evaluating hash index
            sll = self.hash_array[hash_index]
            if sll is None:
                sll = SinglyLinkedList()
            tup = (key, value)
            sll.prepend(tup)
            self.hash_array[hash_index] = sll
            self.length += 1

    def __delitem__(self, key):
        """
        Deletes key,value pair from the hash array
        :param key: key to identify key,value pair to be deleted
        :return: None
        >>> del chained[10]
        >>> print chained[10]
        Value not present.
        """
        hash_index = self.hashing_func(key, self.bin_count)
        sll = self.hash_array[hash_index]
        if sll is not None:
            found = False
            previous = None
            for temp_node in sll.getnode():
                if temp_node.item[0] == key:
                    found = True
                    break
                else:
                    previous = temp_node
            if found:
                if previous is None:
                    sll._head = temp_node.next
                else:
                    previous.next = temp_node.next
            self.length -= 1

    def __contains__(self, key):
        """
        Checks if there is any key, value pair present in the hash arrray
        :param key: key to check
        :return: Boolean value based on search result
        >>> chained[2] = 10
        >>> chained[2]
        10
        """
        hash_index = self.hashing_func(key, self.bin_count)
        sll = self.hash_array[hash_index]
        if sll is None:
            return False
        else:
            for node in sll.getnode():
                if node.item[0] == key:
                    return True
            return False

    def __len__(self):
        """
        Gives the number of key, value pairs present in the hash array
        :return: length of hash array
        >>> len(chained)
        2
        """
        return self.length

    def display(self):
        """
        Returns a string showing the table with multiple lines
        and also items in each bin
        :return: Complete Hash table
        """
        string_list = None
        for i in range(self.bin_count):
            sll = self.hash_array[i]
            if sll is None:
                s = str(i) + ':' + str('None')
            else:
                s = str(i) + ':' + "->".join([item for item in sll])
            if string_list is None:
                string_list = s
            else:
                string_list += "\n"
                string_list += s
        return string_list


class OpenAddressHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        # initialize
        self.max_bin_capacity = bin_count
        self.max_load_factor = max_load
        self.hashing_func = hashfunc
        self.length = 0
        self.hash_array = [None]*bin_count

    @property
    def load_factor(self):
        """
        Gives the load factor of the hash table.
        :return: load factor
        >>> openAdd.load_factor
        Decimal('0.3')
        """
        return Decimal(self.length)/Decimal(self.bin_count)

    @property
    def bin_count(self):
        """
        Gives the maximum capacity of the hash table.
        :return: maximum bin capacity
        >>> openAdd.bin_count
        10
        """
        return self.max_bin_capacity

    def get_hash_key(self, hash_array, key, probe_count, bincount):
        """
        Evaluates the appropriate hash index of the given key
        :param hash_array: hash table which consists of all the key, value pairs
        :param key: key to identify the key, value pair
        :param probe_count: to increment probe count when searching for appropriate hash index
        :param bincount: capacity of the hash table
        :return: Hash index
        """
        hash_index = self.hashing_func(key, probe_count, bincount)
        if hash_array[hash_index] is not None:
            probe_count += 1
            hash_index = self.get_hash_key(hash_array, key, probe_count, bincount)
        return hash_index

    def rebuild(self, bincount):
        """
        Rebuilds the hash table and Rearranges the existing data with new bin size
        :param bincount: new bin size
        :return: None
        >>> openAdd[0] = 10
        >>> openAdd.rebuild(20)
        >>> print openAdd.display()
        0:(0, 10)
        1:None
        2:(2, 10)
        3:None
        4:None
        5:None
        6:None
        7:None
        8:None
        9:None
        10:None
        11:(11, 20)
        12:None
        13:None
        14:None
        15:None
        16:None
        17:None
        18:None
        19:None
        """
        # Rebuild this hash table with a new bin count
        self.length = 0
        temp_hash_array = [None]*bincount
        for i in range(self.bin_count):
            sll1 = self.hash_array[i]
            if sll1 is not None:
                for list_node in sll1.getnode():
                    new_hash_index = self.get_hash_key(temp_hash_array, list_node.item[0], 0, bincount)
                    sll2 = SinglyLinkedList()
                    sll2.prepend(list_node.item)
                    temp_hash_array[new_hash_index] = sll2
                    self.length += 1
        self.hash_array = []
        self.hash_array = list(temp_hash_array)
        self.max_bin_capacity = bincount

    def search(self, key, probe_count):
        """
        Search to see if given key in present in the hash table.
        :param key: key to be searches
        :param probe_count: to keep track of no. of probes when searching for appropriate hash index
        :return: Key,Value node
        """
        hash_index = self.hashing_func(key, probe_count, self.bin_count)
        sll = self.hash_array[hash_index]
        if sll is None:
            return None
        else:
            for node in sll.getnode():
                if node.item[0] == key:
                    return node
            probe_count += 1
            self.search(key, probe_count)

    def __getitem__(self, key):
        """
        Gives the value associated with the given key.
        :param key: key to get the associated value
        :return: Value
        >>> openAdd[0] = 10
        >>> openAdd[0]
        10
        """
        node = self.search(key, 0)
        if node is not None:
            return node.item[1]
        else:
            return "Value not present."

    def __setitem__(self, key, value):
        """
        Insert the given key,value pair into the hash table.
        :param key: key to identify a value
        :param value: the actual value
        :return: None
        >>> openAdd[11] = 20
        >>> print openAdd[11]
        20
        """
        if not self.__contains__(key):
            if self.load_factor >= self.max_load_factor:
                self.rebuild(self.bin_count*2)
            hash_index = self.get_hash_key(self.hash_array, key, 0, self.bin_count)
            sll = SinglyLinkedList()
            tup = (key, value)
            sll.prepend(tup)
            self.hash_array[hash_index] = sll
            self.length += 1

    def __delitem__(self, key):
        """
        Remove the key, value pair represented by the key from the hash table
        :param key: key to identify the pair
        :return: None
        >>> del openAdd[10]
        >>> print openAdd[10]
        Value not present.
        """
        probe_count = 0
        found = False
        hash_index = self.hashing_func(key, probe_count, self.bin_count)
        sll = self.hash_array[hash_index]
        if sll is not None:
            for node in sll.getnode():
                if node.item[0] == key:
                    found = True
                    break
                else:
                    probe_count += 1
                    hash_index = self.hashing_func(key, probe_count, self.bin_count)
        if found:
            if self.hash_array[hash_index] is not None:
                self.hash_array[hash_index] = None
                self.length -= 1

    def __contains__(self, key):
        """
        Checks if a key, value pair is present in the hash table
        :param key: key to identify the key,value pair
        :return: Boolean value based on the search result
        >>> openAdd[2] = 10
        >>> openAdd[2]
        10
        """
        node = self.search(key, 0)
        if node is not None:
            return True
        return False

    def __len__(self):
        """
        Gives the number of items present in the hash table.
        :return: Length
        >>> len(openAdd)
        2
        """
        return self.length

    def display(self):
        """
        Gives a string showing the table with multiple lines and items in each bin
        :return: String representing complete hash table.
        """
        string_list = None
        for i in range(self.bin_count):
            sll = self.hash_array[i]
            if sll is None:
                s = str(i) + ':' + str('None')
            else:
                s = str(i) + ':' + "->".join([item for item in sll])
            if string_list is None:
                string_list = s
            else:
                string_list += "\n"
                string_list += s
        return string_list


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        # initialize
        self.root = None
        self.length = 0

    def height_of_tree(self, root):
        """
        Evaluates the height of the BST recursively
        :param root: root node in the BST
        :return: height
        """
        if root is None:
            return 0
        else:
            left = self.height_of_tree(root.left)
            right = self.height_of_tree(root.right)
            return max(left, right) + 1

    @property
    def height(self):
        """
        Gives the height of the BST
        :return: height
        >>> print tree.height
        3
        """
        temp = self.root
        return self.height_of_tree(temp)

    def inorder_traversal(self, node):
        """
        Recursively evaluates the the BST to yield nodes in "in-order" fashion
        :param node: a node in the BST
        :return: Yields the consequent node
        """
        if node is None:
            raise StopIteration
        for node1 in self.inorder_traversal(node.left):
            yield node1
        yield node
        for node2 in self.inorder_traversal(node.right):
            yield node2

    def preorder_traversal(self, node):
        """
        Recursively evaluates the the BST to yield nodes in "pre-order" fashion
        :param node: a node in BST
        :return: Yields the consequent node
        """
        if node is None:
            raise StopIteration
        yield node
        for node1 in self.preorder_traversal(node.left):
            yield node1
        for node2 in self.preorder_traversal(node.right):
            yield node2

    def postorder_traversal(self, node):
        """
        Recursively evaluates the the BST to yield nodes in "post-order" fashion
        :param node: a node in BST
        :return: Yields the consequent node
        """
        if node is None:
            raise StopIteration
        for node1 in self.postorder_traversal(node.left):
            yield node1
        for node2 in self.postorder_traversal(node.right):
            yield node2
        yield node

    def inorder_keys(self):
        """
        Prints the keys present in the BST using an INORDER traversal
        :return: Keys in INORDER traversal
        >>> tree[1] = 4
        >>> tree[6] = 12
        >>> tree[3] = 6
        >>> tree.inorder_keys()
        [1, 3, 6]
        """
        temp = self.root
        print ([node.data[0] for node in self.inorder_traversal(temp)])

    def postorder_keys(self):
        """
        Prints the keys present in the BST using an POSTORDER traversal
        :return: Keys in POSTORDER traversal
        >>> tree.postorder_keys()
        [3, 6, 1]
        """
        temp = self.root
        print ([node.data[0] for node in self.postorder_traversal(temp)])

    def preorder_keys(self):
        """
        Prints the keys present in the BST using an PREORDER traversal
        :return: Keys in PREORDER traversal
        >>> tree.preorder_keys()
        [1, 6, 3]
        """
        temp = self.root
        print ([node.data[0] for node in self.preorder_traversal(temp)])

    def items(self):
        """
        Gives the items (key and value) using an INORDER Traversal
        :return: Yields the node (key and value)
        """
        temp = self.root
        for node in self.inorder_traversal(temp):
            yield node.data

    def search_node(self, node, key):
        """
        Searches for key in the node and its children
        :param node: where the key is searched
        :param key: key being searched
        :return: node that contains the key
        """
        if node is None:
            return None
        elif key == node.data[0]:
            return node
        elif key < node.data[0]:
            return self.search_node(node.left, key)
        else:
            return self.search_node(node.right, key)

    def __getitem__(self, key):
        """
        Gives the value associated with a key.
        :param key: key to get the associated value
        :return: Value
        >>> tree[1] = 4
        >>> tree[6] = 12
        >>> tree[3] = 6
        >>> tree[3]
        6
        """
        temp = self.root
        if temp is None:
            return "Empty Tree."
        temp = self.search_node(temp, key)
        if temp is not None:
            return temp.data[1]
        else:
            return "Item not available."

    def __setitem__(self, key, value):
        """
        Insert the key,value pair in the BST at its appropriate position
        :param key: identifier of position in BST
        :param value: actual value
        :return: None
        >>> tree[6] = 12
        >>> print tree[6]
        12
        """
        if not self.__contains__(key):
            new_item = BinaryTreeNode((key, value))
            temp1 = self.root
            temp2 = None
            while temp1 is not None:
                temp2 = temp1
                if key < temp1.data[0]:
                    temp1 = temp1.left
                else:
                    temp1 = temp1.right
            new_item.parent = temp2
            if temp2 is None:
                self.root = new_item
            elif new_item.data[0] < temp2.data[0]:
                temp2.left = new_item
            else:
                temp2.right = new_item
            self.length += 1

    @staticmethod
    def tree_minimum(node):
        """
        Gives the minimum key present in the node and its children
        :param node: where the key is searched
        :return: minimum key node
        >>> tree[1]
        4
        """
        while node.left is not None:
            node = node.left
        return node

    def transplant(self, node1, node2):
        """
        Identify the successor of the node being deleted
        :param node1: left sub tree
        :param node2: right sub tree
        :return: None
        """
        temp1 = node1.parent
        if node1.parent is None:
            self.root = node2
        elif node1 == temp1.left:
            temp1.left = node2
        else:
            temp1.right = node2
        if node2 is not None:
            node2.parent = node1.parent

    def __delitem__(self, key):
        """
        Remove the node identified by the given key
        :param key: key to identify node in the BST
        :return: None
        >>> tree[6] = 12
        >>> del tree[6]
        >>> tree[6]
        'Empty Tree.'
        """
        temp1 = self.root
        if temp1 is None:
            return False
        temp1 = self.search_node(temp1, key)
        if temp1 is not None:
            if temp1.left is None:
                self.transplant(temp1, temp1.right)
            elif temp1.right is None:
                self.transplant(temp1, temp1.left)
            else:
                temp2 = self.tree_minimum(temp1.right)
                if temp2.parent != temp1:
                    self.transplant(temp2, temp2.right)
                    temp2.right = temp1.right
                    temp3 = temp2.right
                    temp3.parent = temp2
                self.transplant(temp1, temp2)
                temp2.left = temp1.left
                temp3 = temp2.left
                temp3.parent = temp2
            self.length -= 1

    def __contains__(self, key):
        """
        Searches for the key in the BST
        :param key: node key being searched
        :return: Boolean value based on the search result
        >>> tree[6] = 12
        >>> tree[6]
        12
        """
        temp = self.root
        if temp is None:
            return False
        temp = self.search_node(temp, key)
        if temp is not None:
            return True
        else:
            return False

    def __len__(self):
        """
        Gives the number of nodes in the BST
        :return: length
        >>> len(tree)
        3
        """
        return self.length

    def display(self):
        """
        Print the keys using INORDER on one line and PREORDER on the next
        :return: None
        >>> tree.display()
        [1, 3, 6]
        [1, 6, 3]
        """
        self.inorder_keys()
        self.preorder_keys()


def chaining_hash_func(key, bin_count):
    """
    Hash function that generates hash index for chained hash tables.
    :param key: the value for which hash index should be calculated
    :param bin_count: Hash Table capacity
    :return: Hash Index
    """
    if isinstance(key, int):
        hash_value = key % bin_count
    else:
        hash_value = ord(key) % bin_count
    return hash_value


def open_addressing_hash_func(key, probe, bin_count):
    """
    Hash function that generates hash index for open addressing hash tables
    using Linear probing.
    :param key: the value for which hash index should be calculated
    :param probe: probe to find next available bin.
    :param bin_count: Hash Table capacity
    :return: Hash Index
    """
    auxiliary_hash_value = chaining_hash_func(key, bin_count)
    return (auxiliary_hash_value + probe) % bin_count


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(x, item):
        return bin
    return hashfunc


def testing_singly_linked_list():
    # Singly Linked List testing
    singlyLL = SinglyLinkedList()
    max_list_length = random.randrange(1, 20)
    for i in range(1, max_list_length):
        listitem = random.randrange(1, 50)
        singlyLL.prepend(listitem)
    print (singlyLL)
    # length
    l = 'length = ' + str(len(singlyLL))
    print l
    # contains
    check_item1 = random.randrange(1, 50)
    if check_item1 in singlyLL:
        print 'Is ' + str(check_item1) + ' present: True'
    else:
        print 'Is ' + str(check_item1) + ' present: False'
    check_item2 = 20
    singlyLL.prepend(check_item2)
    print (singlyLL)
    if check_item2 in singlyLL:
        print 'Is ' + str(check_item2) + ' present: True'
    else:
        print 'Is ' + str(check_item2) + ' present: False'
    # delete
    singlyLL.remove(check_item2)
    print 'After Delete: '
    print (singlyLL)
    print ' '


def testing_chained_hash_dictionary():
    chd = ChainedHashDict(10, 0.8, chaining_hash_func)
    for i in range(0, 9):
        chd[i] = random.randrange(1, 500)
    print chd.display()
    print chd.length
    print chd.bin_count
    print chd.load_factor
    check_chd1 = random.randrange(1, 500)
    if check_chd1 in chd:
        print 'Is ' + str(check_chd1) + ' present: True'
    else:
        print 'Is ' + str(check_chd1) + ' present: False'
    check_chd2 = 2
    chd[check_chd2] = 200
    if check_chd2 in chd:
        print 'Is ' + str(check_chd2) + ' present: True'
    else:
        print 'Is ' + str(check_chd2) + ' present: False'
    del chd[2]
    print chd.display()


def testing_open_addressing_hash_dictionary():
    oahd = OpenAddressHashDict(10, 0.9, open_addressing_hash_func)
    for i in range(0, 9):
        oahd[i] = random.randrange(1, 500)
    print oahd.display()
    print oahd.length
    print oahd.bin_count
    print oahd.load_factor
    check_oahd1 = random.randrange(1, 500)
    if check_oahd1 in oahd:
        print 'Is ' + str(check_oahd1) + ' present: True'
    else:
        print 'Is ' + str(check_oahd1) + ' present: False'
    oahd[2] = 200
    if check_oahd1 in oahd:
        print 'Is ' + str(check_oahd1) + ' present: True'
    else:
        print 'Is ' + str(check_oahd1) + ' present: False'
    del oahd[2]
    print oahd.display()


def testing_binary_search_tree():
    # Binary Search Tree testing
    bst = BinarySearchTreeDict()
    for i in range(1, 20):
        bst[i] = random.randrange(1, 500)
    bst[1] = 45
    print (bst[1])
    print (bst.height)
    print (len(bst))
    print " "
    bst.inorder_keys()
    bst.preorder_keys()
    bst.postorder_keys()
    print " "
    bst.display()
    print " "
    for node in bst.items():
        print node
    print " "
    del bst[1]
    print (bst[1])


def main():
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key

    testing_singly_linked_list()
    testing_chained_hash_dictionary()
    testing_open_addressing_hash_dictionary()
    testing_binary_search_tree()
    import doctest
    doctest.testmod(verbose=1, extraglobs={'tree': BinarySearchTreeDict(),
                                           'chained': ChainedHashDict(10, 0.8, chaining_hash_func),
                                           'openAdd': OpenAddressHashDict(10, 0.9, open_addressing_hash_func),
                                           'slist': SinglyLinkedList()})

if __name__ == '__main__':
    main()
