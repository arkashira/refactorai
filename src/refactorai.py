import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict

@dataclass
class RefactoringAction:
    organization: str
    repository: str
    confidence: float
    cyclomatic_complexity: float
    timestamp: datetime

class RefactorAI:
    def __init__(self):
        self.actions = []
        self.api_key = None

    def add_action(self, action: RefactoringAction):
        self.actions.append(action)

    def get_weekly_metrics(self, organization: str = None, repository: str = None, start_date: datetime = None, end_date: datetime = None) -> Dict:
        filtered_actions = [action for action in self.actions if 
                            (organization is None or action.organization == organization) and 
                            (repository is None or action.repository == repository) and 
                            (start_date is None or action.timestamp >= start_date) and 
                            (end_date is None or action.timestamp <= end_date)]
        weekly_metrics = {}
        for action in filtered_actions:
            week_start = action.timestamp - timedelta(days=action.timestamp.weekday())
            week_key = week_start.strftime('%Y-%W')
            if week_key not in weekly_metrics:
                weekly_metrics[week_key] = {'total_actions': 0, 'confidence_sum': 0.0, 'cyclomatic_complexity_sum': 0.0}
            weekly_metrics[week_key]['total_actions'] += 1
            weekly_metrics[week_key]['confidence_sum'] += action.confidence
            weekly_metrics[week_key]['cyclomatic_complexity_sum'] += action.cyclomatic_complexity
        result = {}
        for week_key, metrics in weekly_metrics.items():
            result[week_key] = {
                'total_accepted_actions': metrics['total_actions'],
                'average_confidence': metrics['confidence_sum'] / metrics['total_actions'] if metrics['total_actions'] > 0 else 0.0,
                'reduction_in_cyclomatic_complexity': metrics['cyclomatic_complexity_sum'] / metrics['total_actions'] if metrics['total_actions'] > 0 else 0.0
            }
        return result

    def export_csv(self, metrics: Dict):
        csv_data = 'Week,Total Accepted Actions,Average Confidence,Reduction in Cyclomatic Complexity\n'
        for week_key, metric in metrics.items():
            csv_data += f'{week_key},{metric["total_accepted_actions"]},{metric["average_confidence"]},{metric["reduction_in_cyclomatic_complexity"]}\n'
        return csv_data

    def authenticate(self, api_key: str):
        self.api_key = api_key

    def update_dashboard(self):
        # Simulate updating the dashboard within 15 minutes
        pass
