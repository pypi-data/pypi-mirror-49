import calendar
import datetime
import time
from typing import Dict, Any


class SafeEval:

    def __init__(self) -> None:
        self._prefix = '>>>'
        self._globals = {
            '__builtins__': None
        }
        self._forbidden = ['__', '**']
        self._safe_builtins = {
            'abs': abs,
            'calendar': calendar,
            'datetime': datetime,
            'float': float,
            'int': int,
            'max': max,
            'min': min,
            'round': round,
            'str': str,
            'sum': sum,
            'time': time
        }

    def __call__(self, expression: str, locals: Dict[str, Any] = None) -> Any:
        if not expression.startswith(self._prefix) or any(
                character in expression for character in self._forbidden):
            return expression

        if not locals:
            locals = {}

        expression = expression.replace(self._prefix, '').strip()
        locals.update(self._safe_builtins)

        return eval(expression, self._globals, locals)
