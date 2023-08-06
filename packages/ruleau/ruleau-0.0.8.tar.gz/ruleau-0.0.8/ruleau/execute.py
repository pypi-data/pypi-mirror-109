import logging
from copy import deepcopy
from json import dumps
from typing import Any, AnyStr, Dict, Iterable, Optional

from jsonpath_ng import parse

from ruleau.adapter import ApiAdapter
from ruleau.constants import OverrideLevel
from ruleau.exceptions import (
    CannotOverrideException,
    CaseIdRequiredException,
    DuplicateRuleIdException,
    DuplicateRuleNameException,
)
from ruleau.process import Process
from ruleau.rule import Rule
from ruleau.structures import RuleauDict

logger = logging.getLogger(__name__)


class DependantResults:
    def __init__(
        self,
        case_id: AnyStr,
        dependants: Iterable[Rule],
        payload: Dict[AnyStr, Any],
        api_adapter: Optional[ApiAdapter] = None,
        lazy: bool = False,
    ):
        self.case_id = case_id
        self.dependants = {dep.__name__: dep for dep in dependants}
        self.payload = deepcopy(payload)
        self.api_adapter = api_adapter
        self.results = {}
        if not lazy:
            for depend in dependants:
                self.run(depend.__name__)

    def run(self, name):
        """
        Run and store the result of a rule dependency
        :param name:
        :return:
        """

        if name not in self.dependants:
            raise AttributeError(
                f"Result for rule '{name}' not available, as it was not "
                f"declared as a dependency. "
                f"depends_on={dumps(list(self.dependants.keys()))}"
            )
        # If the result of rule execution is not set, run & cache it
        if name not in self.results:
            self.results[name] = execute_rule(
                self.case_id,
                self.dependants[name],
                self.payload,
                self.api_adapter,
            )
        # Return the rule execution result
        return self.results[name]

    def __getattr__(self, name):
        # Get the attribute otherwise, run the dependency
        return getattr(super(), name, self.run(name))

    def __iter__(self):
        # Iterate through the dependencies
        for dep in self.dependants:
            yield getattr(self, dep)


class ExecutionResult:
    def __init__(
        self,
        executed_rule: Rule,
        payload: RuleauDict,
        result,
        dependant_results: DependantResults,
        override: AnyStr = None,
        original_result: Optional[bool] = None,
    ):
        self.executed_rule = executed_rule
        self.payload = payload
        self.result = result
        self.override = override
        self.original_result = original_result
        self.dependant_results = dependant_results


def apply_override(
    case_id,
    executable_rule: Rule,
    execution_result: ExecutionResult,
    api_adapter: ApiAdapter,
):
    # Get overrides for the rule in a case
    override = api_adapter.fetch_override(case_id, executable_rule)

    # Apply override to the executed rule result, if any
    # Overrides should only be applied to allowed rule and if they're present
    if override:
        # Throw an exception if the backend is trying to override a NO_OVERRIDE rule
        if executable_rule.override_level == OverrideLevel.NO_OVERRIDE:
            raise CannotOverrideException(f"Cannot override {executable_rule.name}")
        else:
            # Override the rule result and set the overridden flag
            execution_result.override = override["id"]
            execution_result.original_result = execution_result.result
            execution_result.result = override["applied"]
    return execution_result


def execute_rule(
    case_id: AnyStr,
    executable_rule: Rule,
    payload: Dict[AnyStr, Any],
    api_adapter: Optional[ApiAdapter] = None,
):
    api_result = {}
    # Create the rule result so that the execution can store the result
    if api_adapter:
        api_result = api_adapter.create_result(case_id, executable_rule)
    # Prep the rule payload
    rule_payload = RuleauDict(payload)
    # Prep the dependent results
    depend_results = DependantResults(
        case_id,
        executable_rule.depends_on,
        payload,
        api_adapter,
        lazy=executable_rule.lazy_dependencies,
    )
    # Prepare execution result for context from all dependencies
    context = ExecutionResult(executable_rule, rule_payload, None, depend_results)
    # Prepare execution result for the rule to be executed
    execution_result = ExecutionResult(
        executable_rule,
        rule_payload,
        executable_rule(context, rule_payload),
        depend_results,
    )
    # Store the rule result
    if api_adapter:
        # Apply overrides on the rule result
        execution_result = apply_override(
            case_id, executable_rule, execution_result, api_adapter
        )

        api_adapter.update_result(
            case_id, executable_rule, api_result, execution_result
        )
    # Return the rule result
    return execution_result


