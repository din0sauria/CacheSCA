import os
import subprocess
import shutil

class ConfigService:
    _config = {
        'cipher': 'AES',
        'target': 'original',
        'aim': 'original'
    }
    
    def __init__(self):
        self.config = ConfigService._config
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.payload_dir = os.path.join(self.base_dir, 'payload')
        self.evaluation_dir = os.path.join(self.base_dir, 'evaluation')
        self.hitls_dir = os.path.join(self.base_dir, 'hitls')

    def get_targets(self, cipher):
        if cipher == 'AES':
            return ['original', 'preload', 'constant_time', 'lut_p', 'custom']
        elif cipher == 'SM4':
            return ['original', 'preload', 'lut_p', 'custom']
        return []

    def set_config(self, data):
        cipher = data.get('cipher', 'AES')
        target = data.get('target', 'original')
        
        if cipher not in ['AES', 'SM4']:
            return {'success': False, 'message': 'Unsupported cipher'}
        
        targets = self.get_targets(cipher)
        if target not in targets:
            return {'success': False, 'message': 'Invalid target'}
        
        if cipher == 'SM4' and target == 'constant_time':
            target = 'original'
        
        self.config['cipher'] = cipher
        self.config['target'] = target
        self.config['aim'] = 'original' if target == 'original' else f'{cipher.lower()}_{target}'
        
        print(f'\n[Config] 配置已更新:')
        print(f'  - 加密算法: {cipher}')
        print(f'  - 测试目标: {target}')
        print(f'  - 目标标识: {self.config["aim"]}')
        
        return {'success': True, 'config': self.config}

    def get_config(self):
        return self.config

    def upload_custom_library(self, file_path):
        try:
            custom_dir = os.path.join(self.hitls_dir, 'custom')
            os.makedirs(custom_dir, exist_ok=True)
            dest_path = os.path.join(custom_dir, 'libhitls_crypto.so')
            shutil.copy(file_path, dest_path)
            return {'success': True, 'message': 'Custom library uploaded successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Failed to upload library: {str(e)}'}

    def run_command(self, command, cwd, shell=False):
        try:
            if shell:
                cmd_str = ' '.join(command) if isinstance(command, list) else command
                result = subprocess.run(cmd_str, cwd=cwd, stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, text=True, check=True, shell=True)
            else:
                result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, text=True, check=True)
            return True, result.stdout + '\n' + result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout + '\n' + e.stderr if e.stdout else str(e)
        except Exception as e:
            return False, str(e)
