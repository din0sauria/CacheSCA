export const mockEvaluationData = {
  skey: '909040301040f0c040a0c0b000e0c020',
  pages: 16,
  validRows: [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
    0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F
  ],
  generateHeatmapData: (byteIndex) => {
    const rows = mockEvaluationData.validRows.length
    const cols = 64
    const data = []
    
    const keyByte = parseInt(mockEvaluationData.skey.substr(byteIndex * 2, 2), 16)
    const baseOffset = (byteIndex * 4) % 64
    
    for (let i = 0; i < rows; i++) {
      const row = []
      const pt = mockEvaluationData.validRows[i]
      
      for (let j = 0; j < cols; j++) {
        const targetSet = (baseOffset + ((pt >> 4) ^ keyByte)) % 64
        
        if (j === targetSet) {
          row.push(800 + Math.floor(Math.random() * 200))
        } else if (Math.abs(j - targetSet) <= 2 || Math.abs(j - targetSet) >= 62) {
          row.push(200 + Math.floor(Math.random() * 150))
        } else {
          row.push(50 + Math.floor(Math.random() * 100))
        }
      }
      data.push(row)
    }
    
    return data
  },
  getHeatmap: (byteIndex) => {
    const data = mockEvaluationData.generateHeatmapData(byteIndex)
    const rows = mockEvaluationData.validRows.map(r => `0x${r.toString(16).padStart(2, '0').toUpperCase()}`)
    
    const keyByte = parseInt(mockEvaluationData.skey.substr(byteIndex * 2, 2), 16)
    const baseOffset = (byteIndex * 4) % 64
    
    const annotations = []
    for (let i = 0; i < rows.length; i++) {
      const pt = mockEvaluationData.validRows[i]
      const targetSet = (baseOffset + ((pt >> 4) ^ keyByte)) % 64
      const rowAnn = []
      for (let j = 0; j < 64; j++) {
        rowAnn.push(j === targetSet ? '*' : '')
      }
      annotations.push(rowAnn)
    }
    
    return {
      success: true,
      data: data,
      rows: rows,
      annotations: annotations,
      columns: Array.from({ length: 64 }, (_, i) => i)
    }
  }
}

export const mockPerformanceData = {
  baseResults: {
    original: { low: 645, medium: 812, high: 1247, extreme: 1893 },
    preload: { low: 520, medium: 680, high: 1050, extreme: 1620 },
    constant_time: { low: 780, medium: 950, high: 1420, extreme: 2150 },
    lut_p: { low: 590, medium: 750, high: 1180, extreme: 1780 },
    'aes_original': { low: 645, medium: 812, high: 1247, extreme: 1893 },
    'aes_preload': { low: 520, medium: 680, high: 1050, extreme: 1620 },
    'aes_constant_time': { low: 780, medium: 950, high: 1420, extreme: 2150 },
    'aes_lut_p': { low: 590, medium: 750, high: 1180, extreme: 1780 },
    'sm4_original': { low: 720, medium: 890, high: 1350, extreme: 2050 },
    'sm4_preload': { low: 580, medium: 740, high: 1120, extreme: 1720 },
    'sm4_lut_p': { low: 650, medium: 820, high: 1250, extreme: 1900 }
  },
  
  getMockResults: (aim = 'original') => {
    const base = mockPerformanceData.baseResults[aim] || mockPerformanceData.baseResults['original']
    const randomFactor = () => Math.floor(Math.random() * 100) - 50
    return {
      low: base.low + randomFactor(),
      medium: base.medium + randomFactor(),
      high: base.high + randomFactor(),
      extreme: base.extreme + randomFactor()
    }
  },
  
  generateComparisonData: (aim = 'original') => {
    const randomFactor = () => Math.floor(Math.random() * 80) - 40
    return {
      labels: ['原始实现', '预加载表', '常量时间', '并行拆分表'],
      encryption: [
        645 + randomFactor(),
        520 + randomFactor(),
        780 + randomFactor(),
        590 + randomFactor()
      ],
      decryption: [
        1044 + randomFactor(),
        850 + randomFactor(),
        1200 + randomFactor(),
        920 + randomFactor()
      ],
      keyExpansion: [
        128 + randomFactor(),
        128 + randomFactor(),
        128 + randomFactor(),
        145 + randomFactor()
      ]
    }
  }
}

export const mockConfigData = {
  cipher: 'AES',
  aim: 'original',
  data: 'built-in',
  level: 'low'
}
