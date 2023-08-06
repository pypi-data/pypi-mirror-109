from typing import Callable

from ruleau.execute import ExecutionResult
from ruleau.structures import RuleauDict

Function = Callable[[ExecutionResult, RuleauDict], bool]
