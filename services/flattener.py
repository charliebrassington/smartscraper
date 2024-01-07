import typing


class DataFlattenerService:

    def __init__(self):
        self._data = []

    def get_flattened_data(self, parsed_json: typing.Union[list, dict]) -> typing.List[str]:
        self._traverse(data=parsed_json)
        return self._data

    def _traverse(self, data: typing.Union[list, dict], path: str = "") -> None:
        if isinstance(data, dict):
            self._handle_dict(data, path)
        elif isinstance(data, list):
            self._handle_list(data, path)
        else:
            self._add_to_items(path, data)

    def _handle_dict(self, data, path):
        for key, value in data.items():
            self._traverse(value, path=f"{path}-{key}" if path else str(key))

    def _handle_list(self, data, path):
        for index, item in enumerate(data):
            self._traverse(data=item, path=path)

    def _add_to_items(self, path, data):
        self._data.append(f"{path}: {str(data)}")
