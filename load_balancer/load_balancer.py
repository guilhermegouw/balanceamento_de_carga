class LoadBalancer:
    def __init__(self, u_max: int, t_task: int) -> None:
        self.u_max = u_max
        self.t_task = t_task
        self._servers = []

    def __str__(self) -> str:
        return ",".join(str(s) for s in self._servers)

    def serve_users(self, num_of_tasks: int):
        for server in self._servers:
            for i in range(num_of_tasks):
                added_task = server.add_task()
                if added_task:
                    num_of_tasks -= 1
                else:
                    break
        if num_of_tasks > 0:
            self._servers.append(Server(u_max=self.u_max, t_task=self.t_task))
            self.serve_users(num_of_tasks)

    def tic(self):
        for server in self._servers:
            server.tic()
        self._servers = list(filter(lambda server: server.has_tasks(), self._servers))

    def has_active_server(self):
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
    with open("input.txt", "r") as file:
        file_lines = file.readlines()
        t_task = int(file_lines[0])
        u_max = int(file_lines[1])
        file_lines = [int(line) for line in file_lines[2:]]

    load_balancer = LoadBalancer(u_max=u_max, t_task=t_task)
    with open("output.txt", "a+") as f:
        total_cost = 0
        for line in file_lines:
            load_balancer.serve_users(line)
            f.write(f"{load_balancer}\n")
            total_cost += len(str(load_balancer).split(","))
            load_balancer.tic()
        while load_balancer.has_active_server():
            f.write(f"{load_balancer}\n")
            total_cost += len(str(load_balancer).split(","))
            load_balancer.tic()
        f.write("0\n")
        f.write(str(total_cost))
