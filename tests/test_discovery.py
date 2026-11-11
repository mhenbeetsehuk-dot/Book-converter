import unittest
from unittest.mock import patch
from learning.discovery import discover, github_repositories

class DiscoveryTests(unittest.TestCase):
    def test_short_query(self):
        with self.assertRaises(ValueError):
            github_repositories("x")
    @patch("learning.discovery.github_repositories")
    @patch("learning.discovery.research_papers")
    def test_results(self, papers, repos):
        repos.return_value = [{"name": "example/repo"}]
        papers.return_value = [{"title": "Example paper"}]
        result = discover("procedural animation")
        self.assertEqual(len(result["results"]), 2)
        self.assertFalse(result["errors"])
    @patch("learning.discovery.github_repositories", side_effect=OSError("offline"))
    @patch("learning.discovery.research_papers", return_value=[])
    def test_offline(self, papers, repos):
        result = discover("procedural animation")
        self.assertEqual(result["errors"][0]["source"], "github")

if __name__ == "__main__":
    unittest.main()
