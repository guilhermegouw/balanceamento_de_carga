from load_balancer import ReportCreator


def main(input_filename: str, output_filename: str):
    """Read an input file with a case scenario and creates an output file with the report for that case scenario.

    Args:
        input_filename (str): the name of the input file.
        output_filename (str): the name of the output file.
    """
    report_creator = ReportCreator(input_filename, output_filename)
    t_task, u_max, file_lines = report_creator.read_input_file()
    report_creator.create_report(u_max, t_task, file_lines)


if __name__ == "__main__":
    main("files/input.txt", "files/output.txt")
