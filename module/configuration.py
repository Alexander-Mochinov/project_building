import os
from ast import parse, walk, Name
from importlib.machinery import SourceFileLoader

from modules.exception_state import ExceptionState


class FileIOController:
    """
    Контроллер для работы с файлами

    File Controller
    """

    @staticmethod
    def add_to_the_end_in_file(
        file_to_append_structure: str,
        path_to_structure: str,
    ) -> None:
        """
        Добавление структуры в конец файла

        Adding structure to the end of a file
        """

        # Чтение структуры
        complete_structure = FileIOController.read_data_from_file(
            path_to_file=path_to_structure,
        )

        # Чтение файла настроек
        structure_file = FileIOController.read_data_from_file(
            path_to_file=file_to_append_structure,
        )

        # Перезапись файла
        with open (file_to_append_structure, 'w') as source:
            source.write(
                structure_file + '\n' + complete_structure + '\n'
            )

        return None

    @staticmethod
    def add_beginning_in_file(
        file_to_append_structure: str,
        path_to_structure: str,
    ) -> None:
        """
        Добавление структуры в начало файла

        Adding structure to the beginning of a file
        """

        # Чтение структуры
        complete_structure = FileIOController.read_data_from_file(
            path_to_file=path_to_structure,
        )

        # Чтение файла настроек
        structure_file = FileIOController.read_data_from_file(
            path_to_file=file_to_append_structure,
        )

        # Перезапись файла
        with open (file_to_append_structure, 'w') as source:
            source.write(
                complete_structure + '\n' + structure_file + '\n',
            )

        return None

    @staticmethod
    def read_data_from_file(path_to_file: str) -> str:
        """
        Чтение из файла

        Reading from a file
        """
        with open(path_to_file, "r") as file:
            data = file.read()

        return data
        
    @staticmethod
    def write_in_file(file: str, values: str) -> None:
        """
        Запись данных в файл

        Writing data to a file
        """

        with open (file, 'a') as source:
            source.write(values + "\n")

        return None

    @staticmethod
    def replace_data_from_file(
        file: str, 
        string_be_replaced: str, 
        values: str
    ) -> None:
        """
        Замена данных в файле

        Replacing data in a file
        """

        old_data = FileIOController.read_data_from_file(
            path_to_file=file,
        )

        new_data = old_data.replace(string_be_replaced, values)

        with open (file, 'w') as source:
            source.write(new_data)

        return None


class ConfigurationController:
    """
    Класс для генерации вспомогательных настроек проекта

    Class for generating auxiliary project settings
    """

    def __init__(
        self,
        framework: str,
        main_path: str,
        path_settings: str,
        project_name: str,
        path_project: str,
        necessary_structure: list,
        logging_structure: dict,
        environment_structure: dict,
        *args, **kwargs,
    ) -> None:

        self.framework = framework
        self.main_path = main_path
        self.path_settings = path_settings
        self.project_name = project_name
        self.path_project = path_project
        self.necessary_structure = necessary_structure
        self.logging_structure = logging_structure
        self.environment_structure = environment_structure


    def create_files(self) -> None:
        """
        Способ создания вспомогательных файлов в проекте

        Method of creating auxiliary files in the project
        """

        for file in self.necessary_structure:
            if not os.path.exists(file):
                with open(file, 'w'): pass
                print(f"File created: {file}")
            else:
                print(f"File already exists: {file}")

        return None


    def logging_configure(self) -> None:
        """
        Метод настройки логирования в проекте

        Logging setup method in the project
        """

        return None


    def environment_configure(self) -> None:
        """
        Способ создания конфигурации
            для работы с виртуальным окружением

        Method for creating a configuration 
            for working with a virtual environment
        """

        variables_data = {}

        settings = FileIOController.read_data_from_file(
            path_to_file=self.path_settings,
        )

        variables = [
            node.id for node in walk(parse(settings)) 
                    if isinstance(node, Name) and node.id in self.environment_structure["variable"]
        ]

        module = SourceFileLoader("settings", str(self.path_settings)).load_module()

        for variable in variables: # Получение элементов для генерации переменных для замены их из файла .env
            _vars = getattr(module, variable)
            variables_data[variable] = _vars

        for key, value in variables_data.items(): # Запись данных в файл .env из указанного списка environment_structure
            FileIOController.write_in_file(
                file=self.environment_structure["location_environment"],
                values=f"{key}={value}",
            )
        
        for key, value in variables_data.items(): # Замена данных в файле settings.py
            FileIOController.replace_data_from_file(
                file=self.path_settings,
                string_be_replaced=f"{key} = {value}",
                values=f"{key} = os.environ.get({key})",
            )

        FileIOController.add_beginning_in_file( # Замена структуры файла 
            file_to_append_structure=self.path_settings,
            path_to_structure=self.main_path + "/structure/" + self.framework + "/env_structure.txt",
        )

        return None

    def execute(self) -> tuple:
        """
        Внедрение методов построения проектов
            (последовательность важна)

        Implementation of project building methods 
            (Consistency is important)
        """

        create_files = ExceptionState.method_processing(
            function = self.create_files,
            text="Create files",
        )# first method in line

        logging_configure = ExceptionState.method_processing(
            function = self.logging_configure,
            text="Create logging configurations",
        )# second method in line

        environment_configure = ExceptionState.method_processing(
            function = self.environment_configure,
            text="Create environment configure",
        )# third method in line

        return {
            "create_files": create_files,
            "logging_configure": logging_configure,
            "environment_configure": environment_configure,
        }



