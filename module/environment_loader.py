import os

from .exception_state import ExceptionState
from .systems_execute_commands import SystemsExecuteCommands


class EnvironmentLoader:
    """
    Works with virtual environment 
    """

    def __init__(
        self, 
        path: str,
        virtualenv: str,
        *args, **kwargs
    ) -> None:

        self.path = path
        self.virtualenv = virtualenv

    def __create_environment(self) -> dict:
        """
        Метод для виртуального окружения

        Method for virtual environment 
            and return abs path to env
        """

        if not os.path.isdir(self.path / "env"):
            ExceptionState.method_processing(
                function=SystemsExecuteCommands._execute_commands,
                params={
                    "path": self.path,
                    "commands": [ "virtualenv", "env", ],
                    "help_text": "Create env",
                },
                text="Create env",
            )

        return {
            "PATH": str(self.path / "env/bin/"),
        }

    def __loader_requirements(self, requirements: str) -> bool:
        """
        Метод для загрузки зависимости

        Method for load requirements and return list freeze
        """

        execute = ExceptionState.method_processing(
            function=SystemsExecuteCommands._execute_commands,
            params={
                "path": self.path,
                "commands": [ "pip", "install", *requirements, ],
                "help_text": "Install requirements",
                "environment": self.environment_path,
            },
            text="Install requirements",
        )

        return execute["is_execute"]
