from collections import deque
import argparse
import socket

class Task:
    __slots__ = ('length', 'data', 'in_use')

    def __init__(self, length, data):
        self.length = length
        self.data = data
        self.in_use = False

class TaskQueue(deque):

    def __init__(self):
        deque.__init__(self)
        self._open_tasks = 0

    def _gen_task_id(self, task):
        if task.length > 128:
            task_id = str(task.data[:128])
        else:
            task_id = str(task.data)
        return task_id

    def add_new_task(self, task):
        self._open_tasks += 1
        task_id = self._gen_task_id(task)
        self.append((task_id, task))
        return task_id

    def get_next_task(self):
        if self._open_tasks == 0:
            return None
        i = 0
        task_id, task = self[i]
        while task.in_use:
            i += 1
            task_id, task = self[i]
        task.in_use = True
        self._open_tasks -= 1
        return task_id, task

    def find_task(self, task_id):
        for task_entry in self:
            if task_entry[0] == task_id:
                return True
        return False

    def finish_task(self, task_id):
        for task_entry in self:
            if task_entry[0] == task_id:
                self.remove(task_entry)
                return True
        return False


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path
        self.timeout = timeout

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((self.ip, self.port))
        connection.listen()
        while True:
            current_connection, address = connection.accept()
            while True:
                command = current_connection.recv(1000000)

                if command == b'':
                    break


def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
