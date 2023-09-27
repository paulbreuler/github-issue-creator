"""
Module for testing the IssueManager class.
"""
import unittest
# Ensure the module is in the PYTHONPATH or adjust the import.
from create_gh_issues import IssueManager


class TestIssueExistsFunction(unittest.TestCase):
    """
    A class for testing issue_exists function of IssueManager class.
    """

    def test_issue_exists_with_invalid_repo(self):
        """
        Test issue_exists function with invalid repository.
        """
        manager = IssueManager()
        self.assertFalse(manager.issue_exists("some title", "invalid/repo"))

    # Add more test cases as needed


if __name__ == '__main__':
    unittest.main()
