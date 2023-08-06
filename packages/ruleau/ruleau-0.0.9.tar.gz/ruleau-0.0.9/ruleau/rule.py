import functools
import inspect
from typing import TYPE_CHECKING, AnyStr, List

import regex as re

from ruleau.constants import OverrideLevel
from ruleau.docs import clean_source, comments, description, doctests, parameters, title
from ruleau.exceptions import (
    RuleIdIllegalCharacterException,
    RuleRequiresIdException,
    RuleRequiresNameException,
)

if TYPE_CHECKING:
    from ruleau.types import Function


class Rule:
    def __init__(
        self,
        func: "Function",
        id: AnyStr,
        name: AnyStr,
        depends_on: List["Rule"],
        override_level: OverrideLevel,
        lazy_dependencies: bool,
    ):
        """
        :param func: User defined rule
        :param name: User defined human readable name of the rule
        :param depends_on: Rule dependencies
        :param override_level: Override level
        :param lazy_dependencies: Flag to switch loading of rule dependencies lazily
        """
        self.id = id
        self.name = name
        # Validate the rule, make sure the name is always set for a rule
        self.validate()
        # Set the user defined function
        self.func = func
        self.depends_on = depends_on
        self.override_level = override_level
        self.__name__ = func.__name__
        self.lazy_dependencies = lazy_dependencies

        # This preserves the original Docstring on the decorated function
        # which allows DocTest to detect the function
        functools.update_wrapper(self, func)

    def __str__(self) -> str:
        return self.__name__

    def __call__(self, *args, **kwargs) -> bool:
        return self.func(*args, **kwargs)

    def validate(self):
        """
        Validator to check if top level rule has a human readable name and
        and id
        :raises: TopLevelRuleRequiresNameException
        :raises: RuleRequiresIdException
        """
        if not self.name or not isinstance(self.name, str):
            raise RuleRequiresNameException()
        if not self.id or not isinstance(self.id, str):
            raise RuleRequiresIdException()

        # Validate the Rule ID
        if not re.match(r"^([a-zA-Z0-9-_.~]+)+$", self.id):
            raise RuleIdIllegalCharacterException()

    def _get_source(self) -> AnyStr:
        return clean_source(inspect.getsource(self.func))

    @property
    def description(self) -> AnyStr:
        return description(self.func.__doc__)

    def parse(self):
        return {
            "function_name": self.__name__,
            "id": self.id,
            "name": self.name,
            "title": title(self.__name__),
            "override_level_name": self.override_level.name,
            "override_level": self.override_level.value,
            "source": self._get_source(),
            "comments": comments(self._get_source()),
            "docstring": self.func.__doc__,
            "description": self.description,
            "parameters": parameters(self.func.__doc__),
            "dependencies": [dependent.parse() for dependent in self.depends_on],
            "doctests": doctests(self.func),
        }
