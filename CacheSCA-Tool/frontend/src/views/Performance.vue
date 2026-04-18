<template>
  <div class="performance-page">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><TrendCharts /></el-icon>
            性能测试
          </h1>
          <p class="page-subtitle">测试加密算法在不同负载下的执行性能</p>
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
            <el-icon><Odometer /></el-icon>
            <span>测试控制</span>
          </div>
          
          <div class="control-content">
            <div class="control-item">
              <label class="control-label">测试数据</label>
              <el-select v-model="testdataType" placeholder="选择测试数据" size="large" style="width: 200px">
                <el-option label="内置数据" value="built-in" />
                <el-option label="自定义数据" value="custom" />
              </el-select>
            </div>
            
            <div class="control-item" v-if="testdataType === 'custom'">
              <label class="control-label">自定义文件</label>
              <el-upload
                :show-file-list="false"
                :before-upload="handleFileUpload"
                accept=".txt,.dat"
              >
                <el-button type="primary" size="large">
                  <el-icon><Upload /></el-icon>
                  选择文件
                </el-button>
              </el-upload>
              <el-tag v-if="customFile" type="success" style="margin-left: 10px">
                {{ customFile }}
              </el-tag>
            </div>
            
            <div class="control-actions">
              <el-button 
                type="primary" 
                size="large"
                @click="startTest"
                :loading="performanceStore.testing"
                class="action-btn"
              >
                <el-icon><VideoPlay /></el-icon>
                开始测试
              </el-button>
              
              <el-button 
                size="large"
                @click="saveResults"
                :disabled="!hasResults"
                class="action-btn secondary"
              >
                <el-icon><Download /></el-icon>
                保存结果
              </el-button>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px">
      <el-col :span="16">
        <div class="chart-section">
          <div class="section-header">
            <div class="section-title">
              <el-icon><TrendCharts /></el-icon>
              <span>性能对比图表</span>
            </div>
            <div class="section-actions">
              <el-button size="small" @click="showCompareDialog = true">
                <el-icon><Plus /></el-icon>
                添加对比
              </el-button>
              <el-button size="small" @click="clearComparison" :disabled="!hasComparison">
                <el-icon><Delete /></el-icon>
                清除对比
              </el-button>
            </div>
          </div>
          
          <div ref="chartRef" class="chart-container"></div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="stats-section">
          <div class="section-title">
            <el-icon><DataAnalysis /></el-icon>
            <span>测试统计</span>
          </div>
          
          <div class="stats-content">
            <div class="stat-item" v-for="(value, level) in performanceStore.results" :key="level">
              <div class="stat-header">
                <span class="stat-label">{{ getLevelLabel(level) }}</span>
                <el-tag :type="getLevelType(level)" size="small" effect="dark">{{ level }}</el-tag>
              </div>
              <div class="stat-value">{{ formatNumber(value) }}</div>
              <div class="stat-unit">时钟周期</div>
            </div>
          </div>
        </div>

        <div class="info-section" style="margin-top: 20px">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>负载说明</span>
          </div>
          
          <div class="info-content">
            <div class="info-item">
              <el-tag type="success" size="small" effect="dark">Low</el-tag>
              <span>低负载 - 系统空闲状态</span>
            </div>
            <div class="info-item">
              <el-tag type="info" size="small" effect="dark">Medium</el-tag>
              <span>中负载 - 正常工作负载</span>
            </div>
            <div class="info-item">
              <el-tag type="warning" size="small" effect="dark">High</el-tag>
              <span>高负载 - 高强度工作负载</span>
            </div>
            <div class="info-item">
              <el-tag type="danger" size="small" effect="dark">Extreme</el-tag>
              <span>极限负载 - 最大压力测试</span>
            </div>
          </div>
        </div>

        <div class="guide-section" style="margin-top: 20px">
          <div class="section-title">
            <el-icon><Guide /></el-icon>
            <span>结果解读</span>
          </div>
          <div class="guide-content">
            <p>时钟周期越少，表示加密操作执行效率越高。对比不同负载下的性能表现，评估优化方案的效果。</p>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-dialog v-model="showCompareDialog" title="添加对比数据" width="500px" class="dark-dialog">
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :on-change="handleCompareFileChange"
        :file-list="compareFiles"
        accept=".txt"
        multiple
      >
        <template #trigger>
          <el-button type="primary">选择文件</el-button>
        </template>
        <template #tip>
          <div class="el-upload__tip">选择性能测试结果文件进行对比</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showCompareDialog = false">取消</el-button>
        <el-button type="primary" @click="addComparison">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { usePerformanceStore } from '@/stores/performance'
