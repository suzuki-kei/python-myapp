import yaml

import box


def _load_yaml_file(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def load_config(file_path):
    return box.Box(
            _load_yaml_file(file_path),
            frozen_box=True,
            default_box=True,
    )

