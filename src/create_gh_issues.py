"""
Module for managing GitHub issues using GitHub CLI.
"""
import json
import subprocess
import sys
# Ensure jsonschema is installed in your environment.
from jsonschema import validate, ValidationError


class IssueManager:
    """
    A class for managing GitHub issues.
    """

    def issue_exists(self, title, repo):
        """
        Check if an issue with the given title exists in the repository.
        """
        command = ['gh', 'issue', 'list', '--repo',
                   repo, '--json', 'title', '--state', 'all']
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)

        if result.returncode != 0:
            print(f"Error executing command: {result.stderr.strip()}")
            return False

        if not result.stdout.strip():
            return False

        try:
            issues = json.loads(result.stdout)
        except json.JSONDecodeError as json_err:
            print(f"Error decoding JSON: {json_err}")
            return False

        return any(issue['title'] == title for issue in issues)

    def create_issues(self):
        """
        Create GitHub issues as per the details provided in JSON file.
        """
        with open('schema.json', 'r', encoding='utf-8') as schema_file:
            schema = json.load(schema_file)

        with open('issues.json', 'r', encoding='utf-8') as issues_file:
            data = json.load(issues_file)

        try:
            validate(instance=data, schema=schema)
        except ValidationError as validation_err:
            print(f"JSON Validation Error: {validation_err}")
            sys.exit(1)

        milestone = data['milestone']
        repo = data['repo']

        # Loop through each category in the JSON file
        for category in data['categories']:
            main_section = category['section']

            # Check if 'sub_sections' exist
            if 'sub_sections' in category:
                # Loop through each sub-section in the category
                for sub_section in category['sub_sections']:
                    sub_section_name = sub_section['section']

                    # Loop through each issue in the sub-section
                    for issue in sub_section['issues']:
                        title = f"{main_section} | {sub_section_name} | {issue['title']}"

                        # Skip if the title is a duplicate
                        if self.issue_exists(title, repo):
                            print(f"Skipped duplicate issue: {title}")
                            continue

                        tags = ','.join(issue['tags'])
                        description = issue['description']

                        # Create the GitHub issue
                        command = [
                            'gh', 'issue', 'create',
                            '--repo', repo,
                            '--title', title,
                            '--body', description,
                            '--label', tags,
                            '--milestone', milestone
                        ]

                        subprocess.run(command, check=True)
            else:
                # Handle the case where no 'sub_sections' exist
                for issue in category['issues']:
                    title = f"{main_section} | {issue['title']}"

                    # Skip if the title is a duplicate
                    if self.issue_exists(title, repo):
                        print(f"Skipped duplicate issue: {title}")
                        continue

                    tags = ','.join(issue['tags'])
                    description = issue['description']

                    # Create the GitHub issue
                    command = [
                        'gh', 'issue', 'create',
                        '--repo', repo,
                        '--title', title,
                        '--body', description,
                        '--label', tags,
                        '--milestone', milestone
                    ]

                    subprocess.run(command, check=True)
