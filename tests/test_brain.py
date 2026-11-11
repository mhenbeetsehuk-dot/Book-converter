import unittest
from brain import plan, blender_script

class BrainTests(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            plan(" ")
    def test_plan(self):
        result = plan("A scene happens.\n\nAnother scene happens.")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "S001")
    def test_blender(self):
        self.assertIn("bpy.ops.render.render", blender_script(plan("Hello world")[0]))

if __name__ == "__main__":
    unittest.main()
