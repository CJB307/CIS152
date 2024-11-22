"""
Author: Caden Black
Date: 10/15/2024
Program: Data Structures Final
"""

# Imports
import heapq
import tkinter as tk

# Tasks Class
class Tasks:
    def __init__(self, task_name: str, skill_level: int, priority: int, workers_needed: int):
        self.task_name = task_name
        self.skill_level = skill_level
        self.priority = priority
        self.workers_needed = workers_needed

    def __lt__(self, other):
        # This ensures Tasks are ordered by priority for the GUI
        return self.priority < other.priority

# Workers Class
class Workers:
    def __init__(self, worker_id: int, skill_level: int, time_worked: int):
        self.worker_id = worker_id
        self.skill_level = skill_level
        self.time_worked = time_worked

# LinkedList #
class Node:
    def __init__(self, worker):
        self.worker = worker
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, worker):
        new_node = Node(worker)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.worker)
            current = current.next
            
##############

class Queue:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Tasks):
        heapq.heappush(self.tasks, task)

    def pop_task(self):
        return heapq.heappop(self.tasks) if self.tasks else None

    def display_tasks(self):
        for task in sorted(self.tasks):
            print(task)

##############

# Selection Sort based on skill_level & time_worked
def selection_sort(workers):
    n = len(workers)
    for i in range(n):
        # Assume the min is the first element
        min_index = i
        for j in range(i + 1, n):
            # Compare first by skill_level, then by time_worked
            if (workers[j].skill_level < workers[min_index].skill_level or
                (workers[j].skill_level == workers[min_index].skill_level and 
                 workers[j].time_worked < workers[min_index].time_worked)):
                min_index = j
        # Swap the min with the first element
        workers[i], workers[min_index] = workers[min_index], workers[i]

