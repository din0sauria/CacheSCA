# Mock 数据说明文档

本文档说明 `data.js` 中各数据的含义及修改方法。

---

## 1. mockEvaluationData - 安全评估 Mock 数据

### 1.1 skey - 恢复的密钥

```javascript
skey: '909040301040f0c040a0c0b000e0c020'
```

**含义**: 侧信道攻击恢复的密钥结果（16字节，32个十六进制字符）

**特点**: 
- 每个字节的**低4位为0**，因为侧信道攻击只能稳定恢复高4位
- 例如: `0x9c` → `0x90`（高4位`9`保留，低4位`c`置0）

**修改方法**:
```javascript
// 完整密钥示例
skey: '0b7e151628aed2a6abf7158809cf4f3c'

// 部分恢复示例（低位为0）
skey: '0b001500280000a60015000009000000'
```

### 1.2 pages - 热力图页数

```javascript
pages: 16
```

**含义**: 热力图页数，对应密钥字节数
- AES-128: 16字节 → 16页
- SM4: 16字节 → 16页（可改为4页展示部分结果）

**修改方法**:
```javascript
pages: 4  // 只展示前4个字节
```

### 1.3 validRows - 有效明文字节值

```javascript
validRows: [0x00, 0x01, 0x02, ..., 0x3F]
```

**含义**: 热力图Y轴显示的明文字节值（十六进制）

**修改方法**:
```javascript
// 显示更多行
validRows: [0x00, 0x01, 0x02, ..., 0x7F]  // 0-127

// 显示更少行
validRows: [0x00, 0x10, 0x20, 0x30]  // 只显示4行
```

### 1.4 generateHeatmapData - 热力图数据生成

**含义**: 根据密钥字节生成模拟的Cache访问热力图数据

**数据分布**:
| 位置 | 数值范围 | 含义 |
|------|----------|------|
| 目标Cache Set | 800-1000 | 高亮区域（攻击命中） |
| 相邻Set | 200-350 | 次高区域 |
| 其他Set | 50-150 | 背景噪声 |

**修改热力图亮度**:
```javascript
// 在 generateHeatmapData 函数中修改
if (j === targetSet) {
  row.push(1000 + Math.floor(Math.random() * 200))  // 更亮
} else {
  row.push(30 + Math.floor(Math.random() * 50))     // 更暗
}
```

---

## 2. mockPerformanceData - 性能测试 Mock 数据

### 2.1 baseResults - 基准性能数据

```javascript
baseResults: {
  original: { low: 645, medium: 812, high: 1247, extreme: 1893 },
  preload: { low: 520, medium: 680, high: 1050, extreme: 1620 },
  // ...
}
```

**含义**: 不同测试目标的CPU周期数

| 负载级别 | 含义 | 模拟场景 |
|----------|------|----------|
| low | 低负载 | 系统空闲 |
| medium | 中等负载 | 正常使用 |
| high | 高负载 | CPU密集任务 |
| extreme | 极限负载 | 压力测试 |

**目标标识说明**:
| 标识 | 含义 |
|------|------|
| `original` | 原始实现（基准） |
| `preload` | 预加载表方案 |
| `constant_time` | 常量时间方案 |
| `lut_p` | 并行拆分查找表方案 |
| `aes_original` | AES原始实现 |
| `sm4_preload` | SM4预加载方案 |

**修改方法**:
```javascript
baseResults: {
  original: { low: 700, medium: 900, high: 1400, extreme: 2100 },
  // 修改数值为实际测试结果
}
```

### 2.2 getMockResults - 获取Mock结果

**含义**: 根据当前目标返回性能数据，自动添加 ±50 的随机波动

**修改随机范围**:
```javascript
getMockResults: (aim = 'original') => {
  const base = mockPerformanceData.baseResults[aim] || mockPerformanceData.baseResults['original']
  const randomFactor = () => Math.floor(Math.random() * 200) - 100  // 改为 ±100
  return {
    low: base.low + randomFactor(),
    // ...
  }
}
```

### 2.3 generateComparisonData - 对比数据

**含义**: 生成多种实现的对比数据

**修改方法**:
```javascript
generateComparisonData: (aim = 'original') => {
  return {
    labels: ['方案A', '方案B', '方案C', '方案D'],  // 修改标签
    encryption: [645, 520, 780, 590],              // 修改加密时间
    decryption: [1044, 850, 1200, 920],            // 修改解密时间
    keyExpansion: [128, 128, 128, 145]             // 修改密钥扩展时间
  }
}
```

---

## 3. mockConfigData - 配置 Mock 数据

```javascript
export const mockConfigData = {
  cipher: 'AES',      // 加密算法: 'AES' 或 'SM4'
  aim: 'original',    // 目标标识
  data: 'built-in',   // 数据类型: 'built-in' 或 'custom'
  level: 'low'        // 负载级别
}
```

**修改方法**:
```javascript
mockConfigData = {
  cipher: 'SM4',
  aim: 'sm4_preload',
  data: 'custom',
  level: 'high'
}
```

---

## 4. 快速参考

### 常用修改场景

#### 场景1: 修改恢复密钥显示
```javascript
// 找到第2行
skey: '你的密钥值'
```

#### 场景2: 调整性能数据量级
```javascript
// 找到 baseResults，统一乘以系数
original: { low: 645 * 2, medium: 812 * 2, high: 1247 * 2, extreme: 1893 * 2 }
```

#### 场景3: 添加新的测试目标
```javascript
// 在 baseResults 中添加
'my_custom': { low: 500, medium: 700, high: 1100, extreme: 1700 }
```

#### 场景4: 修改热力图行数
```javascript
// 修改 validRows 数组长度
validRows: [0x00, 0x01, ..., 0xFF]  // 256行
```

---

## 5. 注意事项

1. **密钥格式**: 必须是32个十六进制字符（16字节）
2. **性能数值**: 单位为CPU周期数，数值越大表示越慢
3. **随机波动**: 每次调用会生成不同的随机数，刷新页面数据会变化
4. **热力图数据**: 自动根据密钥生成，无需手动修改
