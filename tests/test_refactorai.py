import pytest
import json
from refactorai import RefactorAI, Suggestion

def test_scan_workspace():
    refactorai = RefactorAI()
    refactorai.scan_workspace()
    assert len(refactorai.get_suggestions()) == 2

def test_get_suggestions():
    refactorai = RefactorAI()
    refactorai.scan_workspace()
    suggestions = refactorai.get_suggestions()
    assert suggestions[0].file == "file1.py"
    assert suggestions[1].line == 20

def test_apply_suggestion():
    refactorai = RefactorAI()
    suggestion = Suggestion("file1.py", 10, "Suggestion 1", "print('Hello World')")
    refactorai.apply_suggestion(suggestion)
    # No assertion, just checking that it runs without error

def test_dismiss_suggestion():
    refactorai = RefactorAI()
    suggestion = Suggestion("file1.py", 10, "Suggestion 1", "print('Hello World')")
    refactorai.dismiss_suggestion(suggestion)
    assert (suggestion.file, suggestion.line) in refactorai.dismissed_suggestions

def test_save_dismissed_suggestions():
    refactorai = RefactorAI()
    suggestion = Suggestion("file1.py", 10, "Suggestion 1", "print('Hello World')")
    refactorai.dismiss_suggestion(suggestion)
    refactorai.save_dismissed_suggestions()
    with open("dismissed_suggestions.json", "r") as f:
        assert json.load(f) == [["file1.py", 10]]

def test_load_dismissed_suggestions():
    refactorai = RefactorAI()
    suggestion = Suggestion("file1.py", 10, "Suggestion 1", "print('Hello World')")
    with open("dismissed_suggestions.json", "w") as f:
        json.dump([["file1.py", 10]], f)
    refactorai.load_dismissed_suggestions()
    assert (suggestion.file, suggestion.line) in refactorai.dismissed_suggestions
