# CacheSCA 总项目

我们实现了：

- **缓解**对称加密算法面对 Cache 类测信道攻击的脆弱性的新方案
- **评估**对称加密算法面对 Cache 类测信道攻击的脆弱性的新方案
- openHiTLS 中 AES 与 SM4 多种方案加固实现
- **CacheSCA-Tool**：一个用于测试与评估 openHiTLS 中 AES 与 SM4 性能与对 Cache 类测信道攻击脆弱性的通用平台
- Mastik 安全评估工具的改进

## 环境准备

### 系统要求

- **操作系统**: Linux (推荐 Ubuntu 20.04+)(支持WSL)
- **编译工具**: gcc, make, cmake
- **运行环境**: Python 3.8+, Node.js 16+ (Web GUI)
- **测试工具**: cpulimit, stress-ng

## 项目结构

```
CacheSCA-Tool/              # 测试平台
├── hitls/                    # HiTLS 加密库编译文件
├── payload/                  # 性能测试模块
├── evaluation/               # 安全评估模块
├── backend/                  # Web 后端 (Flask)
├── frontend/                 # Web 前端 (Vue 3)
└── gui/                      # PyQt GUI
Mastik    # 微体系结构侧信道攻击工具包
openhitls # 开源密码套件
```
## 依赖安装

#### 1. 安装 Mastik （微体系结构侧信道攻击工具包）

```bash
cd Mastik
./configure
make
sudo make install
```
#### 2. 编译 openHiTLS 库（开源密码套件）

**重要**: 项目 `hitls/` 目录中预置的库可能存在兼容性问题，建议重新编译。

```bash
# 克隆 openHiTLS 仓库（随子模块一起克隆，一步准备所有源码和依赖）
git clone --recurse-submodules https://gitcode.com/openhitls/openhitls.git
cd openhitls

# 编译安装
mkdir -p build && cd build
cmake .. && make -j$(nproc) && make install

# 查看生成的库文件
ls -la *.so
# 应该看到: libhitls_crypto.so, libhitls_bsl.so 等
```

#### 3. 部署库文件到项目目录

```bash
# 设置项目路径
PROJECT_DIR=/path/to/CacheSCA-Tool
OPENHITLS_BUILD=/path/to/openhitls/build

# 复制库文件到所有 hitls 子目录
for dir in original aes_lut_p aes_preload aes_constant_time sm4_lut_p sm4_preload; do
    mkdir -p $PROJECT_DIR/hitls/$dir
    cp $OPENHITLS_BUILD/libhitls_crypto.so $PROJECT_DIR/hitls/$dir/
    cp $OPENHITLS_BUILD/libhitls_bsl.so $PROJECT_DIR/hitls/$dir/
    echo "已更新: $dir"
done

# 验证库文件
ldd -r $PROJECT_DIR/hitls/original/libhitls_crypto.so
# 确保没有 "undefined symbol" 错误
```

#### 4. 验证环境

```bash
# 检查所有依赖库
ldconfig -p | grep -E "boundscheck|hitls"

# 测试编译
cd $PROJECT_DIR/payload/aes
make clean
make run-aes_lut_p data 0 0
```

## Web GUI 使用

### 环境要求

- Linux(支持WSL)
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 启动服务

#### 方式一：分别启动

```bash
# 终端1 - 启动后端
cd CacheSCA-Tool/backend
pip install -r requirements.txt
python app.py

# 终端2 - 启动前端
cd CacheSCA-Tool/frontend
npm install
npm run dev
```

#### 方式二：一键启动

```bash
cd CacheSCA-Tool
# Windows
start-backend.bat & start-frontend.bat

# Linux/Mac
./start-backend.sh & ./start-frontend.sh
```

### 访问地址

- 前端界面: http://localhost:3000
- 后端 API: http://localhost:5000
- API 健康检查: http://localhost:5000/api/health

### 功能模块

#### 1. 主页配置
- 选择加密算法 (AES / SM4)
- 选择测试目标 (original / preload / constant_time / lut_p / custom)
- 支持自定义测试库上传

#### 2. 性能测试
- 不同系统负载下的加密性能测试
- 实时性能对比图表
- 测试结果保存与加载
- 多组结果对比分析

#### 3. 安全评估
- Cache 侧信道攻击模拟
- 密钥恢复分析（恢复密钥高4位）
- 热力图可视化
- 颜色标注正确性：
  - 🟢 绿色: 高4位正确
  - 🔴 红色: 错误


## 命令行界面 (CLI) 使用

### 正确性测试

```bash
cd CacheSCA-Tool/payload/aes

# 测试 aes_lut_p 目标
make run-aes_lut_p data 10000 0

# 测试自定义目标
# 将 libhitls_crypto.so 放入 hitls/custom/ 后执行
make run-custom data 10000 0

# 重新生成测试数据
python generate.py 10000 data
```

