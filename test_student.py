import unittest
from proj3 import *


class TestStudentHuffman(unittest.TestCase):

    def test_count_frequency_empty(self) -> None:
        self.assertEqual(count_frequency(""), {})

    def test_count_frequency_repeated(self) -> None:
        self.assertEqual(count_frequency("aaabbc"),{"a": 3, "b": 2, "c": 1})

    def test_insert_one_node(self) -> None:
        heap: MinHeap = MinHeap([])
        node: Node = Node(3, "a")

        result: MinHeap = insert(heap, node)

        self.assertEqual(result.data, [node])
        self.assertEqual(heap.data, [])

    def test_insert_heap_order(self) -> None:
        heap: MinHeap = MinHeap([Node(3, "c"), Node(5, "e")])

        result: MinHeap = insert(heap, Node(1, "a"))

        self.assertEqual(result.data[0], Node(1, "a"))

    def test_extract_min_one_node(self) -> None:
        heap: MinHeap = MinHeap([Node(2, "b")])

        new_heap: MinHeap
        smallest: Node
        new_heap, smallest = extract_min(heap)

        self.assertEqual(smallest, Node(2, "b"))
        self.assertEqual(new_heap.data, [])

    def test_extract_min_multiple_nodes(self) -> None:
        heap: MinHeap = MinHeap([Node(1, "a"), Node(3, "c"), Node(2, "b")])

        new_heap: MinHeap
        smallest: Node
        new_heap, smallest = extract_min(heap)

        self.assertEqual(smallest, Node(1, "a"))
        self.assertEqual(new_heap.data[0], Node(2, "b"))

    def test_create_priority_queue(self) -> None:
        frequency: dict[str, int] = {"a": 3, "b": 1, "c": 2}

        result: MinHeap = create_priority_queue(frequency)

        self.assertEqual(result.data[0], Node(1, "b"))
        self.assertEqual(len(result.data), 3)

    def test_generate_codes_single_character(self) -> None:
        root: Node = Node(4, "a")

        self.assertEqual(generate_codes(root),{"a": "0"})

    def test_generate_codes_small_tree(self) -> None:
        root: Node = Node(3, "a", Node(1, "a"), Node(2, "b"))

        self.assertEqual(generate_codes(root),{"a": "0", "b": "1"})

    def test_encode_basic(self) -> None:
        codes: dict[str, str] = {"A": "0", "B": "1"}

        self.assertEqual(encode("ABBA", codes),"0110")

    def test_decode_basic(self) -> None:
        root: Node = Node(4, "A", Node(1, "A"), Node(1, "B"))

        self.assertEqual(decode("0110", root),"ABBA")

    def test_huffman_single_character(self) -> None:
        encoded: str
        decoded: str
        codes: dict[str, str]

        encoded, decoded, codes = huffman_encoding("aaaa")

        self.assertEqual(encoded, "0000")
        self.assertEqual(decoded, "aaaa")
        self.assertEqual(codes, {"a": "0"})

    def test_huffman_repeated_letters(self) -> None:
        encoded: str
        decoded: str
        codes: dict[str, str]

        encoded, decoded, codes = huffman_encoding("aaabbc")

        self.assertEqual(decoded, "aaabbc")
        self.assertEqual(encode("aaabbc", codes), encoded)

        self.assertTrue("a" in codes)
        self.assertTrue("b" in codes)
        self.assertTrue("c" in codes)

        self.assertEqual(len(codes), 3)

    def test_huffman_spaces(self) -> None:
        encoded: str
        decoded: str
        codes: dict[str, str]

        encoded, decoded, codes = huffman_encoding("a b a")

        self.assertEqual(decoded, "a b a")
        self.assertTrue(" " in codes)
        self.assertTrue("a" in codes)
        self.assertTrue("b" in codes)

    def test_original_heap_not_modified(self) -> None:
        original_node: Node = Node(2, "b")
        heap: MinHeap = MinHeap([original_node])

        result: MinHeap = insert(heap, Node(1, "a"))

        self.assertEqual(heap.data, [original_node])
        self.assertNotEqual(heap.data, result.data)

if __name__ == "__main__":
    unittest.main()