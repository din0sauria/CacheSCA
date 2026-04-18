<template>
  <div class="evaluation-page">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><DataAnalysis /></el-icon>
            安全性评估
          </h1>
          <p class="page-subtitle">Cache侧信道攻击模拟与密钥恢复测试</p>
        </div>
        <div class="target-badge">
          <span class="badge-label">当前目标</span>
          <span class="badge-value">{{ configStore.aim }}</span>
        </div>
      </div>
    </div>

    <el-row :gutter="24">
      <el-col :span="24">
        <div class="control-section">
          <div class="section-title">
            <el-icon><Lock /></el-icon>
            <span>评估控制</span>
          </div>
          
          <div class="control-content">
            <div class="control-row">
              <div class="control-item key-control">
                <label class="control-label">密钥 (Hex)</label>
                <div class="key-input-group">
                  <el-input 
                    v-model="secretKey" 
                    placeholder="16字节十六进制密钥 (可选)"
                    clearable
                    size="large"
                    class="key-input"
                  />
                  <div class="key-buttons">
                    <el-button @click="setTestKey" class="test-key-btn">
                      <el-icon><Key /></el-icon>
                      测试样例
                    </el-button>
                    <el-button @click="generateRandomKey" class="random-key-btn">
                      <el-icon><Refresh /></el-icon>
                      随机生成
                    </el-button>
                  </div>
                </div>
              </div>
              
              <div class="control-item samples-control">
                <label class="control-label">采样组数</label>
                <div class="samples-input-group">
                  <div class="samples-row">
                    <div class="quick-select">
                      <el-button 
                        v-for="preset in [10000, 50000, 100000, 500000, 1000000]" 
                        :key="preset"
                        :type="samples === preset ? 'danger' : 'default'"
                        size="small"
                        @click="samples = preset"
                        class="preset-btn"
                      >
                        {{ preset }}
                      </el-button>
                    </div>
                    <el-input 
                      v-model.number="samples" 
                      type="number" 
                      :min="10000" 
                      :max="1000000"
                      size="small"
                      class="samples-input"
                    >
                      <template #suffix>
                        <span class="input-suffix">组</span>
                      </template>
                    </el-input>
                  </div>
                  <div class="slider-group">
                    <el-slider 
                      v-model="samples" 
                      :min="10000" 
                      :max="1000000" 
                      :step="10000"
                      :show-tooltip="true"
                      :format-tooltip="(val) => `${val} 组`"
                      class="samples-slider"
                    />
                  </div>
                </div>
              </div>            
              
              <div class="control-actions">
              <el-button 
                type="danger" 
                size="large"
                @click="startEvaluation"
                :loading="evaluationStore.evaluating"
                class="action-btn danger"
              >
                <el-icon><VideoPlay /></el-icon>
                开始评估
              </el-button>
            </div>
            </div>
            

          </div>
          
          <transition name="slide-fade">
            <div v-if="evaluationStore.skey" class="result-section">
              <div class="result-header">
                <el-icon class="result-icon"><Key /></el-icon>
                <span>恢复密钥</span>
              </div>
              <div class="result-content">
                <div class="skey-bytes" v-if="evaluationStore.skey && evaluationStore.originalSkey">
                  <span 
                    v-for="(byte, index) in getKeyBytes(evaluationStore.skey)" 
                    :key="index"
                    class="skey-byte"
                    :class="getByteClass(index)"
                  >
                    {{ byte.toUpperCase() }}
                  </span>
                </div>
                <span class="skey-value" v-else>{{ formatSkey(evaluationStore.skey) }}</span>
                <el-button size="small" @click="copySkey" class="copy-btn">
                  <el-icon><CopyDocument /></el-icon>
                  复制
                </el-button>
              </div>
              <div class="result-stats" v-if="evaluationStore.originalSkey">
                <div class="stat-item">
                  <span class="stat-label">原始密钥:</span>
                  <span class="stat-value">{{ formatSkey(evaluationStore.originalSkey) }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">高4位正确:</span>
                  <span class="stat-value correct" :class="{ all: evaluationStore.correctHighNibbles === evaluationStore.totalBytes }">
                    {{ evaluationStore.correctHighNibbles }} / {{ evaluationStore.totalBytes }} 字节
                  </span>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px">
      <el-col :span="24">
        <div class="heatmap-section">
          <div class="section-header">
            <div class="section-title">
              <el-icon><DataBoard /></el-icon>
              <span>Cache访问热力图 (点击小图查看详细视图)</span>
            </div>
            <div class="section-actions">
              <el-tag v-if="evaluationStore.useMockData" type="warning" effect="dark">
                <el-icon><Warning /></el-icon>
                Mock数据
              </el-tag>
            </div>
          </div>
          
          <div class="heatmaps-grid">
            <div 
              v-for="byteIndex in 16" 
              :key="byteIndex - 1" 
              class="heatmap-item"
              :class="{ active: selectedByteIndex === byteIndex - 1 }"
              @click="selectByte(byteIndex - 1)"
            >
              <div class="heatmap-header">
                <span class="byte-label">字节 {{ byteIndex - 1 }}</span>
                <span class="key-byte" v-if="evaluationStore.skey">
                  {{ evaluationStore.skey.substr((byteIndex - 1) * 2, 2).toUpperCase() }}
                </span>
              </div>
              <div 
                :ref="el => setHeatmapRef(byteIndex - 1, el)" 
                class="heatmap-mini"
              ></div>
            </div>
          </div>
          
          <div v-if="selectedByteIndex !== null" class="heatmap-detail">
            <div class="detail-header">
              <span class="detail-title">字节 {{ selectedByteIndex }} 详细视图</span>
              <span class="detail-key" v-if="evaluationStore.skey">
                密钥: {{ evaluationStore.skey.substr(selectedByteIndex * 2, 2).toUpperCase() }}
              </span>
            </div>
            <div ref="heatmapDetailRef" class="heatmap-detail-container"></div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px">
      <el-col :span="8">
        <div class="analysis-section">
          <div class="section-title">
            <el-icon><DataAnalysis /></el-icon>
            <span>分析结果</span>
          </div>
          
          <div class="analysis-content">
            <div class="analysis-item">
              <div class="analysis-label">算法类型</div>
              <el-tag :type="configStore.cipher === 'AES' ? 'primary' : 'success'" size="large" effect="dark">
                {{ configStore.cipher }}
              </el-tag>
            </div>
            
            <div class="analysis-item">
              <div class="analysis-label">测试目标</div>
              <el-tag type="info" size="large" effect="dark">{{ configStore.aim }}</el-tag>
            </div>
            
            <div class="analysis-item">
              <div class="analysis-label">采样组数</div>
              <el-tag type="warning" size="large" effect="dark">{{ samples }}</el-tag>
            </div>
            
            <div class="analysis-item" v-if="evaluationStore.skey">
              <div class="analysis-label">密钥长度</div>
              <el-tag type="danger" size="large" effect="dark">{{ evaluationStore.skey.length / 2 }} 字节</el-tag>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="info-section">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>评估说明</span>
          </div>
          
          <div class="info-content">
            <div class="info-item warning">
              <el-icon><Warning /></el-icon>
              <span>Cache侧信道攻击模拟</span>
            </div>
            <div class="info-item warning">
              <el-icon><Warning /></el-icon>
              <span>通过分析Cache访问模式恢复密钥</span>
            </div>
            <div class="info-item warning">
              <el-icon><Warning /></el-icon>
              <span>热力图显示访问频率分布</span>
            </div>
            <div class="info-item warning">
              <el-icon><Warning /></el-icon>
              <span>点击小图查看详细视图</span>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="legend-section">
          <div class="section-title">
            <el-icon><Grid /></el-icon>
            <span>热力图图例</span>
          </div>
          
          <div class="legend-content">
            <div class="legend-gradient"></div>
            <div class="legend-labels">
              <span>低</span>
              <span>中</span>
              <span>高</span>
            </div>
          </div>
        </div>

        <div class="guide-section" style="margin-top: 20px">
          <div class="section-title">
            <el-icon><Guide /></el-icon>
            <span>结果解读</span>
          </div>
          <div class="guide-content">
            <p>恢复的密钥字节数越少，表示防护方案越有效。热力图中高亮区域表示Cache访问热点。</p>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useEvaluationStore } from '@/stores/evaluation'
