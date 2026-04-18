# CacheSCA-Tool

Cache 侧信道攻击分析与测试工具，用于评估 openHiTLS 中 AES 与 SM4 算法的性能及对 Cache 侧信道攻击的脆弱性。

## 功能特性

- **性能测试**: 在不同系统负载下测试加密性能
- **安全评估**: Cache 侧信道攻击模拟与密钥恢复分析
- **可视化**: 16张热力图展示 Cache 访问模式
- **Mock 数据**: 后端失败时自动切换模拟数据展示

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite 5 + Element Plus + ECharts + Pinia |
| 后端 | Flask 3.0 + NumPy + Pandas |
| 桌面端 | PyQt5 (可选) |

## 项目结构

```
CacheSCA-Tool/
├── backend/                 # Flask 后端 API
│   ├── routes/             # API 路由
│   ├── services/           # 业务逻辑
│   └── app.py              # 应用入口
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── mock/          # Mock 数据
│   │   ├── stores/        # 状态管理
│   │   └── views/         # 页面组件
│   └── vite.config.js
├── gui/                    # PyQt5 桌面端 (可选)
├── evaluation/             # 评估核心代码
├── payload/                # 攻击载荷
│   ├── aes/               # AES 相关
│   └── sm4/               # SM4 相关
└── hitls/                  # openHiTLS 库
```

## 快速开始

### 环境要求

- **Python 3.8+**
- **Node.js 16+**
- **WSL/Linux** (用于编译和运行评估程序)

### 安装与运行

1. **克隆仓库**
   ```bash
   cd CacheSCA-Tool
   ```

2. **启动后端服务**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

3. **启动前端服务**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   或
   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```
4. **访问应用**
   - 前端界面: http://localhost:5173
   - 后端 API: http://localhost:5000

## 使用说明

### 主页配置

1. 选择加密算法 (AES / SM4)
2. 选择测试目标:
   - `original` - 原始实现
   - `preload` - 预加载表
   - `constant_time` - 常量时间
   - `lut_p` - 查找表保护
   - `custom` - 自定义库

### 性能测试

- 选择测试数据类型 (内置/自定义)
- 设置采样组数
- 点击运行测试，查看不同负载下的性能对比

### 安全评估

- 输入测试密钥或随机生成
- 设置采样数量
- 运行评估后查看16字节热力图分析

## API 文档

### 配置
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/config/targets` | 获取可用测试目标 |
| POST | `/api/config/set-config` | 设置当前配置 |

### 性能测试
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/performance/test` | 运行性能测试 |
| POST | `/api/performance/save` | 保存测试结果 |

### 安全评估
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/evaluation/test` | 运行安全评估 |
| POST | `/api/evaluation/heatmap` | 获取热力图数据 |

## 开发

```bash
# 前端开发
cd frontend
npm run dev      # 开发模式
npm run build    # 生产构建

# 后端开发
cd backend
python app.py    # 开发模式（热重载）
```

## 许可证

MIT License
