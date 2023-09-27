# GitHub Issue Creator

## Overview

This Python script automates the process of creating GitHub issues. It reads a JSON file containing the issues' details and uses the `gh` CLI to create the issues in a specified GitHub repository.

## Features

- **Validation**: Validates the input JSON file against a predefined schema to ensure correctness.
- **Duplication Check**: Checks whether an issue with the same title already exists in the repository to avoid duplicates.
- **Customization**: Allows creating issues under specific milestones and with specific tags.
- **Organization**: Supports categorization and sub-categorization to organize issues effectively.

## Prerequisites

- [gh CLI](https://github.com/cli/cli#installation): The GitHub CLI tool must be installed and configured on your machine.
- Python 3.x: The script is written in Python 3.
- [jsonschema](https://pypi.org/project/jsonschema/): Python package used for validating JSON data against a schema. Install it using pip:
  ```sh
  pip install jsonschema
  ```

## Usage

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd <repository-dir>
   ```

2. **Prepare the JSON File:**
   Create a JSON file (`issues.json`) with the details of the issues to be created. Refer to `schema.json` for the expected structure.

3. **Run the Script:**
   ```sh
   python create_gh_issues.py
   ```

## JSON Structure

The JSON file should adhere to the structure defined in `schema.json`. Here’s a brief overview:

- **milestone**: The milestone to associate the issues with.
- **repo**: The GitHub repository where the issues will be created.
- **categories**: An array of categories, each containing:
  - **section**: The main section or category of the issue.
  - **sub_sections** (optional): An array of sub-sections, each containing:
    - **section**: The sub-section of the issue.
    - **issues**: An array of issues belonging to this sub-section.
- **issues**: An array of issues belonging to the main section if there are no sub-sections.

### Example

```json
{
  "milestone": "v1.0",
  "repo": "username/repository",
  "categories": [
    {
      "section": "Bug",
      "sub_sections": [
        {
          "section": "UI",
          "issues": [
            {
              "title": "Button Alignment",
              "description": "The submit button is misaligned.",
              "tags": ["frontend", "bug"]
            }
          ]
        }
      ]
    }
  ]
}
```

A good way to create this JSON is to provide chat GPT the schema.json and in markdown the issues you want to create. The follwing markdown can be converted into JSON by GPT in one prompt provide the correct input.

```Markdown
### Features
#### Audio and Video
1. Issue: Implement Audio Streaming
   - Tag: `Feature`, `Audio`
   - Description: Enable streaming of audio to allow users to communicate within the application.

2. Issue: Add Video Support
   - Tag: `Feature`, `Video`
   - Description: Incorporate video capabilities to enhance user interaction and engagement.

#### Text Communication
3. Issue: Integrate Chat System
   - Tag: `Feature`, `Chat`
   - Description: Implement a chat system to enable text communication between users.

### Bugs
1. Issue: Fix Login Timeout
   - Tag: `Bug`, `Authentication`
   - Description: Resolve the issue where users are timed out prematurely while logging in.

2. Issue: Resolve Chat Delay
   - Tag: `Bug`, `Chat`
   - Description: Fix delays in the chat system which are affecting real-time user communication.
```


## Testing

To run the tests, use the following command:

```sh
python -m unittest test_create_gh_issues.py
```

## Contributing

Feel free to fork the repository and submit pull requests for any enhancements, fixes, or features you add.

## License

This project is open source and available under the [MIT License](LICENSE).

```

Make sure to customize the content to fit the actual details and requirements of your project, including the repository URL, directory names, JSON structure, etc.