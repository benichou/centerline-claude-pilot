"""YAML + Jinja2 prompt library for the doc-intelligence tools.

Prompts are authored as YAML files (a `system` persona/role + an `instruction` task body, each a Jinja2
template) so they are configuration, not hardcoded strings — reviewable and editable without touching the
tools. The shared expert persona lives once in `_shared.yaml` and is injected into every prompt; the document
catalog lives in `catalog.yaml` and is rendered into the classifier.

Usage:
    from centerline_mcp import prompts
    system, instruction = prompts.render("classify")
    system, instruction = prompts.render("extract_financial_statement")
"""

import os

import yaml
from jinja2 import Environment, FileSystemLoader

_DIR = os.path.dirname(os.path.abspath(__file__))
_env = Environment(loader=FileSystemLoader(_DIR), autoescape=False, trim_blocks=True, lstrip_blocks=True)


def _load_yaml(name):
    with open(os.path.join(_DIR, name), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


PERSONA = _load_yaml("_shared.yaml")["persona"]
DOC_TYPES = _load_yaml("catalog.yaml")["doc_types"]


def render(name, **ctx):
    """Return (system, instruction) for prompt `name`, Jinja-rendered with the shared persona + catalog + ctx."""
    spec = _load_yaml(f"{name}.yaml")
    context = {"persona": PERSONA, "doc_types": DOC_TYPES, **ctx}
    system = _env.from_string(spec["system"]).render(**context).strip()
    instruction = _env.from_string(spec["instruction"]).render(**context).strip()
    return system, instruction
