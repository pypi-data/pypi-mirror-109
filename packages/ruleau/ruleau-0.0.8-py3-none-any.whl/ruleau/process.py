from typing import AnyStr, Dict

from .rule import Rule


class Process:
    """Class holding rule process"""

    def __init__(
        self,
        process_id: str,
        name: str,
        description: str,
        flattened_rules: Dict[AnyStr, Rule],
        root_rule: Rule,
    ):
        self.id = process_id
        self.name = name
        self.description = description
        self.flattened_rules = flattened_rules
        self.root_rule = root_rule

    def parse(self):
        rules = []
        for rule in self.flattened_rules:
            parsed_rule = rule["rule"].parse()
            rules.append(
                {
                    "id": rule["id"],
                    "name": rule["name"],
                    "description": parsed_rule["description"],
                    "override_level": parsed_rule["override_level"],
                    "order": rule["order"],
                    "dependencies": rule["dependencies"],
                    "doctests": parsed_rule["doctests"],
                    "parameters": [
                        {"name": name, "value": value}
                        for name, value in parsed_rule["parameters"].items()
                    ],
                }
            )
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "root_rule": self.root_rule.id,
            "rules": rules,
        }
