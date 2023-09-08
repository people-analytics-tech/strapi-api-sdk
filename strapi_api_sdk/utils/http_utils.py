from typing import List, Union


def stringify_parameters(name: str, parameters: Union[dict, List[str], None]) -> dict:
    """Stringify dict for query parameters."""
    if type(parameters) is dict:
        return {name + k: v for k, v in flatten_parameters(parameters)}
    elif type(parameters) is str:
        return {name: parameters}
    elif type(parameters) is list:
        return {name: ','.join(parameters)}
    else:
        return {}


def flatten_parameters(parameters: dict):
    """Flatten parameters dict for query."""
    for key, value in parameters.items():
        if isinstance(value, dict):
            for key1, value1 in flatten_parameters(value):
                yield f'[{key}]{key1}', value1
        else:
            yield f'[{key}]', value 