import { useConfigStore } from '@/stores/config'
import { mockEvaluationData } from '@/mock/data'
import { 
  Lock, VideoPlay, Refresh, Key, CopyDocument, DataBoard, 
  DataAnalysis, InfoFilled, Warning, Grid, Guide
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const evaluationStore = useEvaluationStore()
const configStore = useConfigStore()
const heatmapDetailRef = ref(null)
const heatmapDetailChart = ref(null)
const heatmapRefs = ref({})
const heatmapCharts = ref({})
const selectedByteIndex = ref(null)
const secretKey = ref('')
const samples = ref(10000)
const heatmapDataCache = ref({})

const setHeatmapRef = (index, el) => {
  if (el) {
    heatmapRefs.value[index] = el
  }
}

const generateRandomKey = () => {
  const key = Array.from({ length: 16 }, () => 
    Math.floor(Math.random() * 256).toString(16).padStart(2, '0')
  ).join('')
  secretKey.value = key
  ElMessage.success('已生成随机密钥')
}

const setTestKey = () => {
  secretKey.value = '9c9e4e3a194bf4cf43afc0bd08ebc924'
  ElMessage.success('已设置测试样例密钥')
}

const formatSkey = (skey) => {
  if (!skey) return ''
  return skey.match(/.{1,2}/g).join('-').toUpperCase()
}

const getKeyBytes = (skey) => {
  if (!skey) return []
  return skey.match(/.{1,2}/g) || []
}

const getByteClass = (index) => {
  if (!evaluationStore.originalSkey || !evaluationStore.skey) return ''
  
  const recoveredByte = parseInt(evaluationStore.skey.substr(index * 2, 2), 16)
  const originalByte = parseInt(evaluationStore.originalSkey.substr(index * 2, 2), 16)
  
  const highNibbleCorrect = (recoveredByte & 0xF0) === (originalByte & 0xF0)
  const fullyCorrect = recoveredByte === originalByte
  
  if (fullyCorrect) {
    return 'fully-correct'
  } else if (highNibbleCorrect) {
    return 'high-nibble-correct'
  } else {
    return 'incorrect'
  }
}

const copySkey = () => {
  if (evaluationStore.skey) {
    navigator.clipboard.writeText(evaluationStore.skey)
    ElMessage.success('密钥已复制到剪贴板')
  }
}

const startEvaluation = async () => {
  if (secretKey.value && !/^[0-9a-fA-F]{32}$/.test(secretKey.value)) {
    ElMessage.error('密钥格式错误，请输入32位十六进制字符')
    return
  }
  
  const result = await evaluationStore.runEvaluation(secretKey.value, samples.value)
  
  if (result.success) {
    ElMessage.success('评估完成')
    const analyzeResult = await evaluationStore.analyzeResult('result')
    if (analyzeResult.mock) {
      ElMessage.warning('后端执行失败，使用Mock数据展示')
    }
  } else {
    ElMessage.warning('评估执行失败，使用Mock数据展示')
    evaluationStore.useMockData = true
    evaluationStore.skey = mockEvaluationData.skey
    evaluationStore.pages = mockEvaluationData.pages
  }
  
  await nextTick()
  await loadAllHeatmaps()
}

const loadAllHeatmaps = async () => {
  for (let i = 0; i < 16; i++) {
    const result = await evaluationStore.getHeatmap(i)
    if (result.success) {
      heatmapDataCache.value[i] = result
      await nextTick()
      updateMiniHeatmap(i, result)
    }
  }
}

const updateMiniHeatmap = (index, data) => {
  const el = heatmapRefs.value[index]
  if (!el) return
  
  if (!heatmapCharts.value[index]) {
    heatmapCharts.value[index] = echarts.init(el)
  }
  
  const chart = heatmapCharts.value[index]
  const maxValue = Math.max(...data.data.flat())
  
  const option = {
    backgroundColor: 'transparent',
    grid: {
      left: '5%',
      right: '5%',
      top: '5%',
      bottom: '5%'
    },
    xAxis: {
      type: 'category',
      data: data.columns,
      show: false
    },
    yAxis: {
      type: 'category',
      data: data.rows,
      show: false
    },
    visualMap: {
      show: false,
      min: 0,
      max: maxValue,
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    series: [{
      type: 'heatmap',
      data: convertToHeatmapData(data.data),
      label: { show: false },
      emphasis: { disabled: true }
    }]
  }
  
  chart.setOption(option, true)
}

const selectByte = async (index) => {
  selectedByteIndex.value = index
  await nextTick()
  
  if (heatmapDataCache.value[index]) {
    updateDetailHeatmap(heatmapDataCache.value[index])
  } else {
    const result = await evaluationStore.getHeatmap(index)
    if (result.success) {
      heatmapDataCache.value[index] = result
      updateDetailHeatmap(result)
    }
  }
}

const updateDetailHeatmap = (data) => {
  if (!heatmapDetailRef.value) return
  
  if (!heatmapDetailChart.value) {
    heatmapDetailChart.value = echarts.init(heatmapDetailRef.value)
  }
  
  const maxValue = Math.max(...data.data.flat())
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      textStyle: { color: '#fff' },
      formatter: function (params) {
        return `明文字节: ${data.rows[params.value[1]]}<br/>Cache集合: ${params.value[0]}<br/>访问次数: ${params.value[2]}`
      }
    },
    grid: {
      left: '12%',
      right: '8%',
      top: '8%',
      bottom: '12%'
    },
    xAxis: {
      type: 'category',
      data: data.columns,
      name: 'Cache Set Index',
      nameLocation: 'middle',
      nameGap: 25,
      nameTextStyle: { color: 'rgba(255, 255, 255, 0.6)' },
      splitArea: {
        show: true,
        areaStyle: { color: ['rgba(255, 255, 255, 0.02)', 'rgba(255, 255, 255, 0.05)'] }
      },
      axisLabel: { interval: 7, fontSize: 10, color: 'rgba(255, 255, 255, 0.6)' },
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.2)' } }
    },
    yAxis: {
      type: 'category',
      data: data.rows,
      name: 'Plaintext Byte',
      nameLocation: 'middle',
      nameGap: 40,
      nameTextStyle: { color: 'rgba(255, 255, 255, 0.6)' },
      splitArea: {
        show: true,
        areaStyle: { color: ['rgba(255, 255, 255, 0.02)', 'rgba(255, 255, 255, 0.05)'] }
      },
      axisLabel: { color: 'rgba(255, 255, 255, 0.6)' },
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.2)' } }
    },
    visualMap: {
      min: 0,
      max: maxValue,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      textStyle: { color: 'rgba(255, 255, 255, 0.6)' },
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    series: [{
      name: 'Cache Access',
      type: 'heatmap',
      data: convertToHeatmapData(data.data),
      label: { show: false },
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' }
      }
    }]
  }
  
  heatmapDetailChart.value.setOption(option, true)
}

