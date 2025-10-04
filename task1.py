class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int) -> None:
        cur, prev = self.head, None
        if cur and cur.data == key:
            self.head = cur.next
            return
        while cur and cur.data != key:
            prev, cur = cur, cur.next
        if cur is None:
            return
        prev.next = cur.next

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data, "-->", end="")
            current = current.next
        print('None')

    def reverse(self):
        """Реверс однозв'язного списку in-place. O(n) часу, O(1) пам'яті."""
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def merge_sort(self, head):
        """
        Рекурсивне сортування злиттям для однозв'язного списку.
        Приймає голову підсписку, повертає відсортовану голову.
        """
        if head is None or head.next is None:
            return head

        mid = self.get_middle(head)  # mid — голова ПРАВОЇ половини; ліва вже відрізана
        left_sorted = self.merge_sort(head)
        right_sorted = self.merge_sort(mid)
        return self.sorted_merge(left_sorted, right_sorted)

    def get_middle(self, head):
        """
        Знаходить середину та РОЗРІЗАЄ список навпіл.
        Повертає голову правої половини (middle).
        Ліва половина починається у head і закінчується None.
        """
        if head is None or head.next is None:
            return head
        slow = head
        fast = head
        prev = None
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        # розрізати між prev і slow
        if prev:
            prev.next = None
        return slow

    def sorted_merge(self, a, b):
        """Злиття двох відсортованих ланцюгів вузлів, повертає голову результату."""

        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)

        return result

    def merge_sorted_lists(self, list1, list2):
        """
        Об'єднує два ВІДСОРТОВАНІ списки list1 і list2 у self.
        Результат створюється перелінковуванням вузлів (без копій).
        """
        self.head = self.sorted_merge(list1.head, list2.head)
        return self


if __name__ == '__main__':
    first_list = LinkedList()
    first_list.insert_at_beginning(5)
    first_list.insert_at_beginning(10)
    first_list.insert_at_beginning(15)
    first_list.insert_at_end(20)
    first_list.insert_at_end(25)
    print("Зв'язний список:")
    first_list.print_list()

    first_list.reverse()
    print("Зв'язний список після реверсування:")
    first_list.print_list()

    first_list.head = first_list.merge_sort(first_list.head)
    print("Зв'язний список відсортовано:")
    first_list.print_list()

    second_list = LinkedList()
    second_list.insert_at_beginning(59)
    second_list.insert_at_beginning(20)
    second_list.insert_at_beginning(35)
    second_list.head = second_list.merge_sort(second_list.head)

    merged = LinkedList().merge_sorted_lists(first_list, second_list)
    print("Злиття двох відсортованих списків:")
    merged.print_list()
