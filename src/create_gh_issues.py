# BEGIN: 9f7d8e5c8d9a
import json
import subprocess
from jsonschema import validate, ValidationError

class IssueManager:
    # Function to check if an issue with the given title exists
    def issue_exists(self, title, repo):


        command = ['gh', 'issue', 'list', '--repo', repo, '--json', 'title', '--state', 'all']
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"Error executing command: {result.stderr}")
            return False  # or raise an exception, depending on how you want to handle errors
        
        if not result.stdout.strip():
            return False  # No issues found
        
        try:
            issues = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return False  # or raise an exception, depending on how you want to handle errors
        
        return any(issue['title'] == title for issue in issues)

    def create_issues(self):
        
        with open('schema.json', 'r') as f:
            schema = json.load(f)

        # Load issues from JSON file
        with open('issues.json', 'r') as f:
            data = json.load(f)

        # Validate the loaded JSON data against the schema
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            print(f"JSON Validation Error: {e}")
            exit(1)

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

                        subprocess.run(command)
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

                    subprocess.run(command)