const convertToHeatmapData = (data) => {
  const result = []
  for (let i = 0; i < data.length; i++) {
    for (let j = 0; j < data[i].length; j++) {
      result.push([j, i, data[i][j]])
    }
  }
  return result
}

onMounted(async () => {
  await nextTick()
})
</script>

<style scoped>
.evaluation-page {
  padding: 0;
  min-height: calc(100vh - 110px);
}

.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
}

.title-section {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 28px;
  color: #f56c6c;
}

.page-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 5px 0 0 0;
}

.target-badge {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding: 12px 20px;
  background: rgba(245, 108, 108, 0.1);
  border: 1px solid rgba(245, 108, 108, 0.3);
  border-radius: 12px;
}

.badge-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.badge-value {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
}

.control-section,
.heatmap-section,
.analysis-section,
.info-section,
.legend-section,
.guide-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
}

.section-title .el-icon {
  font-size: 20px;
  color: #409eff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-info {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.control-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-row {
  display: flex;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
}

.control-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.key-control {
  flex-direction: column;
  align-items: flex-start !important;
  gap: 10px !important;
}

.key-input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.key-input {
  width: 380px;
}

.key-buttons {
  display: flex;
  gap: 10px;
}

.test-key-btn, .random-key-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.7) !important;
}

.test-key-btn:hover, .random-key-btn:hover {
  border-color: rgba(245, 108, 108, 0.5) !important;
  color: rgba(245, 108, 108, 0.9) !important;
  background: rgba(245, 108, 108, 0.1) !important;
}

