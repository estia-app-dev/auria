from typing import Union, Dict, List

from jsonschema import FormatChecker, Draft7Validator, ValidationError

from AuriaException import JsonSchemaException


class JsonSchemaValidator:

  def __init__(self, schema: Dict, json: Union[Dict, List]):
    if not isinstance(json, dict) and not isinstance(json, list):
      raise JsonSchemaException('Invalid JSON', [ValidationError(message='JSON can\'t be empty')])

    if not isinstance(schema, dict):
      raise Exception("Schema is not valid")

    self.schema: Dict = schema
    self.json: Union[Dict, List] = json

    # On rajoute quelques info
    self.schema['$schema'] = "http://json-schema.org/schema#"
    self.schema['additionalproperties'] = False

  def validate(self):
    # Trim
    if 'trim' in self.schema:
      for key in self.schema.get('trim', []):
        value = self.json.get(key)
        if isinstance(value, str):
          self.json[key] = value.strip()

    # On valide le schema
    v = Draft7Validator(self.schema, format_checker=FormatChecker())
    errors = list(v.iter_errors(self.json))

    # Un liste vide est évaluée à False en Python
    if errors:
      raise JsonSchemaException("Invalid json", errors)
