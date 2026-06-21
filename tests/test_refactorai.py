import pytest
from refactorai import RefactorAI, Suggestion

@pytest.fixture
def refactor_ai():
    repository_permissions = {"owner1": True, "owner2": False}
    return RefactorAI(repository_permissions)

def test_analyze_changed_files(refactor_ai):
    changed_files = ["file1.py", "file2.py"]
    suggestions = refactor_ai.analyze_changed_files(changed_files)
    assert len(suggestions) == 6

def test_analyze_file(refactor_ai):
    file = "file1.py"
    suggestions = refactor_ai.analyze_file(file)
    assert len(suggestions) == 3

def test_post_comment(refactor_ai):
    suggestions = [Suggestion(1, "Code snippet 1", "https://example.com/apply/1")]
    refactor_ai.post_comment(suggestions, "owner1")
    # No assertion, just checking that it runs without error

def test_post_comment_disabled(refactor_ai):
    suggestions = [Suggestion(1, "Code snippet 1", "https://example.com/apply/1")]
    refactor_ai.post_comment(suggestions, "owner2")
    # No assertion, just checking that it runs without error

def test_log_activity(refactor_ai):
    activity = "Comment posted"
    refactor_ai.log_activity(activity)
    # No assertion, just checking that it runs without error
