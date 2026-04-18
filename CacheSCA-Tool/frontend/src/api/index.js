import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export const configApi = {
  getTargets(cipher) {
    return api.get('/config/targets', { params: { cipher } })
  },
  setConfig(data) {
    return api.post('/config/set-config', data)
  },
  getConfig() {
    return api.get('/config/get-config')
  }
}

export const performanceApi = {
  runTest(data) {
    return api.post('/performance/test', data)
  },
  compareResults(files) {
    return api.post('/performance/compare', { files })
  },
  saveResult(data) {
    return api.post('/performance/save', data)
  }
}

export const evaluationApi = {
  runEvaluation(data) {
    return api.post('/evaluation/test', data)
  },
  analyzeResult(filepath) {
    return api.post('/evaluation/analyze', { filepath })
  },
  getHeatmap(data) {
    return api.post('/evaluation/heatmap', data)
  }
}

export default api
