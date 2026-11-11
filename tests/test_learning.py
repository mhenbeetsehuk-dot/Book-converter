import tempfile
import unittest
from learning.registry import Capability, save_capability, load_capability

class RegistryTests(unittest.TestCase):
    def test_roundtrip(self):
        c = Capability("Rigging", "Character rigging", "https://docs.blender.org", "GPL-3.0", "Study documented rigging workflow")
        with tempfile.TemporaryDirectory() as folder:
            path = save_capability(c, folder)
            self.assertEqual(load_capability(str(path)).name, "Rigging")
    def test_reject_unapproved(self):
        c = Capability("Test", "Task", "https://example.com", "MIT", "Method", "approved")
        with self.assertRaises(ValueError):
            c.validate()
    def test_reject_unreviewed_license(self):
        c = Capability("Test", "Task", "https://example.com", "Proprietary", "Method")
        with self.assertRaises(ValueError):
            c.validate()

if __name__ == "__main__":
    unittest.main()