# GUI Application
class TaskManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Management System")
        
        # Set background color to black
        self.master.configure(bg='#000000')

        # Linked List for Workers & Queue for Tasks
        self.workers_list = LinkedList()
        self.queue = Queue()
        assign_array = []

        # Worker Inputs
        self.worker_frame = tk.Frame(master, bg='#000000')
        self.worker_frame.pack(pady=2)

        tk.Label(self.worker_frame, text="Worker ID:", bg='#000000', fg='#FFFFFF').grid(row=0, column=0)
        self.worker_id_entry = tk.Entry(self.worker_frame, bg='#333333', fg='#FFFFFF')
        self.worker_id_entry.grid(row=0, column=1)

        tk.Label(self.worker_frame, text="Skill Level:", bg='#000000', fg='#FFFFFF').grid(row=1, column=0)
        self.skill_level_entry = tk.Entry(self.worker_frame, bg='#333333', fg='#FFFFFF')
        self.skill_level_entry.grid(row=1, column=1)

        tk.Label(self.worker_frame, text="Time Worked:", bg='#000000', fg='#FFFFFF').grid(row=2, column=0)
        self.time_worked_entry = tk.Entry(self.worker_frame, bg='#333333', fg='#FFFFFF')
        self.time_worked_entry.grid(row=2, column=1)

        self.add_worker_button = tk.Button(self.worker_frame, text="Add Worker", command=self.add_worker, bg='#0000FF', fg='#FFFFFF')
        self.add_worker_button.grid(row=3, columnspan=2, pady=2)

        self.workers_display = tk.Text(master, height=5, width=50, bg='#333333', fg='#FFFFFF')
        self.workers_display.pack(pady=10)

        # Task Inputs
        self.task_frame = tk.Frame(master, bg='#000000')
        self.task_frame.pack(pady=10)

        tk.Label(self.task_frame, text="Task Name:", bg='#000000', fg='#FFFFFF').grid(row=0, column=0)
        self.task_name_entry = tk.Entry(self.task_frame, bg='#333333', fg='#FFFFFF')
        self.task_name_entry.grid(row=0, column=1)

        tk.Label(self.task_frame, text="Skill Level Required:", bg='#000000', fg='#FFFFFF').grid(row=1, column=0)
        self.task_skill_level_entry = tk.Entry(self.task_frame, bg='#333333', fg='#FFFFFF')
        self.task_skill_level_entry.grid(row=1, column=1)

        tk.Label(self.task_frame, text="Priority:", bg='#000000', fg='#FFFFFF').grid(row=2, column=0)
        self.task_priority_entry = tk.Entry(self.task_frame, bg='#333333', fg='#FFFFFF')
        self.task_priority_entry.grid(row=2, column=1)

        tk.Label(self.task_frame, text="Workers Needed:", bg='#000000', fg='#FFFFFF').grid(row=3, column=0)
        self.workers_needed_entry = tk.Entry(self.task_frame, bg='#333333', fg='#FFFFFF')
        self.workers_needed_entry.grid(row=3, column=1)

        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task, bg='#0000FF', fg='#FFFFFF')
        self.add_task_button.grid(row=4, columnspan=2, pady=5)

        self.tasks_display = tk.Text(master, height=5, width=50, bg='#333333', fg='#FFFFFF')
        self.tasks_display.pack(pady=10)

        # Task selection for worker assignment
        self.assignment_frame = tk.Frame(master, bg='#000000')
        self.assignment_frame.pack(pady=10)

        tk.Label(self.assignment_frame, text="Select Task:", bg='#000000', fg='#FFFFFF').grid(row=0, column=0)
        self.task_dropdown = tk.StringVar(master)
        self.task_dropdown_menu = tk.OptionMenu(self.assignment_frame, self.task_dropdown, '')
        self.task_dropdown_menu.grid(row=0, column=1)

        self.assign_workers_button = tk.Button(self.assignment_frame, text="Assign Workers", command=self.assign_workers, bg='#0000FF', fg='#FFFFFF')
        self.assign_workers_button.grid(row=1, columnspan=2, pady=5)

        self.assign_display = tk.Text(master, height=5, width=50, bg='#333333', fg='#FFFFFF')
        self.assign_display.pack(pady=10)

        # Initialize Workers and Tasks
        self.update_task_dropdown()

    def add_worker(self):
        try:
            worker_id = int(self.worker_id_entry.get())
            skill_level = int(self.skill_level_entry.get())
            time_worked = int(self.time_worked_entry.get())
            new_worker = Workers(worker_id, skill_level, time_worked)
            self.workers_list.append(new_worker)
            self.worker_id_entry.delete(0, tk.END)
            self.skill_level_entry.delete(0, tk.END)
            self.time_worked_entry.delete(0, tk.END)
            self.display_workers()
        except ValueError:
            self.show_error("Invalid input. Please enter valid integers.")

    def display_workers(self):
        self.workers_display.delete(1.0, tk.END)  # Clear current display
        workers_array = []
        current = self.workers_list.head
        while current:
            workers_array.append(current.worker)
            current = current.next
        selection_sort(workers_array)
        for worker in workers_array:
            self.workers_display.insert(tk.END, f"ID: {worker.worker_id}, Skill: {worker.skill_level}, Time Worked: {worker.time_worked}\n")

    def add_task(self):
        try:
            task_name = self.task_name_entry.get()
            skill_level_required = int(self.task_skill_level_entry.get())
            priority = int(self.task_priority_entry.get())
            workers_needed = int(self.workers_needed_entry.get())
            new_task = Tasks(task_name, skill_level_required, priority, workers_needed)
            self.queue.add_task(new_task)
            self.task_name_entry.delete(0, tk.END)
            self.task_skill_level_entry.delete(0, tk.END)
            self.task_priority_entry.delete(0, tk.END)
            self.workers_needed_entry.delete(0, tk.END)
            self.display_tasks()
            self.update_task_dropdown()
        except ValueError:
            self.show_error("Invalid input. Please enter valid integers.")

    def display_tasks(self):
        self.tasks_display.delete(1.0, tk.END)  # Clear current display
        tasks_array = []
        while True:
            task = self.queue.pop_task()
            if task is None:
                break
            tasks_array.append(task)
        for task in tasks_array:
            self.tasks_display.insert(tk.END, f"Task: {task.task_name}, Skill Level: {task.skill_level}, Priority: {task.priority}, Workers Needed: {task.workers_needed}\n")
            self.queue.add_task(task)  # Add to the queue to display

    def update_task_dropdown(self):
        self.task_dropdown.set('')  # Clear current selection
        tasks = []
        current = self.queue.tasks
        for task in current:
            tasks.append(task.task_name)
        menu = self.task_dropdown_menu['menu']
        menu.delete(0, 'end')  # Clear the menu
        for task in tasks:
            menu.add_command(label=task, command=lambda value=task: self.task_dropdown.set(value))

    def assign_workers(self):
        selected_task_name = self.task_dropdown.get()
        if not selected_task_name:
            self.show_error("Please select a task.")
            return

        # Find the selected task from the queue
        current = self.queue.tasks
        selected_task = None
        while current:
            task = current[0]  # Peek the top of the heap
            if task.task_name == selected_task_name:
                selected_task = task
                break
            current = current[1:]  # Move to the next task in the heap

        if selected_task:
            assigned_workers = []
            current_worker = self.workers_list.head
            while current_worker:
                if (current_worker.worker.skill_level >= selected_task.skill_level and
                    current_worker.worker.time_worked < 40): # make sure worker isn't overworked (40 hour weeks) & has the right skill level
                    assigned_workers.append(current_worker.worker)
                    # Check if we need more workers
                    if len(assigned_workers) >= selected_task.workers_needed:
                        break
                current_worker = current_worker.next

            # Display tree check
            if assigned_workers and len(assigned_workers) >= selected_task.workers_needed:
                self.assign_display.delete(1.0, tk.END)  # Clear current display
                assigned_worker_ids = [str(worker.worker_id) for worker in assigned_workers]
                self.assign_display.insert(tk.END, f"Assigned Workers: {', '.join(assigned_worker_ids)} to Task: {selected_task_name}\n")
            elif assigned_workers and len(assigned_workers) < selected_task.workers_needed:
                self.show_error("Not enough suitable workers available.")
            else:
                self.show_error("No suitable workers available.")
        else:
            self.show_error("Selected task not found.")

    # Error Window
    def show_error(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        tk.Label(error_window, text=message).pack(pady=10)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=5)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementApp(root)
    root.mainloop()


