from unittest import TestCase, main

from load_balancer import LoadBalancer, Server, Task


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.task = Task(t_task=4)
        return super().setUp()

    def test_can_instantiate_a_task(self):
        assert self.task

    def test_t_task_attribute_return_right_value(self):
        self.assertEqual(self.task._t_task, 4)

    def test_task_has_attribute_tic(self):
        assert self.task.tic()

    def test_tic_decrement_t_task_by_1(self):
        self.task.tic()
        self.assertEqual(self.task._t_task, 3)

    def test_task_has_attribute_is_active(self):
        assert self.task.is_active()

    def test_task_is_actvive(self):
        """
        As t_task is set to 4 is_active() must return True
        """
        self.assertEqual(self.task.is_active(), True)

    def test_task_is_actvive(self):
        """
        As t_task is set to 4 is_active() after 4 tics must return False
        """
        self.task.tic()
        self.task.tic()
        self.task.tic()
        self.task.tic()
        self.assertEqual(self.task.is_active(), False)


class ServerTests(TestCase):
    def setUp(self) -> None:
        self.server = Server(u_max=2, t_task=4)
        return super().setUp()

    def test_can_instantiate_a_server(self):
        assert self.server

    def test_has_tasks(self):
        self.assertEqual(self.server.has_tasks(), False)

    def test_add_task(self):
        self.assertEqual(self.server.add_task(), True)

    def test_has_task_after_add_task(self):
        self.server.add_task()
        self.assertEqual(self.server.has_tasks(), True)

    def test_add_task_twice(self):
        self.server.add_task()
        self.server.add_task()
        self.assertEqual(self.server.has_tasks(), True)

    def test_add_task_three_times(self):
        """
        As the u_max is set to 2, a third task cannot be added.
        """
        self.server.add_task()
        self.server.add_task()
        self.server.add_task()
        self.assertEqual(self.server.add_task(), False)

    def test_server_string_representation(self):
        self.assertEqual(str(self.server), "0")

    def test_server_string_representation_one_task(self):
        self.server.add_task()
        self.assertEqual(str(self.server), "1")

    def test_server_string_representation_after_add_task_three_times(self):
        """
        As the u_max is set to 2, a third task cannot be added so str(server) must return "2".
        """
        self.server.add_task()
        self.server.add_task()
        self.server.add_task()
        self.assertEqual(str(self.server), "2")

    def test_server_tic_with_one_user_one_tic(self):
        """
        Each task has 4 tics duration so, after one tic the server must keep that task.
        """
        self.server.add_task()
        self.server.tic()
        self.assertEqual(str(self.server), "1")

    def test_server_tic_with_one_user_two_tics(self):
        """
        Each task has 4 tics duration so, after two tics the server must keep that task.
        """
        self.server.add_task()
        self.server.tic()
        self.server.tic()
        self.assertEqual(str(self.server), "1")

    def test_server_tic_with_one_user_four_tics(self):
        """
        Each task has 4 tics duration so, after four tics the server will no longer have that task.
        """
        self.server.add_task()
        self.server.tic()
        self.server.tic()
        self.server.tic()
        self.server.tic()
        self.assertEqual(str(self.server), "0")


class LoadBalancerTests(TestCase):
    def setUp(self) -> None:
        self.load_balancer = LoadBalancer(u_max=2, t_task=4)
        return super().setUp()

    def test_can_instantiate_load_balancer(self):
        assert self.load_balancer

    def test_load_balancer_string_representation(self):
        self.assertEqual(str(self.load_balancer), "")

    def test_serve_user(self):
        self.load_balancer.serve_tasks(1)
        self.assertEqual(str(self.load_balancer), "1")

    def test_has_active_servers_True(self):
        self.load_balancer.serve_tasks(2)
        self.assertEqual(self.load_balancer.has_active_server(), True)

    def test_has_active_servers_False(self):
        self.load_balancer.serve_tasks(2)
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.assertEqual(self.load_balancer.has_active_server(), False)

    def test_testcases_for_input_txt_file_first_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.assertEqual(str(self.load_balancer), "1")

    def test_testcases_for_input_txt_file_second_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.assertEqual(str(self.load_balancer), "2,2")

    def test_testcases_for_input_txt_file_third_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.assertEqual(str(self.load_balancer), "2,2")

    def test_testcases_for_input_txt_file_fourth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.assertEqual(str(self.load_balancer), "2,2,1")

    def test_testcases_for_input_txt_file_fifth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.assertEqual(str(self.load_balancer), "1,2,1")

    def test_testcases_for_input_txt_file_sixth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.assertEqual(str(self.load_balancer), "2")

    def test_testcases_for_input_txt_file_seventh_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.assertEqual(str(self.load_balancer), "2")

    def test_testcases_for_input_txt_file_eighth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.assertEqual(str(self.load_balancer), "1")

    def test_testcases_for_input_txt_file_nineth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.assertEqual(str(self.load_balancer), "1")

    def test_testcases_for_input_txt_file_tenth_tic(self):
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(3)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(0)
        self.load_balancer.tic()
        self.load_balancer.serve_tasks(1)
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.load_balancer.tic()
        self.assertEqual(self.load_balancer.has_active_server(), False)
        self.assertEqual(str(self.load_balancer), "")


if __name__ == "__main__":
    main()
