import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health():
    response = requests.get(f'{BASE_URL}/health')
    print('Health Check:', response.json())

def test_config():
    response = requests.get(f'{BASE_URL}/config/targets', params={'cipher': 'AES'})
    print('AES Targets:', response.json())
    
    response = requests.post(f'{BASE_URL}/config/set-config', json={'cipher': 'AES', 'target': 'original'})
    print('Set Config:', response.json())

if __name__ == '__main__':
    try:
        test_health()
        test_config()
        print('\nAll tests passed!')
    except Exception as e:
        print(f'Test failed: {e}')
