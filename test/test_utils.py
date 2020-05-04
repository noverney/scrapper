import unittest
import sys
sys.path.append("..") # Adds higher directory to python modules path.
# I would need to hard code the path 
from utils.parse_page import get_download_links

test_url = "https://link.springer.com/book/10.1007%2F978-3-319-13072-9"

class TestUtils(unittest.TestCase):
    def test_get_downlink_links(self):
        outputs = get_download_links(test_url, ["pdf", "epub"])
        self.assertEqual(outputs[0], "https://link.springer.com/content/pdf/10.1007%2F978-3-319-13072-9.pdf")
        self.assertEqual(outputs[1], 'https://link.springer.com/download/epub/10.1007%2F978-3-319-13072-9.epub')

if __name__ == '__main__':
    unittest.main()