def flatten_rules(rule: Rule, flattened_rules: list, order: int = 0):
    """Flatten the rule to find it's dependencies
    :param rule:
    :param flattened_rules: Output to append flattened results to
    :param order: Execution Order of the rule
    :return:
    """
    dependencies = {
        "id": rule.id,
        "rule": rule,
        "name": rule.name or rule.__name__,
        "dependencies": [],
    }
    # Check if there are any rule dependencies
    if len(rule.depends_on):
        # If yes, find the rule IDs
        for dependency in rule.depends_on:
            # Recursively flatten rules
            flatten_rules(dependency, flattened_rules, order + 1)
            # Append the rule as a dependency
            dependencies["dependencies"].append(dependency.id)
    # Set the order of the current rule
    dependencies["order"] = order
    # Append th
    flattened_rules.append(dependencies)
    return flattened_rules


def flatten_rule_objects(rule: Rule, flat_rules=None) -> [Rule]:
    if flat_rules is None:
        flat_rules = []
    flat_rules.append(rule)
    if len(rule.depends_on):
        for dependency in rule.depends_on:
            flatten_rule_objects(dependency, flat_rules)
    return flat_rules


def validate_no_duplicate_rule_names(rules: [Rule]) -> None:
    """Returns True if there are no duplicate Rule Names are used
    A name can only be re-used if the same rule is included multiple times
    """
    rules_dict = {}
    for rule in rules:
        if rule.name not in rules_dict:
            rules_dict[rule.name] = rule
        else:
            if rule != rules_dict[rule.name]:
                raise DuplicateRuleNameException()


def validate_no_duplicate_rule_ids(rules: [Rule]) -> None:
    """Returns True if there are no duplicate Rule IDs used
    An ID can only be re-used if the same rule is included multiple times
    """
    rules_dict = {}
    for rule in rules:
        if rule.id not in rules_dict:
            rules_dict[rule.id] = rule
        else:
            if rule != rules_dict[rule.id]:
                raise DuplicateRuleIdException()


def execute(
    root_rule: Rule,
    payload: Dict[AnyStr, Any],
    case_id_jsonpath: AnyStr = None,
    case_id: Optional[AnyStr] = None,
    api_adapter: Optional[ApiAdapter] = None,
) -> ExecutionResult:
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """

    # If neither case_id_jsonpath or case_id are present, raise exception
    if not case_id_jsonpath and not case_id:
        raise CaseIdRequiredException()

    # If case_id is not present in parameters, find it
    if not case_id:
        case_id_results = parse(case_id_jsonpath).find(payload)
        if not case_id_results:
            raise ValueError("Case ID not found in payload")
        case_id = str(case_id_results[0].value)

    # If there's no case ID, don't run
    if not case_id:
        raise ValueError("Case ID not found")

    # Validate unique rule name
    flattened_rules_as_objects = flatten_rule_objects(root_rule)
    validate_no_duplicate_rule_names(flattened_rules_as_objects)

    # Validate unique rule ids
    validate_no_duplicate_rule_ids(flattened_rules_as_objects)

    # If API adapter was was passed sync the case

    if api_adapter:
        rules = flatten_rules(root_rule, [], 0)
        rules = {
            rule["id"]: rule for rule in rules
        }.values()  # Hot fix: De-duplicate rules
        process = Process(
            root_rule.id, root_rule.name, root_rule.description, rules, root_rule
        )

        # Sync the process rules
        api_adapter.sync_process(process)

        # Sync the case
        api_adapter.sync_case(case_id, process.id, payload)
    # Trigger the rule execution, from the top level rule
    return execute_rule(case_id, root_rule, payload, api_adapter)
