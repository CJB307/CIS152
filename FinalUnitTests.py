"""
Author: Caden Black
Date: 10/30/2024
Program: Data Structures Final Unit Tests
"""

import unittest
from DataStructuresFinal import Tasks, Workers, LinkedList, Queue, selection_sort

# Test Tasks
class TestTask(unittest.TestCase):
    def test_task_initialization(self):
        task = Tasks("Task 1", 5, 1, 3)
        self.assertEqual(task.task_name, "Task 1")
        self.assertEqual(task.skill_level, 5)
        self.assertEqual(task.priority, 1)
        self.assertEqual(task.workers_needed, 3)

    def test_task_comparison(self):
        task1 = Tasks("Task 1", 5, 2, 3)
        task2 = Tasks("Task 2", 4, 1, 2)
        self.assertTrue(task1 > task2)

# Test Workers
class TestWorker(unittest.TestCase):
    def test_worker_initialization(self):
        worker = Workers(1, 10, 30)
        self.assertEqual(worker.worker_id, 1)
        self.assertEqual(worker.skill_level, 10)
        self.assertEqual(worker.time_worked, 30)

# Test LinkedList
class TestLinkedList(unittest.TestCase):
    def test_append_worker(self):
        ll = LinkedList()
        worker1 = Workers(1, 5, 40)
        worker2 = Workers(2, 10, 30)
        ll.append(worker1)
        ll.append(worker2)

        # Verify that workers are in the list
        current = ll.head
        self.assertEqual(current.worker.worker_id, 1)
        current = current.next
        self.assertEqual(current.worker.worker_id, 2)

    def test_display_workers(self):
        ll = LinkedList()
        worker1 = Workers(1, 5, 40)
        worker2 = Workers(2, 10, 30)
        ll.append(worker1)
        ll.append(worker2)

        # Capture the display output
        workers_display = []
        current = ll.head
        while current:
            workers_display.append(current.worker.worker_id)
            current = current.next

        self.assertEqual(workers_display, [1, 2])

# Test Queue
class TestQueue(unittest.TestCase):
    def test_add_task(self):
        queue = Queue()
        task = Tasks("Task 1", 5, 1, 3)
        queue.add_task(task)

        # Verify task is added correctly
        self.assertEqual(len(queue.tasks), 1)

    def test_pop_task(self):
        queue = Queue()
        task1 = Tasks("Task 1", 5, 1, 3)
        task2 = Tasks("Task 2", 6, 2, 2)
        queue.add_task(task1)
        queue.add_task(task2)

        # Pop tasks by priority
        popped_task = queue.pop_task()
        self.assertEqual(popped_task.task_name, "Task 1")
        self.assertEqual(len(queue.tasks), 1)

# Test Selection Sort
class TestSelectionSort(unittest.TestCase):
    def test_selection_sort(self):
        workers = [
            Workers(1, 10, 40),
            Workers(2, 5, 30),
            Workers(3, 10, 20),
            Workers(4, 5, 50)
        ]
        
        # Sort workers
        selection_sort(workers)

        # Check that workers are sorted by skill level and by time worked
        self.assertEqual(workers[0].worker_id, 2)
        self.assertEqual(workers[1].worker_id, 4)
        self.assertEqual(workers[2].worker_id, 3)
        self.assertEqual(workers[3].worker_id, 1)

# Run tests
if __name__ == '__main__':
    unittest.main()