.samples-control {
  flex-direction: column;
  align-items: flex-start !important;
  gap: 10px !important;
}

.samples-input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.samples-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quick-select {
  display: flex;
  gap: 6px;
}

.preset-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.7) !important;
}

.preset-btn:hover {
  border-color: rgba(245, 108, 108, 0.5) !important;
  color: rgba(245, 108, 108, 0.9) !important;
}

.preset-btn.el-button--danger {
  background: rgba(245, 108, 108, 0.2) !important;
  border-color: rgba(245, 108, 108, 0.5) !important;
  color: rgba(245, 108, 108, 1) !important;
}

.slider-group {
  width: 100%;
  max-width: 320px;
}

.samples-slider {
  --el-slider-main-bg-color: rgba(245, 108, 108, 0.6);
  --el-slider-runway-bg-color: rgba(255, 255, 255, 0.1);
}

:deep(.samples-slider .el-slider__bar) {
  background: linear-gradient(90deg, rgba(245, 108, 108, 0.4), rgba(245, 108, 108, 0.8));
}

:deep(.samples-slider .el-slider__button) {
  border-color: rgba(245, 108, 108, 0.8);
}

.samples-input {
  width: 100px;
}

.samples-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.samples-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 255, 255, 0.3);
}

.samples-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(245, 108, 108, 0.6);
}

