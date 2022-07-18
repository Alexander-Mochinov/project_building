import os

from module import (
    ProjectList,
    EnvironmentLoader,
    SystemsExecuteCommands,
    ExceptionState,
)


class ProjectInitialization:
    """
    Class for project initialization
    """

    def __init__(
        self,
        framework: str,
        path_project: str,
        project_name: str,
        virtualenv: str = None, # Пока что None, потом нужно переделать на выбор типа виртуального окружения 
        *args, **kwargs,
    ) -> None:

        self.path_project = path_project
        self.framework = framework
        self.project_name = project_name
        self.virtualenv = virtualenv

        self.environment_loader = EnvironmentLoader(
            path=self.path_project,
            virtualenv=self.virtualenv,
        )

        self.environment_path = ExceptionState.method_processing(
            function=self.environment_loader.__create_environment,
            text="Create environment",
        )["result_execute"]


    def create_project(self) -> None:
        """
        Method is created a project
        """

        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)

        ExceptionState.method_processing( # Загрузка зависимостей 
            function=self.environment_loader.__loader_requirements,
            params={
                "requirements": ProjectList.PROJECT_LIST[self.framework]["requirements"],
            },
            text="Load requirement",
        )

        ExceptionState.method_processing( # Выполнение команды инициализации проекта 
            function=SystemsExecuteCommands._execute_commands,
            params={
                "path": self.path_project,
                "environment": self.environment_path,
                "commands": [ *ProjectList.PROJECT_LIST[self.framework]["init_command"], self.project_name, ],
                "help_text": "Create project",
            },
            text="Create project",
        )

        for commands in ProjectList.PROJECT_LIST[self.framework]["commands_project"]:
            for command in commands:
                ExceptionState.method_processing( # Выполнение команд указанный в конфигурации 
                    function=SystemsExecuteCommands._execute_commands,
                    params={
                        "commands": command,
                        "path": self.path_project,
                        "environment": self.environment_path,
                        "help_text": "Execute commands",
                    },
                    text="Execute commands",
                )

        ProjectList.PROJECT_LIST[self.framework]["configurations"]( # Выполнение сборки
            main_path=path,
            framework=self.framework,
            project_name=self.project_name,
            path_project=self.path_project,
        ).execute()