class DjangoConfigurations(ConfigurationController):
    """
    Configuration 
    """

    def __init__(
        self, 
        framework: str, 
        main_path: str, 
        project_name: str, 
        path_project: str, 
        *args, **kwargs,
    ) -> None:

        self.project_name = project_name
        self.path_project = path_project
        
        path_settings = path_project / project_name / project_name / "settings.py"
        location_environment = self.path_project / self.project_name / ".env"

        environment_structure = {
            "name": ".env",
            "location_environment": location_environment,
            "structure": "env_structure.txt",
            "variable": [
                "DEBUG",
                "SECRET_KEY",
                "ALLOWED_HOSTS",
            ]
        }
        logging_structure = { }

        necessary_structure = [ # Structure files to be created
            location_environment,
            path_settings,

            # ...
        ]


        super().__init__(
            framework = framework,
            main_path = main_path,
            project_name = project_name,
            path_project = path_project,
            path_settings = path_settings,
            necessary_structure = necessary_structure,
            logging_structure = logging_structure,
            environment_structure = environment_structure,
            *args, **kwargs,
        )


class FastAPIConfigurations(ConfigurationController):
    """
    Configuration 
    """

    def __init__(
        self, 
        framework: str, 
        main_path: str, 
        path_settings: str, 
        project_name: str, 
        path_project: str, 
        *args, **kwargs,
    ) -> None:

        logging_structure = { }
        environment_structure = { }
        necessary_structure = [ ]

        super().__init__(
            framework = framework,
            main_path = main_path,
            path_settings = path_settings,
            project_name = project_name,
            path_project = path_project, 
            necessary_structure = necessary_structure,
            logging_structure = logging_structure,
            environment_structure = environment_structure,
            *args, **kwargs,
        )


class FlaskConfigurations(ConfigurationController):
    """
    Configuration 
    """

    def __init__(
        self, 
        framework: str, 
        main_path: str, 
        path_settings: str, 
        project_name: str, 
        path_project: str, 
        *args, **kwargs,
    ) -> None:

        logging_structure = { }
        environment_structure = { }
        necessary_structure = [ ]

        super().__init__(
            framework = framework,
            main_path = main_path,
            path_settings = path_settings,
            project_name = project_name,
            path_project = path_project, 
            necessary_structure = necessary_structure,
            logging_structure = logging_structure,
            environment_structure = environment_structure,
            *args, **kwargs,
        )


class ProjectList:

    PROJECT_LIST = {
        "django": {
            "init_command": [ "django-admin", "startproject" ],
            "commands_project": [
                [ ],
            ],
            "requirements": [
                "django", "gunicorn", "psycopg2-binary", "python-dotenv", 
            ],
            "configurations": DjangoConfigurations,
        },
        "fastapi": {
            "init_command": [ ],
            "commands_project": [
                [ ],
            ],
            "requirements": [
                "fastapi", "uvicorn[standard]"
            ],
            "configurations": FastAPIConfigurations,
        },
        "flask": {
            "init_command": [ ],
            "commands_project": [
                [ ],
            ],
            "requirements": [
                "Flask", "uvicorn[standard]"
            ],
            "configurations": FlaskConfigurations,
        }
    }
