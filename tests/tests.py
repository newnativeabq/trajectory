import unittest

class Test_Yet_to_be_named(unittest.TestCase):

    def test_one_of_some_number(self):
        self.assertEqual(sum([1,2,10,4,5]), 15, "should be 15")

def run_and_check_tests():
    return True

if __name__ == "__main__":
    unittest.main()
