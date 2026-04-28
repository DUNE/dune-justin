from collections import defaultdict
from .components.filterForm import Option

def extract_rows_unique_value(rows: list[dict]) -> dict[str, list]:
    if not isinstance(rows, list):
      raise ValueError("Expected a list of dictionaries")
    if len(rows) == 0:
      return {}
    if not isinstance(rows[0], dict):
      raise ValueError("Expected a list of dictionaries")

    unique_values = defaultdict(set)
    keys = rows[0].keys()

    for row in rows:
      if not isinstance(row, dict) or set(row.keys()) != set(keys):
        raise ValueError("All rows must be dictionaries with the same keys")
      for k in keys:
        unique_values[k].add(row[k])

    # avoid sorting issues with None
    return {k: sorted([x for x in v if x is not None]) for k, v in unique_values.items()}

def parse_cgi_value(cgiValues:dict[str, str], keys: list[str], default_value = Option.default_value) -> dict[str, str]:
  if not isinstance(cgiValues, dict):   raise ValueError("Expected a dictionary for cgiValues")
  if not isinstance(keys, list):        raise ValueError("Expected a list for keys")
  result = {}

  for key in keys:
    value = cgiValues.get(key)

    if value and value != default_value:
      result[key] = str(value)
    else:
      result[key] = None

  return result
    