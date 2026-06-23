# RefactorAI
RefactorAI is a dashboard that shows weekly accepted refactoring actions and their effect on code-quality metrics.

## Usage
1. Create a RefactorAI instance: `refactor_ai = RefactorAI()`
2. Add refactoring actions: `refactor_ai.add_action(RefactoringAction('org1', 'repo1', 0.8, 10.0, datetime(2022, 1, 3)))`
3. Get weekly metrics: `metrics = refactor_ai.get_weekly_metrics()`
4. Export CSV: `csv_data = refactor_ai.export_csv(metrics)`
5. Authenticate: `refactor_ai.authenticate('api_key')`
