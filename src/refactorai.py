import json
from dataclasses import dataclass
from typing import List

@dataclass
class Suggestion:
    file: str
    line: int
    description: str
    code_change: str

class RefactorAI:
    def __init__(self):
        self.suggestions = []
        self.dismissed_suggestions = set()

    def scan_workspace(self):
        # Simulate scanning the workspace and generating suggestions
        self.suggestions = [
            Suggestion("file1.py", 10, "Suggestion 1", "print('Hello World')"),
            Suggestion("file2.py", 20, "Suggestion 2", "print('Hello Universe')"),
        ]

    def get_suggestions(self):
        return [s for s in self.suggestions if (s.file, s.line) not in self.dismissed_suggestions]

    def apply_suggestion(self, suggestion):
        # Simulate applying the suggestion and staging the file in Git
        print(f"Applying suggestion: {suggestion.description}")
        print(f"Staging file: {suggestion.file}")

    def dismiss_suggestion(self, suggestion):
        self.dismissed_suggestions.add((suggestion.file, suggestion.line))

    def save_dismissed_suggestions(self):
        with open("dismissed_suggestions.json", "w") as f:
            json.dump([list(s) for s in self.dismissed_suggestions], f)

    def load_dismissed_suggestions(self):
        try:
            with open("dismissed_suggestions.json", "r") as f:
                self.dismissed_suggestions = set(tuple(s) for s in json.load(f))
        except FileNotFoundError:
            pass
