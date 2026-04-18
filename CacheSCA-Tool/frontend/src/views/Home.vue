<template>
  <div class="home-page">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="main-title">
            <span class="title-icon">🔐</span>
            CacheSCA 测试平台
          </h1>
          <p class="subtitle">Cache侧信道攻击防护评估系统</p>
        </div>
        <div class="header-decoration">
          <div class="pulse-ring"></div>
          <div class="pulse-ring delay-1"></div>
          <div class="pulse-ring delay-2"></div>
        </div>
      </div>
    </div>
    <el-row :gutter="24" class="main-content">
      <el-col :span="12">
        <div class="config-section">
          <div class="section-header">
            <div class="step-badge">Step 1</div>
            <h2>选择加密算法</h2>
          </div>
          
          <div class="cipher-cards">
            <div 
              class="cipher-card" 
              :class="{ active: configStore.cipher === 'AES' }"
              @click="selectCipher('AES')"
            >
              <div class="card-glow"></div>
              <div class="card-content">
                <div class="cipher-icon aes-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z" />
                  </svg>
                </div>
                <h3>AES</h3>
                <p>高级加密标准</p>
                <div class="cipher-specs">
                  <span class="spec-tag">128/192/256位密钥(内置为128位)
                  </span>
                  <span class="spec-tag">128位分组</span>
                  <span class="spec-tag">10/12/14轮(内置为10轮)</span>
                </div>
              </div>
              <div class="card-check" v-if="configStore.cipher === 'AES'">
                <el-icon><CircleCheckFilled /></el-icon>
              </div>
            </div>

            <div 
              class="cipher-card" 
              :class="{ active: configStore.cipher === 'SM4' }"
              @click="selectCipher('SM4')"
            >
              <div class="card-glow"></div>
              <div class="card-content">
                <div class="cipher-icon sm4-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z" />
                  </svg>
                </div>
                <h3>SM4</h3>
                <p>国密分组加密算法</p>
                <div class="cipher-specs">
                  <span class="spec-tag">128位密钥</span>
                  <span class="spec-tag">128位分组</span>
                  <span class="spec-tag">32轮</span>
                </div>
              </div>
              <div class="card-check" v-if="configStore.cipher === 'SM4'">
                <el-icon><CircleCheckFilled /></el-icon>
              </div>
            </div>
          </div>
        </div>

        <div class="config-section">
          <div class="section-header">
            <div class="step-badge">Step 2</div>
            <h2>选择测试目标</h2>
          </div>
          
          <div class="target-grid">
            <div 
              v-for="(target, key) in filteredTargets" 
              :key="key"
              class="target-card"
              :class="{ 
                active: configStore.target === key,
                'is-baseline': key === 'original',
                'is-optimized': ['preload', 'constant_time', 'lut_p'].includes(key),
                'is-custom': key === 'custom'
              }"
              @click="selectTarget(key)"
            >
              <div class="target-badge" v-if="key === 'original'">基准</div>
              <div class="target-badge optimized" v-else-if="['preload', 'constant_time', 'lut_p'].includes(key)">优化方案</div>
              <div class="target-badge custom" v-else-if="key === 'custom'">自定义</div>
              
              <div class="target-icon-wrapper">
                <el-icon class="target-icon">
                  <CircleCheck v-if="key === 'original'" />
                  <Opportunity v-else-if="key === 'preload'" />
                  <Timer v-else-if="key === 'constant_time'" />
                  <Grid v-else-if="key === 'lut_p'" />
                  <Upload v-else />
                </el-icon>
              </div>
              
              <h4>{{ target.name }}</h4>
              <p>{{ target.description }}</p>
              
              <div class="target-check" v-if="configStore.target === key">
                <el-icon><Select /></el-icon>
              </div>
            </div>
          </div>

          <transition name="slide-fade">
            <div v-if="configStore.target === 'custom'" class="custom-upload-section">
              <div class="upload-header">
                <el-icon class="upload-icon"><UploadFilled /></el-icon>
                <span>上传自定义加密库</span>
              </div>
              <el-upload
                class="custom-uploader"
                drag
                action="/api/config/upload-library"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
                accept=".so"
              >
                <div class="upload-content">
                  <el-icon class="upload-icon-large"><UploadFilled /></el-icon>
                  <div class="upload-text">
                    <p>拖拽文件到此处或 <em>点击上传</em></p>
                    <p class="upload-hint">仅支持 .so 格式的动态库文件</p>
                  </div>
                </div>
              </el-upload>
            </div>
          </transition>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="info-panel">
          <div class="current-config">
            <div class="config-header">
              <el-icon class="config-icon"><Setting /></el-icon>
              <span>当前配置</span>
            </div>
            <div class="config-items">
              <div class="config-item">
                <span class="config-label">加密算法</span>
                <el-tag :type="configStore.cipher === 'AES' ? 'primary' : 'success'" size="large" effect="dark">
                  {{ configStore.cipher }}
                </el-tag>
              </div>
              <div class="config-item">
                <span class="config-label">测试目标</span>
                <el-tag type="info" size="large" effect="dark">
                  {{ getTargetLabel(configStore.target) }}
                </el-tag>
              </div>
              <div class="config-item">
                <span class="config-label">目标标识</span>
                <el-tag type="warning" size="large" effect="dark">
                  {{ configStore.aim }}
                </el-tag>
              </div>
            </div>
          </div>

          <div class="guide-section">
            <div class="guide-header">
              <el-icon class="guide-icon"><Guide /></el-icon>
              <span>操作指引</span>
            </div>
            <div class="guide-steps">
              <div class="guide-step">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4>选择算法</h4>
                  <p>选择要测试的加密算法：AES（国际标准）或 SM4（国密标准）</p>
                </div>
              </div>
              <div class="guide-step">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4>选择目标</h4>
                  <p>选择测试目标：原始实现作为基准，或选择优化方案进行对比评估</p>
                </div>
              </div>
              <div class="guide-step">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4>开始测试</h4>
                  <p>配置完成后，前往「性能测试」或「安全性评估」页面进行测试</p>
                </div>
              </div>
            </div>
          </div>

          <div class="principle-section">
            <div class="principle-header">
              <el-icon class="principle-icon"><Reading /></el-icon>
              <span>测试原理</span>
            </div>
            <div class="principle-content">
              <div class="principle-item">
                <h4>🎯 Cache侧信道攻击</h4>
                <p>利用CPU缓存的访问时间差异，通过测量加密操作的执行时间或缓存访问模式，推断出密钥信息。</p>
              </div>
              <div class="principle-item">
                <h4>🛡️ 防护方案</h4>
                <ul>
                  <li><strong>预加载表</strong>：提前加载查找表到缓存，减少缓存未命中</li>
                  <li><strong>常量时间</strong>：消除数据依赖的分支和内存访问</li>
                  <li><strong>并行拆分表</strong>：将查找表拆分，增加攻击复杂度</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="result-section">
            <div class="result-header">
              <el-icon class="result-icon"><DataAnalysis /></el-icon>
              <span>结果解读</span>
            </div>
            <div class="result-content">
              <div class="result-item">
                <div class="result-icon-wrapper success">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="result-text">
                  <h4>性能测试</h4>
                  <p>时钟周期越少，性能越好。对比原始实现与优化方案的执行效率差异。</p>
                </div>
              </div>
              <div class="result-item">
                <div class="result-icon-wrapper warning">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="result-text">
                  <h4>安全性评估</h4>
                  <p>恢复密钥字节数越少，安全性越高。评估防护方案抵御侧信道攻击的能力。</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { 
  Setting, Upload, UploadFilled, CircleCheck, CircleCheckFilled,
  Opportunity, Timer, Grid, Select, Guide, Reading, DataAnalysis,
  TrendCharts, Warning
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const configStore = useConfigStore()

const targetLabels = {
  'original': '原始实现',
  'preload': '预加载表',
  'constant_time': '常量时间',
  'lut_p': '并行拆分查找表',
  'custom': '自定义'
}

const targetDescriptions = {
  'original': {
    name: '原始实现',
    description: '未加固的原始加密实现，作为基准对比'
  },
  'preload': {
    name: '预加载表',
    description: '通过预加载查找表来缓解Cache攻击'
  },
  'constant_time': {
    name: '常量时间',
    description: '使用常量时间算法消除时间侧信道'
  },
  'lut_p': {
    name: '并行拆分查找表',
    description: '创新的并行拆分查找表加固方案'
  },
  'custom': {
    name: '自定义',
    description: '上传自定义的加密库进行测试'
  }
}

const filteredTargets = computed(() => {
  const targets = { ...targetDescriptions }
  if (configStore.cipher === 'SM4') {
    delete targets['constant_time']
  }
  return targets
})

const getTargetLabel = (target) => {
  return targetLabels[target] || target
}

const selectCipher = async (cipher) => {
  configStore.cipher = cipher
  await onCipherChange()
}

const selectTarget = async (target) => {
  configStore.target = target
  await onTargetChange()
}

const onCipherChange = async () => {
  await configStore.loadTargets()
  if (!configStore.targets.includes(configStore.target)) {
    configStore.target = 'original'
    await configStore.setConfig(configStore.cipher, configStore.target)
  }
}

const onTargetChange = async () => {
  await configStore.setConfig(configStore.cipher, configStore.target)
}

const handleUploadSuccess = (response) => {
  if (response.success) {
    ElMessage.success('自定义库上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败，请重试')
}

onMounted(async () => {
  await configStore.loadConfig()
})
</script>

<style scoped>
.home-page {
  padding: 0;
  height: auto;
  overflow-x: hidden;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.title-section {
  z-index: 1;
}

.main-title {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.title-icon {
  font-size: 36px;
}

.subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0 0;
}

.header-decoration {
  position: relative;
  width: 100px;
  height: 100px;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid #409eff;
  border-radius: 50%;
  animation: pulse 2s ease-out infinite;
}

.pulse-ring.delay-1 {
  animation-delay: 0.5s;
}

.pulse-ring.delay-2 {
  animation-delay: 1s;
}

@keyframes pulse {
  0% {
    transform: scale(0.5);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.main-content {
  height: auto;
  overflow: visible;
}

.config-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.step-badge {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: #fff;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.section-header h2 {
  color: #fff;
  font-size: 20px;
  margin: 0;
}

.cipher-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.cipher-card {
  position: relative;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  overflow: hidden;
}

.cipher-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.12);
}

.cipher-card.active {
  border-color: #409eff;
  background: rgba(64, 158, 255, 0.15);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
}

.cipher-card.active .card-glow {
  opacity: 1;
  animation: glow-rotate 3s linear infinite;
}

@keyframes glow-rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.card-content {
  position: relative;
  z-index: 1;
}

.cipher-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.cipher-icon svg {
  width: 28px;
  height: 28px;
}

.aes-icon {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
  color: #fff;
}

.sm4-icon {
  background: linear-gradient(135deg, #67c23a 0%, #95d475 100%);
  color: #fff;
}

.cipher-card h3 {
  color: #fff;
  font-size: 22px;
  margin: 0 0 5px 0;
}

.cipher-card p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0 0 15px 0;
}

.cipher-specs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.spec-tag {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.card-check {
  position: absolute;
  top: 15px;
  right: 15px;
  color: #409eff;
  font-size: 24px;
}

.target-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.target-card {
  position: relative;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.target-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.12);
}

.target-card.active {
  border-color: #67c23a;
  background: rgba(103, 194, 58, 0.15);
}

.target-card.is-baseline {
  grid-column: span 2;
}

.target-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
}

.target-badge.optimized {
  background: linear-gradient(135deg, #67c23a 0%, #95d475 100%);
}

.target-badge.custom {
  background: linear-gradient(135deg, #e6a23c 0%, #f0c78a 100%);
}

.target-icon-wrapper {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.target-icon {
  font-size: 22px;
  color: #409eff;
}

.target-card.active .target-icon {
  color: #67c23a;
}

.target-card h4 {
  color: #fff;
  font-size: 16px;
  margin: 0 0 5px 0;
}

.target-card p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  margin: 0;
  line-height: 1.4;
}

.target-check {
  position: absolute;
  bottom: 10px;
  right: 10px;
  color: #67c23a;
  font-size: 20px;
}

.custom-upload-section {
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px dashed rgba(255, 255, 255, 0.2);
}

.upload-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  color: #fff;
}

.upload-icon {
  font-size: 20px;
  color: #e6a23c;
}

.custom-uploader :deep(.el-upload-dragger) {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  transition: all 0.3s;
}

.custom-uploader :deep(.el-upload-dragger:hover) {
  border-color: #409eff;
  background: rgba(64, 158, 255, 0.1);
}

.upload-content {
  padding: 30px;
  text-align: center;
}

.upload-icon-large {
  font-size: 48px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 15px;
}

.upload-text {
  color: rgba(255, 255, 255, 0.7);
}

.upload-text p {
  margin: 5px 0;
}

.upload-text em {
  color: #409eff;
  font-style: normal;
}

.upload-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.info-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.current-config,
.guide-section,
.principle-section,
.result-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.config-header,
.guide-header,
.principle-header,
.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.config-icon,
.guide-icon,
.principle-icon,
.result-icon {
  font-size: 20px;
  color: #409eff;
}

.config-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.config-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.guide-step {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  transition: all 0.3s;
}

.guide-step:hover {
  background: rgba(255, 255, 255, 0.08);
}

.step-number {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.step-content h4 {
  color: #fff;
  font-size: 14px;
  margin: 0 0 5px 0;
}

.step-content p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  margin: 0;
  line-height: 1.5;
}

.principle-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.principle-item {
  padding: 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.principle-item h4 {
  color: #fff;
  font-size: 14px;
  margin: 0 0 10px 0;
}

.principle-item p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  margin: 0;
  line-height: 1.6;
}

.principle-item ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  line-height: 1.8;
}

.principle-item li strong {
  color: #409eff;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.result-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.result-icon-wrapper.success {
  background: rgba(103, 194, 58, 0.2);
  color: #67c23a;
}

.result-icon-wrapper.warning {
  background: rgba(230, 162, 60, 0.2);
  color: #e6a23c;
}

.result-icon-wrapper .el-icon {
  font-size: 22px;
}

.result-text h4 {
  color: #fff;
  font-size: 14px;
  margin: 0 0 5px 0;
}

.result-text p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  margin: 0;
  line-height: 1.5;
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

:deep(.el-tag) {
  border: none;
}
</style>