.samples-input :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
}

.input-suffix {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.control-actions {
  display: flex;
  gap: 12px;
  margin-left: auto;
}

.action-btn.danger {
  padding: 12px 24px;
  background: linear-gradient(135deg, #f56c6c 0%, #e64242 100%);
  border: none;
}

.result-section {
  margin-top: 20px;
  padding: 20px;
  background: rgba(103, 194, 58, 0.1);
  border: 1px solid rgba(103, 194, 58, 0.3);
  border-radius: 12px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  color: #67c23a;
  font-weight: 600;
}

.result-icon {
  font-size: 20px;
}

.result-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.skey-value {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  font-size: 16px;
  color: #67c23a;
  letter-spacing: 1px;
}

.skey-bytes {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  font-family: 'Courier New', monospace;
  font-weight: 700;
  font-size: 16px;
}

.skey-byte {
  padding: 4px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.skey-byte.fully-correct {
  color: #67c23a;
  background: rgba(103, 194, 58, 0.2);
  box-shadow: 0 0 8px rgba(103, 194, 58, 0.3);
}

.skey-byte.high-nibble-correct {
  color: #e6a23c;
  background: rgba(230, 162, 60, 0.2);
  box-shadow: 0 0 8px rgba(230, 162, 60, 0.2);
}

.skey-byte.incorrect {
  color: #f56c6c;
  background: rgba(245, 108, 108, 0.2);
  box-shadow: 0 0 8px rgba(245, 108, 108, 0.2);
}

.copy-btn {
  background: rgba(103, 194, 58, 0.2);
  border-color: rgba(103, 194, 58, 0.3);
  color: #67c23a;
}

.result-stats {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.result-stats .stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.result-stats .stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  min-width: 80px;
}

.result-stats .stat-value {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.result-stats .stat-value.correct {
  color: #67c23a;
}

.result-stats .stat-value.correct.all {
  color: #67c23a;
  text-shadow: 0 0 10px rgba(103, 194, 58, 0.5);
}

.heatmap-container {
  width: 100%;
  height: 500px;
}

.heatmaps-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.heatmap-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.heatmap-item:hover {
  border-color: rgba(245, 108, 108, 0.3);
  background: rgba(245, 108, 108, 0.05);
}

.heatmap-item.active {
  border-color: rgba(245, 108, 108, 0.6);
  background: rgba(245, 108, 108, 0.1);
  box-shadow: 0 0 10px rgba(245, 108, 108, 0.2);
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.byte-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

.key-byte {
  font-size: 10px;
  font-family: monospace;
  color: rgba(245, 108, 108, 0.9);
  background: rgba(245, 108, 108, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
}

.heatmap-mini {
  width: 100%;
  height: 60px;
}

.heatmap-detail {
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.detail-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.detail-key {
  font-family: monospace;
  color: rgba(245, 108, 108, 0.9);
  background: rgba(245, 108, 108, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 13px;
}

.heatmap-detail-container {
  width: 100%;
  height: 400px;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.analysis-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.analysis-label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.info-item.warning {
  background: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
}

.info-item.warning .el-icon {
  color: #e6a23c;
}

.info-item span {
  font-size: 13px;
}

.legend-content {
  padding: 10px 0;
}

.legend-gradient {
  height: 20px;
  background: linear-gradient(to right, 
    #313695, #4575b4, #74add1, #abd9e9, #e0f3f8, 
    #ffffbf, #fee090, #fdae61, #f46d43, #d73027, #a50026
  );
  border-radius: 4px;
}

.legend-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.guide-content {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  line-height: 1.6;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: none;
}

:deep(.el-input__inner) {
  color: #fff;
}
</style>
