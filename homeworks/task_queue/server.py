from collections import deque
import argparse

class Task:
    pass

class TaskQueue(deque):

    def _gen_task_id(self, task):
        pass

    def add(self, task):
        task_id = self._gen_task_id(task)
        self.append((task_id, task))
        return task_id

    def get(self):
        i = 0
        task_id, task = *self[i]
        while task.in_use:
            i += 1
            task_id, task = *self[i]
        task.in_use = True
        return task_id, task

class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        pass

    def run(self):
        pass

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
