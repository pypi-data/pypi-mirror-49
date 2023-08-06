import os
import unittest

from pymongoimport.filesplitter import LineCounter
from pymongoimport.liner import make_line_file


class MyTestCase(unittest.TestCase):

    def _test_file(self, count, doseol=False,filename="liner.txt", unlink=False):
        f = make_line_file(count=count, doseol=doseol, filename=filename)
        self.assertEqual(count, LineCounter(f).line_count)
        if unlink:
            os.unlink(f)

    def test_Line_Counter(self):
        self._test_file(1, filename="1.txt")
        self._test_file(2, filename="2.txt")
        self._test_file(512, filename="3.txt")
        self._test_file(65000, filename="5.txt")
        self._test_file(1, doseol=True, filename="6.txt")
        self._test_file(10, filename="7.txt", doseol=True)
        self._test_file(65000, filename="8.txt",doseol=True)


if __name__ == '__main__':
    unittest.main()