**参数说明**:
- `target`: 测试对象 (original/aes_lut_p/aes_preload/aes_constant_time/custom)
- `datafile`: 测试数据文件
- `nsamples`: 测试数据组数
- `mode`: 测试模式 (0=正确性测试)

### 性能测试

```bash
cd CacheSCA-Tool/payload

# 执行性能测试
python payload.py aes_lut_p aes data low

# 参数说明:
# - aim: 测试目标
# - cipher: 加密算法 (aes/sm4)
# - datafile: 测试数据文件
# - level: 系统负载 (low/medium/high/extreme)
```

### 安全评估

```bash
cd CacheSCA-Tool/evaluation

# 执行评估测试
make run-aes-aes_lut_p ARGS="-k 0b7e151628aed2a6abf7158809cf4f3c -s 10000" > results

# 参数说明:
# - cipher: 加密算法 (aes/sm4)
# - target: 测试目标
# - -k: 测试密钥 (32位十六进制)
# - -s: 采样组数

# 分析结果
python analyze.py results
```


## 常见问题

### 1. 编译错误: 找不到 -lboundscheck

**原因**: 未安装 libboundscheck 库

**解决**:
```bash
git clone https://gitee.com/openeuler/libboundscheck.git
cd libboundscheck
make
sudo cp lib/libboundscheck.so /usr/local/lib/
sudo ldconfig
```

### 2. 运行错误: undefined symbol: BSL_HASH_Destory

**原因**: `hitls/` 目录中的预置库与系统库不兼容

**解决**: 重新编译 openHiTLS 并替换库文件（见上文"编译 openHiTLS 库"）

### 3. 编译错误: undefined reference to `BSL_HASH_Destory`

**原因**: 缺少 libhitls_bsl.so 链接

**解决**: 
1. 确保 `hitls/original/` 目录中有 `libhitls_bsl.so`
2. 修改 `payload/aes/makefile`，添加 `-lhitls_bsl`:
   ```makefile
   main: main.c
       $(CC) -o $@ $< -L$(HITLS_DIR)/original/ -lhitls_crypto -lhitls_bsl $(CFLAGS)
   ```

### 4. 运行错误: symbol lookup error

**原因**: 运行时找不到动态库

**解决**:
```bash
# 设置 LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/path/to/CacheSCA-Tool/hitls/original:$LD_LIBRARY_PATH

# 或复制库到系统目录
sudo cp /path/to/CacheSCA-Tool/hitls/original/*.so /usr/local/lib/
sudo ldconfig
```

### 5. Web GUI 无法连接后端

**检查**:
1. 后端是否启动: 访问 http://localhost:5000/api/health
2. 端口是否被占用: `lsof -i :5000`
3. 防火墙设置

## 项目结构

```
CacheSCA-Tool/
├── hitls/                    # HiTLS 加密库
│   ├── original/            # 原始版本
│   ├── aes_lut_p/           # AES LUT-P 加固版本
│   ├── aes_preload/         # AES 预加载版本
│   ├── aes_constant_time/   # AES 常量时间版本
│   ├── sm4_lut_p/           # SM4 LUT-P 加固版本
│   ├── sm4_preload/         # SM4 预加载版本
│   └── custom/              # 自定义版本
│
├── payload/                  # 性能测试模块
│   ├── aes/                 # AES 测试
│   ├── sm4/                 # SM4 测试
│   └── payload.py           # 性能测试脚本
│
├── evaluation/               # 安全评估模块
│   ├── main.c               # 评估主程序
│   ├── analyze.py           # 结果分析脚本
│   └── makefile             # 编译配置
│
├── backend/                  # Web 后端 (Flask)
│   ├── routes/              # API 路由
│   ├── services/            # 业务逻辑
│   └── app.py               # 应用入口
│
├── frontend/                 # Web 前端 (Vue 3)
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # 状态管理
│   │   └── api/             # API 接口
│   └── package.json
│
└── gui/                      # PyQt GUI (旧版)
```

## openHiTLS 加固代码

不同加固实现在原仓库的不同分支中：

| 分支 | 说明 |
|------|------|
| `aes-constant-time` | 传统常量时间加固方案 |
| `aes-preload` | 传统预加载表加固方案 |
| `aes-lut-p` | 并行拆分查找表加固方案（推荐）|
| `sm4-preload` | SM4 预加载方案 |
| `sm4-lut-p` | SM4 并行拆分查找表方案 |

## 密钥恢复说明

本工具的 Cache 侧信道攻击可以恢复密钥的**高4位**：

- 攻击原理：通过 Cache 访问模式推断密钥字节的高4位
- 恢复结果：每个字节恢复值为 `keybyte << 4`（低4位为0）
- 评估指标：高4位正确率

## 参考资料

- [openHiTLS 仓库](https://gitee.com/openhitls/openhitls)
- [libboundscheck 仓库](https://gitee.com/openeuler/libboundscheck)
- [Mastik 工具](https://github.com/0xADE1A1DE/Mastik)
