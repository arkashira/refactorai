from dataclasses import dataclass
from typing import Dict, List
import ast


@dataclass
class Codebase:
    """Container for uploaded source files."""
    files: Dict[str, str]


@dataclass
class FunctionInfo:
    """Simple representation of a function extracted from source."""
    name: str
    line_count: int


@dataclass
class Analysis:
    """Result of a “training” step – mapping filenames to discovered functions."""
    functions: Dict[str, List[FunctionInfo]]  # filename -> list of functions


def upload_codebase(files: Dict[str, str]) -> Codebase:
    """
    Validate and wrap a dictionary of filename → source code.

    Raises:
        TypeError: If ``files`` is not a dict.
        ValueError: If any key or value is not a string.
    """
    if not isinstance(files, dict):
        raise TypeError("files must be a dict")
    for k, v in files.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ValueError("filenames and code must be strings")
    return Codebase(files=files)


def _extract_functions(source: str) -> List[FunctionInfo]:
    """
    Parse ``source`` with ``ast`` and return a list of ``FunctionInfo`` objects.
    Files that cannot be parsed are ignored (return empty list).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []  # unparsable source – treat as having no functions

    functions: List[FunctionInfo] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # ``end_lineno`` is available on Python 3.8+; fallback to ``lineno``.
            end = getattr(node, "end_lineno", node.lineno)
            line_count = end - node.lineno + 1
            functions.append(FunctionInfo(name=node.name, line_count=line_count))
    return functions


def train_model(codebase: Codebase) -> Analysis:
    """
    “Train” a model by extracting function metadata from each file.
    Returns an ``Analysis`` object that can be fed to ``generate_recommendations``.
    """
    functions_by_file: Dict[str, List[FunctionInfo]] = {}
    for filename, source in codebase.files.items():
        funcs = _extract_functions(source)
        if funcs:
            functions_by_file[filename] = funcs
    return Analysis(functions=functions_by_file)


def generate_recommendations(analysis: Analysis, max_func_len: int = 20) -> List[str]:
    """
    Produce human‑readable refactoring suggestions for functions longer than ``max_func_len``.
    """
    recommendations: List[str] = []
    for filename, funcs in analysis.functions.items():
        for func in funcs:
            if func.line_count > max_func_len:
                recommendations.append(
                    f"In {filename}, function '{func.name}' is {func.line_count} lines long; "
                    f"consider refactoring."
                )
    return recommendations
