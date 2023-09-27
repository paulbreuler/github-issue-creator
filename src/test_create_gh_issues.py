import unittest
from create_gh_issues import IssueManager

class TestIssueExistsFunction(unittest.TestCase):

    def test_issue_exists_with_invalid_repo(self):
        manager = IssueManager()  # Don't forget to instantiate the class
        self.assertFalse(manager.issue_exists("some title", "invalid/repo"))
        
    # Add more test cases as needed
    
if __name__ == '__main__':
    unittest.main()
