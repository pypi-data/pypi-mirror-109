from typing import Dict, List, Optional
import aws_cdk.aws_appsync as appsync
import inspect


class EdgeAppsyncMappingTemplate:

    def __init__(self, mapping_template_string: str):
        self.string = self._clean(mapping_template_string)

    def __add__(self, other):
        if isinstance(other, EdgeAppsyncMappingTemplate):
            return EdgeAppsyncMappingTemplate(self._clean(self.string + other.string))
        raise NotImplementedError()

    def render(self):
        return appsync.MappingTemplate.from_string(self.string)

    @staticmethod
    def _clean(string: str):
        return inspect.cleandoc(string)


class EdgeAppsyncMappingTemplateMacro(EdgeAppsyncMappingTemplate):

    def __init__(self, argument_names: List[str], mapping_template_string: str, return_name: str):
        for argument_name in argument_names:
            assert argument_name[0] == "$"
        assert return_name[0] == "$"

        super().__init__(mapping_template_string)
        self._argument_names = argument_names
        self._return_name = return_name

    def __call__(self, argument_definitions: Dict[str, Optional[EdgeAppsyncMappingTemplate]]):
        assert set(argument_definitions.keys()) == set(self._argument_names)

        execution_mapping_template = EdgeAppsyncMappingTemplate("")
        for argument_name in sorted(argument_definitions.keys()):
            if argument_definitions[argument_name]:
                execution_mapping_template += argument_definitions[argument_name]
        execution_mapping_template += self
        return execution_mapping_template

    @property
    def return_name(self):
        return self._return_name
