from dataclasses import dataclass


__all__ = 'FieldsConfig', 'DEFAULT_FIELDS_CONFIG',


@dataclass
class FieldsConfig:
    id: str
    parent: str
    parent_id: str


DEFAULT_FIELDS_CONFIG = FieldsConfig(id='id', parent='parent', parent_id='parent_id')
