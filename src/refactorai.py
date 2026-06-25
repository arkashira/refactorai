import json
from dataclasses import dataclass
from typing import List

@dataclass
class Suggestion:
    line_number: int
    code_snippet: str
    apply_link: str

@dataclass
class FileAnalysis:
    file_name: str
    suggestions: List[Suggestion]

class RefactorAI:
    def __init__(self, repository_permissions):
        self.repository_permissions = repository_permissions

    def analyze_pull_request(self, pull_request):
        if not self.repository_permissions.get(pull_request['repository'], False):
            return []

        changed_files = pull_request.get('changed_files', [])
        analyses = []

        for file in changed_files:
            suggestions = self.analyze_file(file)
            analyses.append(FileAnalysis(file, suggestions))

        return analyses

    def analyze_file(self, file_name):
        # Simulate file analysis
        suggestions = [
            Suggestion(1, 'code snippet 1', 'apply link 1'),
            Suggestion(2, 'code snippet 2', 'apply link 2'),
            Suggestion(3, 'code snippet 3', 'apply link 3'),
        ]
        return suggestions[:3]  # Return top 3 suggestions

    def post_comment(self, file_analysis):
        comment = f'File: {file_analysis.file_name}\n'
        for suggestion in file_analysis.suggestions:
            comment += f'Line {suggestion.line_number}: {suggestion.code_snippet} ({suggestion.apply_link})\n'
        return comment

    def log_activity(self, activity):
        print(f'Logging activity: {activity}')

def main():
    repository_permissions = {
        'repo1': True,
        'repo2': False,
    }
    refactor_ai = RefactorAI(repository_permissions)

    pull_request = {
        'repository': 'repo1',
        'changed_files': ['file1.py', 'file2.py'],
    }

    analyses = refactor_ai.analyze_pull_request(pull_request)
    for analysis in analyses:
        comment = refactor_ai.post_comment(analysis)
        print(comment)
        refactor_ai.log_activity(f'Comment posted on {analysis.file_name}')

if __name__ == '__main__':
    main()
