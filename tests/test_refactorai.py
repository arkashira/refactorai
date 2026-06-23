import pytest
from src.refactorai import RefactorAI, RefactoringAction
from datetime import datetime, timedelta

def test_get_weekly_metrics():
    refactor_ai = RefactorAI()
    action1 = RefactoringAction('org1', 'repo1', 0.8, 10.0, datetime(2022, 1, 3))
    action2 = RefactoringAction('org1', 'repo1', 0.9, 12.0, datetime(2022, 1, 10))
    refactor_ai.add_action(action1)
    refactor_ai.add_action(action2)
    metrics = refactor_ai.get_weekly_metrics()
    assert len(metrics) == 2
    week_key1 = (datetime(2022, 1, 3) - timedelta(days=datetime(2022, 1, 3).weekday())).strftime('%Y-%W')
    week_key2 = (datetime(2022, 1, 10) - timedelta(days=datetime(2022, 1, 10).weekday())).strftime('%Y-%W')
    assert metrics[week_key1]['total_accepted_actions'] == 1
    assert metrics[week_key2]['total_accepted_actions'] == 1

def test_get_weekly_metrics_filtered():
    refactor_ai = RefactorAI()
    action1 = RefactoringAction('org1', 'repo1', 0.8, 10.0, datetime(2022, 1, 3))
    action2 = RefactoringAction('org1', 'repo2', 0.9, 12.0, datetime(2022, 1, 10))
    refactor_ai.add_action(action1)
    refactor_ai.add_action(action2)
    metrics = refactor_ai.get_weekly_metrics(organization='org1', repository='repo1')
    assert len(metrics) == 1
    week_key1 = (datetime(2022, 1, 3) - timedelta(days=datetime(2022, 1, 3).weekday())).strftime('%Y-%W')
    assert metrics[week_key1]['total_accepted_actions'] == 1

def test_export_csv():
    refactor_ai = RefactorAI()
    metrics = {
        '2022-01': {'total_accepted_actions': 1, 'average_confidence': 0.8, 'reduction_in_cyclomatic_complexity': 10.0},
        '2022-02': {'total_accepted_actions': 1, 'average_confidence': 0.9, 'reduction_in_cyclomatic_complexity': 12.0}
    }
    csv_data = refactor_ai.export_csv(metrics)
    assert csv_data.startswith('Week,Total Accepted Actions,Average Confidence,Reduction in Cyclomatic Complexity\n')
    assert '2022-01,1,0.8,10.0' in csv_data
    assert '2022-02,1,0.9,12.0' in csv_data

def test_authenticate():
    refactor_ai = RefactorAI()
    refactor_ai.authenticate('api_key')
    assert refactor_ai.api_key == 'api_key'