import { useConfigStore } from '@/stores/config'
import { 
  Odometer, VideoPlay, Download, Plus, Delete, Upload, 
  TrendCharts, DataAnalysis, InfoFilled, Guide, Warning
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const performanceStore = usePerformanceStore()
const configStore = useConfigStore()
const chartRef = ref(null)
const chart = ref(null)
const testdataType = ref('built-in')
const customFile = ref('')
const showCompareDialog = ref(false)
const compareFiles = ref([])
const uploadRef = ref(null)

const hasResults = computed(() => {
  return Object.keys(performanceStore.results).length > 0
})

const hasComparison = computed(() => {
  return Object.keys(performanceStore.comparisonData).length > 0
})

const levelLabels = {
  'low': '低负载',
  'medium': '中负载',
  'high': '高负载',
  'extreme': '极限负载'
}

const getLevelLabel = (level) => levelLabels[level] || level

const getLevelType = (level) => {
  const types = {
    'low': 'success',
    'medium': 'info',
    'high': 'warning',
    'extreme': 'danger'
  }
  return types[level] || 'info'
}

const formatNumber = (num) => {
  if (!num) return '0'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const handleFileUpload = (file) => {
  customFile.value = file.name
  return false
}

const startTest = async () => {
  const datafile = testdataType.value === 'custom' ? customFile.value : 'data'
  const result = await performanceStore.runTest(datafile)
  
  if (result.success) {
    if (result.mock) {
      ElMessage.warning('性能测试执行失败，使用Mock数据展示')
    } else {
      ElMessage.success('性能测试完成')
    }
    await nextTick()
    updateChart()
  } else {
    ElMessage.error(result.message || '测试失败')
  }
}

const saveResults = async () => {
  const filename = `performance_${Date.now()}.txt`
  const result = await performanceStore.saveResult(filename)
  if (result.success) {
    ElMessage.success(`结果已保存: ${result.filepath || filename}`)
  } else {
    ElMessage.error('保存失败')
  }
}

const handleCompareFileChange = (file, fileList) => {
  compareFiles.value = fileList
}

const addComparison = async () => {
  if (compareFiles.value.length === 0) {
    ElMessage.warning('请选择文件')
    return
  }
  
  const filePaths = compareFiles.value.map(f => f.raw.path || f.name)
  const result = await performanceStore.compareResults(filePaths)
  
  if (result.success) {
    ElMessage.success('对比数据已添加')
    showCompareDialog.value = false
    compareFiles.value = []
    await nextTick()
    updateChart()
  } else {
    ElMessage.error(result.message || '添加失败')
  }
}

const clearComparison = () => {
  performanceStore.clearComparison()
  updateChart()
  ElMessage.success('对比数据已清除')
}

const updateChart = () => {
  if (!chart.value) {
    chart.value = echarts.init(chartRef.value)
  }
  
  const levels = ['low', 'medium', 'high', 'extreme']
  const levelNames = ['Low', 'Medium', 'High', 'Extreme']
  
  const series = []
  const allData = { '当前测试': performanceStore.results, ...performanceStore.comparisonData }
  
  Object.entries(allData).forEach(([name, data], index) => {
    const values = levels.map(level => data[level] || 0)
    series.push({
      name,
      type: 'bar',
      data: values,
      itemStyle: {
        color: index === 0 ? '#409eff' : getSeriesColor(index),
        borderRadius: [4, 4, 0, 0]
      },
      label: {
        show: true,
        position: 'top',
        formatter: '{c}',
        fontWeight: 'bold',
        color: '#fff'
      }
    })
  })
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      textStyle: {
        color: '#fff'
      }
    },
    legend: {
      data: Object.keys(allData),
      top: 10,
      textStyle: {
        color: 'rgba(255, 255, 255, 0.7)'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: levelNames,
      axisLabel: {
        fontSize: 14,
        fontWeight: 'bold',
        color: 'rgba(255, 255, 255, 0.8)'
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '时钟周期',
      nameTextStyle: {
        color: 'rgba(255, 255, 255, 0.6)'
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.6)',
        formatter: value => {
          if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
          if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
          return value
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    },
    series
  }
  
  chart.value.setOption(option, true)
}

const getSeriesColor = (index) => {
  const colors = ['#67c23a', '#e6a23c', '#f56c6c', '#909399', '#00d4ff']
  return colors[index % colors.length]
}

watch(() => performanceStore.results, () => {
  updateChart()
}, { deep: true })

onMounted(async () => {
  await nextTick()
  updateChart()
})
</script>

<style scoped>
.performance-page {
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
  color: #409eff;
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
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 12px;
}

.badge-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.badge-value {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
}

.control-section,
.chart-section,
.stats-section,
.info-section,
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
  gap: 10px;
}

.control-content {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
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
}

.control-actions {
  display: flex;
  gap: 12px;
  margin-left: auto;
}

.action-btn {
  padding: 12px 24px;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.chart-container {
  width: 100%;
  height: 450px;
}

.stats-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-item {
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stat-label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-unit {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.info-item span {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
}

.guide-content {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  line-height: 1.6;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: none;
}

:deep(.el-input__inner) {
  color: #fff;
}

:deep(.el-form-item__label) {
  color: rgba(255, 255, 255, 0.7);
}
</style>
