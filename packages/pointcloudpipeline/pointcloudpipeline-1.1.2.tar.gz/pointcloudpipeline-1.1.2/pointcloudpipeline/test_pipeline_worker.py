from pipeline_worker import convert_to_laz, convert_from_laz, convert_laz_to_ept_laz, convert_laz_to_2d
import unittest
import shutil
import os


class TestWorker(unittest.TestCase):
    def test_view(self):
        self.assertEqual(convert_laz_to_ept_laz("la.laz", "le", "la/untwine"), "la.laz does not exist.",
                         "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertEqual(b'',
                         convert_laz_to_ept_laz("./test_data/from/test.laz", "./test_data/to", "./untwine/build/untwine"))
        self.assertTrue(os.path.exists("./test_data/to/test"))
        shutil.rmtree("./test_data/to/test")

    def test_convert_laz_to_laz(self):
        self.assertEqual(convert_to_laz("la.laz", "le"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convert_to_laz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convert_e57_to_laz(self):
        self.assertEqual(convert_to_laz("la.e57", "le"), "la.e57 does not exist.", "Should be la.e57 does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convert_to_laz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convert_ply_to_laz(self):
        self.assertEqual(convert_to_laz("la.ply", "le"), "la.ply does not exist.", "Should be la.ply does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convert_to_laz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convert_las_to_laz(self):
        self.assertEqual(convert_to_laz("la.las", "le"), "la.las does not exist.", "Should be la.las does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convert_to_laz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_generate_laz_from_laz(self):
        self.assertEqual(convert_from_laz("la.laz", "le", "laz"), "la.laz does not exist.",
                         "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convert_from_laz("./test_data/from/test.laz", "./test_data/to", "laz"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_generate_e57_from_laz(self):
        self.assertEqual(convert_from_laz("la.laz", "le", "e57"), "la.laz does not exist.",
                         "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.e57"))
        self.assertTrue("metadata" in convert_from_laz("./test_data/from/test.laz", "./test_data/to", "e57"))
        self.assertTrue(os.path.exists("./test_data/to/test.e57"))
        os.remove("./test_data/to/test.e57")

    def test_generate_ply_from_laz(self):
        self.assertEqual(convert_from_laz("la.laz", "le", "ply"), "la.laz does not exist.",
                         "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.ply"))
        self.assertTrue("metadata" in convert_from_laz("./test_data/from/test.laz", "./test_data/to", "ply"))
        self.assertTrue(os.path.exists("./test_data/to/test.ply"))
        os.remove("./test_data/to/test.ply")

    def test_generate_las_from_laz(self):
        self.assertEqual(convert_from_laz("la.laz", "le", "las"), "la.laz does not exist.",
                         "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.las"))
        self.assertTrue("metadata" in convert_from_laz("./test_data/from/test.laz", "./test_data/to", "las"))
        self.assertTrue(os.path.exists("./test_data/to/test.las"))
        os.remove("./test_data/to/test.las")

    def test_get_2d(self):
        self.assertEqual(convert_laz_to_2d("la.laz", "le"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.tif"))
        self.assertTrue("metadata" in convert_laz_to_2d("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.tif"))
        os.remove("./test_data/to/test.tif")


if __name__ == '__main__':
    unittest.main()
