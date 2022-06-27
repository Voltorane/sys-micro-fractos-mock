import os
from stat import S_IREAD, S_IRGRP, S_IROTH


def generate_task_graph():
    task_graph = []
    # iterate over free storage + computational nodes
    # we need os.chmod(path, S_IREAD) for storage node to make file read-only
    pass


class Application:

    def start(self):
        generate_task_graph(self)
        # execute
        pass
