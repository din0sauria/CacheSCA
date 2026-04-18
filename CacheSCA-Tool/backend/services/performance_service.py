import os
import sys
import subprocess
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.config_service import ConfigService

class PerformanceService:
    def __init__(self):
        self.config_service = ConfigService()
        self.payload_dir = self.config_service.payload_dir
        self.levels = ['low', 'medium', 'high', 'extreme']

    def run_test(self, data):
        config = self.config_service.get_config()
        datafile = data.get('datafile', 'data')
        
        print(f'\n{"="*60}')
        print(f'[Performance] 执行性能测试')
        print(f'  - 加密算法: {config["cipher"]}')
        print(f'  - 测试目标: {config["target"]}')
        print(f'  - 目标标识: {config["aim"]}')
        print(f'  - 数据文件: {datafile}')
        print(f'  - 工作目录: {self.payload_dir}')
        print(f'{"="*60}')
        
        results = {}
        for level in self.levels:
            cmd = ['python', 'payload.py', config['aim'], config['cipher'], datafile, level]
            
            print(f'\n[Performance] 测试负载级别: {level}')
            print(f'  - 执行命令: {" ".join(cmd)}')
            
            success, output = self.config_service.run_command(cmd, self.payload_dir)
            
            if not success:
                print(f'  - 结果: 失败')
                return {'success': False, 'message': f'Test failed for {level}: {output}'}
            
            try:
                cycles = int(output.strip().split('\n')[-1])
                results[level] = cycles
                print(f'  - CPU周期: {cycles}')
            except (ValueError, IndexError):
                results[level] = 0
                print(f'  - 结果: 解析失败')
        
        print(f'\n{"="*60}')
        print(f'[Performance] 测试完成')
        print(f'  - 结果: {results}')
        print(f'{"="*60}\n')
        
        return {'success': True, 'results': results}

    def compare_results(self, files):
        comparison_data = {}
        
        for filepath in files:
            try:
                with open(filepath, 'r') as f:
                    data = f.readlines()[0].strip().split(' ')
                    values = list(map(int, data))
                    filename = os.path.basename(filepath).split('.')[0]
                    comparison_data[filename] = values
            except Exception as e:
                return {'success': False, 'message': f'Failed to read {filepath}: {str(e)}'}
        
        return {'success': True, 'comparison_data': comparison_data}

    def save_result(self, data):
        results = data.get('results', {})
        filepath = data.get('filepath', 'performance_result.txt')
        
        try:
            with open(filepath, 'w') as f:
                f.write(' '.join(map(str, [results.get(level, 0) for level in self.levels])))
            return {'success': True, 'filepath': filepath}
        except Exception as e:
            return {'success': False, 'message': f'Failed to save: {str(e)}'}
