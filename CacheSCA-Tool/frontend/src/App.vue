<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon-wrapper">
            <el-icon class="logo-icon"><Key /></el-icon>
          </div>
          <div class="title-section">
            <h1 class="app-title">CacheSCA-Tool</h1>
            <p class="app-subtitle">Cache侧信道攻击防护评估系统</p>
          </div>
        </div>
        <div class="header-status">
          <div class="status-indicator">
            <span class="status-dot"></span>
            <span class="status-text">系统就绪</span>
          </div>
        </div>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="220px" class="app-sidebar">
        <div class="sidebar-header">
          <span class="sidebar-title">导航菜单</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/home">
            <el-icon><HomeFilled /></el-icon>
            <span>测试配置</span>
            <div class="menu-indicator"></div>
          </el-menu-item>
          <el-menu-item index="/performance">
            <el-icon><TrendCharts /></el-icon>
            <span>性能测试</span>
            <div class="menu-indicator"></div>
          </el-menu-item>
          <el-menu-item index="/evaluation">
            <el-icon><DataAnalysis /></el-icon>
            <span>安全性评估</span>
            <div class="menu-indicator"></div>
          </el-menu-item>
        </el-menu>
        <div class="sidebar-footer">
          <div class="version-info">
            <el-icon><InfoFilled /></el-icon>
            <span>v1.0.0</span>
          </div>
        </div>
      </el-aside>
      
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  Key, HomeFilled, TrendCharts, DataAnalysis, InfoFilled 
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const handleMenuSelect = (index) => {
  router.push(index)
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.app-container {
  height: 100vh;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  overflow: hidden;
}

.app-header {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  padding: 0 30px;
  height: 70px !important;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon-wrapper {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.logo-icon {
  font-size: 26px;
  color: #fff;
}

.title-section {
  display: flex;
  flex-direction: column;
}

.app-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #fff 0%, #a8a8a8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
}

.app-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin: 2px 0 0 0;
}

.header-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(103, 194, 58, 0.1);
  border: 1px solid rgba(103, 194, 58, 0.3);
  border-radius: 20px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #67c23a;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.status-text {
  font-size: 13px;
  color: #67c23a;
  font-weight: 500;
}

.app-sidebar {
  background: rgba(255, 255, 255, 0.02);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px 20px 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-title {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sidebar-menu {
  border: none !important;
  background: transparent !important;
  flex: 1;
  padding: 10px;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 4px 0;
  border-radius: 12px;
  background: transparent;
  color: rgba(255, 255, 255, 0.6) !important;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.sidebar-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9) !important;
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  color: #fff !important;
  border-left: 3px solid #667eea;
}

.sidebar-menu .el-menu-item .el-icon {
  font-size: 18px;
  margin-right: 12px;
}

.sidebar-menu .el-menu-item .menu-indicator {
  position: absolute;
  right: 15px;
  width: 6px;
  height: 6px;
  background: #667eea;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s;
}

.sidebar-menu .el-menu-item.is-active .menu-indicator {
  opacity: 1;
}

.sidebar-footer {
  padding: 15px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.version-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
}

.app-main {
  background: transparent;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  height: calc(100vh - 70px);
}

.app-main::-webkit-scrollbar {
  width: 8px;
}

.app-main::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.app-main::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.app-main::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
