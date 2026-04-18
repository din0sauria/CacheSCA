import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.config_service import ConfigService

class EvaluationService:
    def __init__(self):
        self.config_service = ConfigService()
        self.evaluation_dir = self.config_service.evaluation_dir
        self.raw_data = None
        self.valid_rows = []
        self.skey = b''
        self.original_skey = b''
        self.cache_set_idx = []

    def run_evaluation(self, data):
        config = self.config_service.get_config()
        skey_str = data.get('skey', '')
        samples = data.get('samples', 1000)
        fout = data.get('output', 'result')
        
        if not self._is_key_valid(skey_str):
            return {'success': False, 'message': 'Invalid secret key format'}
        
        if not skey_str:
            skey_str = '0b7e151628aed2a6abf7158809cf4f3c'
        
        self.original_skey = bytes.fromhex(skey_str.lower())
        
        cipher_lower = config['cipher'].lower()
        aim = config['aim']
        
        cmd = f'make run-{cipher_lower}-{aim} ARGS="-k {skey_str.lower()} -s {samples}" > {fout}'
        
        print(f'\n{"="*60}')
        print(f'[Evaluation] 执行安全性评估')
        print(f'  - 加密算法: {config["cipher"]}')
        print(f'  - 测试目标: {config["target"]}')
        print(f'  - 目标标识: {aim}')
        print(f'  - 密钥: {skey_str}')
        print(f'  - 采样组数: {samples}')
        print(f'  - 工作目录: {self.evaluation_dir}')
        print(f'  - 执行命令: {cmd}')
        print(f'{"="*60}\n')
        
        success, output = self.config_service.run_command(cmd, self.evaluation_dir, shell=True)
        if not success:
            return {'success': False, 'message': f'Evaluation failed: {output}'}
        
        return {'success': True, 'output_file': fout}

    def analyze_result(self, filepath):
        full_path = os.path.join(self.evaluation_dir, filepath)
        
        try:
            self.raw_data = np.zeros((16, 256, 64), dtype=int)
            self.valid_rows = []
            
            with open(full_path, 'r') as f:
                for line in f:
                    parts = line.strip().split(': ')
                    if len(parts) != 2:
                        continue
                    
                    idx, pt = parts[0].split()
                    idx = int(idx)
                    pt = int(pt, 16)
                    
                    values = list(map(int, parts[1].split()))
                    self.raw_data[idx, pt] = np.array(values)
                    
                    if idx == 0:
                        self.valid_rows.append(pt)
            
            self.skey = b''
            self.cache_set_idx = [None] * 16
            for i in range(16):
                keybyte, _, set_idx, _ = self._analyze(self.raw_data[i], self.valid_rows)
                self.skey += keybyte.to_bytes(1, 'big')
                self.cache_set_idx[i] = set_idx
            
            skey_hex = self.skey.hex()
            pages = 16 if self.config_service.config['cipher'] == 'AES' else 4
            
            correct_bytes = 0
            correct_high_nibbles = 0
            if self.original_skey:
                for i in range(len(self.skey)):
                    if self.skey[i] == self.original_skey[i]:
                        correct_bytes += 1
                    if (self.skey[i] & 0xF0) == (self.original_skey[i] & 0xF0):
                        correct_high_nibbles += 1
            
            return {
                'success': True, 
                'skey': skey_hex, 
                'pages': pages,
                'original_skey': self.original_skey.hex(),
                'correct_bytes': correct_bytes,
                'correct_high_nibbles': correct_high_nibbles,
                'total_bytes': len(self.skey)
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Analysis failed: {str(e)}'}

    def get_heatmap(self, data):
        idx = data.get('index', 0)
        
        if self.raw_data is None:
            return {'success': False, 'message': 'No data available'}
        
        try:
            heatmap_data = self.raw_data[idx, self.valid_rows].tolist()
            rows = [f'0x{r:02X}' for r in self.valid_rows]
            set_idx = self.cache_set_idx[idx]
            
            annotations = []
            for i, pt in enumerate(self.valid_rows):
                row_ann = []
                for j in range(64):
                    if set_idx is not None and j == set_idx[pt]:
                        row_ann.append('*')
                    else:
                        row_ann.append('')
                annotations.append(row_ann)
            
            return {
                'success': True,
                'data': heatmap_data,
                'rows': rows,
                'annotations': annotations,
                'columns': list(range(64))
            }
        except Exception as e:
            return {'success': False, 'message': f'Failed to generate heatmap: {str(e)}'}

    def _analyze(self, data, rows):
        maxn = -np.inf
        keybyte = -1
        offset = -1
        
        for guess in range(16):
            for off in range(64):
                sum_val = 0
                for pt in rows:
                    set_idx = (off + ((pt >> 4) ^ guess)) % 64
                    sum_val += data[pt, set_idx]
                
                if sum_val > maxn:
                    maxn = sum_val
                    keybyte = guess
                    offset = off
        
        set_idx = np.zeros(256, dtype=int)
        for pt in rows:
            set_idx[pt] = (offset + ((pt >> 4) ^ keybyte)) % 64
        
        return keybyte << 4, offset, set_idx, maxn

    def _is_key_valid(self, skey_str):
        if len(skey_str) == 0:
            return True
        try:
            skey_bytes = bytes.fromhex(skey_str)
            return len(skey_bytes) == 16
        except:
            return False
