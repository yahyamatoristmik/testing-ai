#!/usr/bin/env python3
import json
import sys

def parse_zap_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    high = medium = low = info = 0
    
    # Method 1: Parse from alerts
    if 'site' in data:
        for site in data['site']:
            for alert in site.get('alerts', []):
                risk = alert.get('risk', 'Informational').lower()
                count = alert.get('count', 1)
                
                if risk == 'high':
                    high += count
                elif risk == 'medium':
                    medium += count
                elif risk == 'low':
                    low += count
                else:
                    info += count
    
    print(f"High: {high}")
    print(f"Medium: {medium}")
    print(f"Low: {low}")
    print(f"Informational: {info}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 parse_zap_json.py <json_file>")
        sys.exit(1)
    
    parse_zap_json(sys.argv[1])
