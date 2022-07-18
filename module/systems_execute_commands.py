import os, subprocess


class SystemsExecuteCommands:

    @staticmethod
    def _execute_commands(
        commands: list,
        path: str,
        help_text: str,
        environment: dict = None,
    ) -> dict:
        """
        Метод реализует выполнение команды

        Method implements command execution
        """

        print('\n\n\n' + help_text)
        print("Use command:  \n\t" + str(" ".join(commands)))
        args_list = []

        with open(os.path.join(path, "execute_logs.txt"), "w+") as file:
            subprocess.call(
                commands,
                cwd=path,
                universal_newlines=True,
                env=environment,
                stdout=file,
            )

        return args_list
