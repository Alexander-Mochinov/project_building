from enum import Enum
from typing import Any


class ExecutionState:
    """
    Класс для генерации выполнения команды

    Class generations execute state
    """

    class CodeStatus(Enum):

        SUCCESS = "success"
        ERROR = "failure"

    def __init__(self, *args, **kwargs,) -> None:
        pass

    @staticmethod    
    def set_success_or_failure_command(
        text: str,
        method: Any,
        status: CodeStatus,
        params: dict = None,
        exception: Exception = None,
        result_execute: Any = None,
    ) -> dict:

        """
        Обработка ошибок и метод сбора для генерации
            словаря успешных или неудачных команд

        Error handling and collection method for generation
            dictionary of successful or failed commands
        """

        return {
            "text": text,
            "params": params,
            "status": status,
            "exception": exception,
            "execute_method": method,
            "result_execute": result_execute,
            "is_execute": False if exception else True,
        }
