from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

def _swap_helper(data: list[Node], i: int, j: int) -> list[Node]:
    """
    A helper function that swaps two elements in a list and returns them in a new list.
    """
    return data[:i] + [data[j]] + data[i + 1:j] + [data[i]] + data[j + 1:]

def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    """
    A function that restores heap order by moving a node upward.
    """
    if index <= 0:
        return heap

    parent: int = (index - 1) // 2

    if heap.data[index] < heap.data[parent]:
        new_heap: MinHeap = MinHeap(_swap_helper(heap.data, parent, index))
        return heapify_up(new_heap, parent)

    return heap

def insert(heap: MinHeap, element: Node) -> MinHeap:
    """
    A function that inserts a node into a heap.
    """
    new_data: list[Node] = heap.data + [element]
    return heapify_up(MinHeap(new_data), len(new_data) - 1)

def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    """
    A function that restores heap order by moving a node downward.
    """
    left: int = 2 * index + 1
    right: int = 2 * index + 2

    if left >= len(heap.data):
        return heap

    smallest: int = index

    if right >= len(heap.data) or heap.data[left] < heap.data[right]:
        smallest = left
    else:
        smallest = right

    if heap.data[smallest] < heap.data[index]:
        new_heap: MinHeap = MinHeap(_swap_helper(heap.data, index, smallest))
        return heapify_down(new_heap, smallest)

    return heap

def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    """
    A function that removes and returns the smallest node in the heap.
    """
    if len(heap.data) == 0:
        raise ValueError("Heap is empty.")

    if len(heap.data) == 1:
        return MinHeap([]), heap.data[0]

    smallest: Node = heap.data[0]

    new_data: list[Node] = ([heap.data[-1]] + heap.data[1:-1])
    new_heap: MinHeap = heapify_down(MinHeap(new_data), 0)

    return new_heap, smallest

def count_frequency(s: str)-> dict[str,int]:
    """
    A function that counts how many times each character appears and puts them in a dictionary.
    """
    if s == "":
        return {}

    rest: dict[str, int] = count_frequency(s[1:])
    char: str = s[0]

    if char in rest:
        return {**rest, char: rest[char] + 1}

    return {**rest, char: 1}

def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    """
    A function that creates a MinHeap from a frequency dictionary.
    """
    if frequency == {}:
        return MinHeap([])

    char: str = list(frequency.keys())[0]
    freq: int = frequency[char]

    rest: dict[str, int] = dict(list(frequency.items())[1:])

    smaller_heap: MinHeap = create_priority_queue(rest)

    return insert(smaller_heap, Node(freq, char))

def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    """
    A function that builds a Huffman tree from a priority queue.
    """
    if len(priority_queue.data) == 0:
        return None

    if len(priority_queue.data) == 1:
        return priority_queue.data[0]

    heap1: MinHeap
    first: Node
    heap1, first = extract_min(priority_queue)

    heap2: MinHeap
    second: Node
    heap2, second = extract_min(heap1)

    combined: Node = Node(first.freq + second.freq, first.char, first, second)

    new_heap: MinHeap = insert(heap2, combined)

    return build_tree_from_queue(new_heap)

def generate_codes(node: Node | None, prefix="", code: dict | None =None)-> dict:
    """
    A function that generates Huffman codes from a tree.
    """
    if code is None:
        code: dict = {}

    if node is None:
        return code

    if node.left is None and node.right is None:
        if prefix == "":
            code[node.char] = "0"
        else:
            code[node.char] = prefix
        return code

    generate_codes(node.left, prefix + "0", code)
    generate_codes(node.right, prefix + "1", code)

    return code

def encode(s: str, codes: dict)-> str:
    """
    A function that encodes a string using Huffman codes.
    """
    if s == "":
        return ""

    return codes[s[0]] + encode(s[1:], codes)

def _decode_bits_helper(encoded_string: str, root: Node, current: None) -> str:
    """
    A helper function that traverses a Huffman tree while decoding bits.
    """
    if encoded_string == "":
        return ""

    if encoded_string[0] == "0":
        next_node: Node = current.left
    else:
        next_node = current.right

    if next_node.left is None and next_node.right is None:
        return(next_node.char + _decode_bits_helper(encoded_string[1:], root, root))

    return _decode_bits_helper(encoded_string[1:], root, next_node)

def decode(encoded_string: str, root: Node):
    """
    A function that decodes a Huffman encoded string.
    """
    if root is None:
        return ""

    if root.left is None and root.right is None:
        if encoded_string == "":
            return ""

        return(root.char + decode(encoded_string[1:], root))

    return _decode_bits_helper(encoded_string, root, root)

def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes

