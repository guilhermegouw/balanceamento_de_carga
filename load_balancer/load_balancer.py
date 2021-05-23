from typing import List, Tuple


class ReportCreator:
    """
    Class that process an input file with data for a case scenario of
    load management and creates a report file with the behavior of the
    loads for that case scenario.
    """

    def __init__(self, input_filename: str, output_filename: str) -> None:
        self._input = input_filename
        self._output = output_filename

    def read_input_file(self) -> Tuple[int, int, List[int]]:
        """
        Read an input file and return the data necessary to create the report.

        Returns:
            Tuple[int, int, List[int]]: duration of tic by task, max users by server, list of new tasks by tic.
        """

        with open(self._input, "r") as file:
            file_lines = file.readlines()
            t_task = int(file_lines[0])
            u_max = int(file_lines[1])
            new_tasks = [int(line) for line in file_lines[2:]]
        return t_task, u_max, new_tasks

    def create_report(self, u_max: int, t_task: int, new_tasks: List[int]):
        """Create a .txt file with a report with the loads behavior

        Args:
            u_max (int): represents the max number of users a server can afford
            t_task (int): quantity of tics consumed by each task.
            new_tasks (List[int]): list containing the number of tasks added by tic.
        """
        load_balancer = LoadBalancer(u_max=u_max, t_task=t_task)
        with open(self._output, "a+") as f:
            total_cost = 0
            for line in new_tasks:
                load_balancer.serve_tasks(line)
                f.write(f"{load_balancer}\n")
                total_cost += len(str(load_balancer).split(","))
                load_balancer.tic()
            while load_balancer.has_active_server():
                f.write(f"{load_balancer}\n")
                total_cost += len(str(load_balancer).split(","))
                load_balancer.tic()
            f.write("0\n")
            f.write(str(total_cost))


class LoadBalancer:
    """
    Manages the loads of tasks by server
    """

    def __init__(self, u_max: int, t_task: int) -> None:
        self.u_max = u_max
        self.t_task = t_task
        self._servers = []

    def __str__(self) -> str:
        """String representation of the loads of tasks by server

        Returns:
            str: represents each server separated by "," each number is the number of tasks by server.
        """
        return ",".join(str(s) for s in self._servers)

    def serve_tasks(self, num_of_tasks: int):
        """Add a task to a server if possible, if not add a new server e add to it that task.

        Args:
            num_of_tasks (int): number of task to add.
        """
        for server in self._servers:
            for i in range(num_of_tasks):
                added_task = server.add_task()
                if added_task:
                    num_of_tasks -= 1
                else:
                    break
        if num_of_tasks > 0:
            self._servers.append(Server(u_max=self.u_max, t_task=self.t_task))
            self.serve_tasks(num_of_tasks)

    def tic(self):
        """
        Apply tic to each active server and update _servers.
        """
        for server in self._servers:
            server.tic()
        self._servers = list(filter(lambda server: server.has_tasks(), self._servers))

    def has_active_server(self) -> bool:
        """Verify if there is an active server.

        Returns:
            bool: True if there is at least an active server, False if there is not.
        """
        return len(self._servers) > 0


class Server:
    def __init__(self, u_max: int, t_task: int) -> None:
        self._u_max = u_max
        self.t_task = t_task
        self._tasks = []

    def has_tasks(self) -> bool:
        return len(self._tasks) > 0

    def add_task(self) -> bool:
        if len(self._tasks) >= self._u_max:
            return False
        else:
            self._tasks.append(Task(self.t_task))
            return True

    def tic(self):
        for task in self._tasks:
            task.tic()
        self._tasks = [t for t in self._tasks if t.is_active()]

    def __str__(self) -> str:
        return str(len(self._tasks))


class Task:
    def __init__(self, t_task: int) -> None:
        self._t_task = t_task

    def tic(self) -> int:
        self._t_task -= 1
        return self._t_task

    def is_active(self) -> bool:
        return self._t_task > 0


if __name__ == "__main__":
    report_creator = ReportCreator("input.txt", "output.txt")
    t_task, u_max, file_lines = report_creator.read_input_file()
    report_creator.create_report(u_max, t_task, file_lines)
