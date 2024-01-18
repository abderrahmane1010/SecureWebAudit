
import unittest
from secure_web_audit.detector import detect_anomalies

class TestDetector(unittest.TestCase):
    def test_detect_anomalies(self):
        test_packets = ['normal_packet', 'suspicious_packet', 'normal_packet']
        result = detect_anomalies(test_packets)
        # Vérifier si le résultat est comme attendu
        self.assertIn('suspicious_packet', result)
        self.assertNotIn('normal_packet', result)

if __name__ == '__main__':
    unittest.main()