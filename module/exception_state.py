from typing import Any
from .systems_module import ExecutionState


class ExceptionState:
    """
    Класс для обработки команд
        и отлов ошибки

    Class for processing commands 
        and catching errors
    """

    @staticmethod
    def method_processing(
        text: str,
        function: Any,
        params: dict = {},
    ) -> ExecutionState:
        """
        Метод для обработки команд
            и отлов ошибки

        Method for processing commands 
            and catching errors
        """

        try:
            result_execute = function(**params) # Execute command
            return ExecutionState.set_success_or_failure_command(
                text=text,
                params=params,
                method=function,
                result_execute=result_execute,
                status=ExecutionState.CodeStatus.SUCCESS,
            )

        except Exception as error:
            print(error)
            return ExecutionState.set_success_or_failure_command(
                text=text,
                params=params,
                method=function,
                status=ExecutionState.CodeStatus.ERROR,
                exception=error,
            )
