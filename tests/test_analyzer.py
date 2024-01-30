import unittest
from secure_web_audit.analyzer import analyze_packets
from secure_web_audit.webpagecontent_analyzer import WebPageContent

class TestAnalyzer(unittest.TestCase):
    def get_comments(self):
        # Appeler analyze_packets
        packets = analyze_packets()
        # Vérifier si le résultat est une liste (pour simplifier)
        self.assertIsInstance(packets, list)

if __name__ == '__main__':
    unittest.main()