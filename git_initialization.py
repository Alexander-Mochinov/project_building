import os

from module import (
    EnvironmentLoader,
    SystemsExecuteCommands,
    ExceptionState,
)


class GitProjectInitialization:

    def __init__(
        self,
        repository: str,
        path_project: str,
        virtualenv: str = None,
        *args, **kwargs
    ) -> None:

        self.repository = repository
        self.path_project = path_project
        self.virtualenv = virtualenv

        self.environment_loader = EnvironmentLoader(
            path=self.path_project,
            virtualenv=self.virtualenv,
        )

        self.environment_path = ExceptionState.method_processing(
            function=self.environment_loader.__create_environment,
            text="Create environment",
        )["result_execute"]

    def init_repository(self) -> bool:
        return True or False
