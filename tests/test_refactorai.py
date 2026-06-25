import pytest
from src.refactorai import RefactorAI, Suggestion, FileAnalysis

def test_analyze_pull_request_enabled_repository():
    repository_permissions = {
        'repo1': True,
    }
    refactor_ai = RefactorAI(repository_permissions)

    pull_request = {
        'repository': 'repo1',
        'changed_files': ['file1.py', 'file2.py'],
    }

    analyses = refactor_ai.analyze_pull_request(pull_request)
    assert len(analyses) == 2

def test_analyze_pull_request_disabled_repository():
    repository_permissions = {
        'repo1': False,
    }
    refactor_ai = RefactorAI(repository_permissions)

    pull_request = {
        'repository': 'repo1',
        'changed_files': ['file1.py', 'file2.py'],
    }

    analyses = refactor_ai.analyze_pull_request(pull_request)
    assert len(analyses) == 0

def test_analyze_file():
    refactor_ai = RefactorAI({})

    file_name = 'file1.py'
    suggestions = refactor_ai.analyze_file(file_name)
    assert len(suggestions) == 3

def test_post_comment():
    refactor_ai = RefactorAI({})

    file_analysis = FileAnalysis('file1.py', [
        Suggestion(1, 'code snippet 1', 'apply link 1'),
        Suggestion(2, 'code snippet 2', 'apply link 2'),
        Suggestion(3, 'code snippet 3', 'apply link 3'),
    ])

    comment = refactor_ai.post_comment(file_analysis)
    assert 'File: file1.py' in comment
    assert 'Line 1: code snippet 1 (apply link 1)' in comment
    assert 'Line 2: code snippet 2 (apply link 2)' in comment
    assert 'Line 3: code snippet 3 (apply link 3)' in comment

def test_log_activity():
    refactor_ai = RefactorAI({})

    activity = 'Comment posted on file1.py'
    refactor_ai.log_activity(activity)
    # No assertion, just checking that it runs without error
