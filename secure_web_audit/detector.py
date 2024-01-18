from .utils import *

def detect_anomalies(packets):
    suspicious_packets = []
    for packet in packets:
        if is_packet_suspicious(packet):
            print(f"Suspicious packet detected: {packet}")
            suspicious_packets.append(packet)
    return suspicious_packets