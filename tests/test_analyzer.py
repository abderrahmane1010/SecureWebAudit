import unittest
from secure_web_audit.analyzer import analyze_packets

class TestAnalyzer(unittest.TestCase):
    def test_analyze_packets(self):
        # Appeler analyze_packets
        packets = analyze_packets()
        # Vérifier si le résultat est une liste (pour simplifier)
        self.assertIsInstance(packets, list)

if __name__ == '__main__':
    unittest.main()