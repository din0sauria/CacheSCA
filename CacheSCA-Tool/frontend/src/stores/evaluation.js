import { defineStore } from 'pinia'
import { evaluationApi } from '@/api'
import { mockEvaluationData } from '@/mock/data'

export const useEvaluationStore = defineStore('evaluation', {
  state: () => ({
    skey: '',
    originalSkey: '',
    pages: 0,
    currentPage: 0,
    heatmapData: null,
    evaluating: false,
    useMockData: false,
    correctBytes: 0,
    correctHighNibbles: 0,
    totalBytes: 16
  }),

  actions: {
    async runEvaluation(skey = '', samples = 1000) {
      this.evaluating = true
      try {
        const response = await evaluationApi.runEvaluation({
          skey,
          samples,
          output: 'result'
        })
        return response.data
      } catch (error) {
        console.error('Failed to run evaluation:', error)
        return { success: false, message: error.message }
      } finally {
        this.evaluating = false
      }
    },

    async analyzeResult(filepath) {
      try {
        const response = await evaluationApi.analyzeResult(filepath)
        if (response.data.success) {
          if (!response.data.skey || response.data.skey === '00000000000000000000000000000000') {
            console.log('Using mock data: invalid skey')
            return this._useMockAnalyzeResult()
          }
          this.skey = response.data.skey
          this.pages = response.data.pages
          this.currentPage = 0
          this.useMockData = false
          this.originalSkey = response.data.original_skey || ''
          this.correctBytes = response.data.correct_bytes || 0
          this.correctHighNibbles = response.data.correct_high_nibbles || 0
          this.totalBytes = response.data.total_bytes || 16
        }
        return response.data
      } catch (error) {
        console.error('Failed to analyze result, using mock data:', error)
        return this._useMockAnalyzeResult()
      }
    },

    _useMockAnalyzeResult() {
      this.skey = mockEvaluationData.skey
      this.pages = mockEvaluationData.pages
      this.currentPage = 0
      this.useMockData = true
      return { success: true, skey: this.skey, pages: this.pages, mock: true }
    },

    async getHeatmap(index = 0) {
      if (this.useMockData) {
        return this._getMockHeatmap(index)
      }
      
      try {
        const response = await evaluationApi.getHeatmap({ index })
        if (response.data.success) {
          const data = response.data.data
          if (!data || data.length === 0 || this._isDataEmpty(data)) {
            console.log('Using mock data: empty heatmap data')
            return this._getMockHeatmap(index)
          }
          this.heatmapData = response.data
        }
        return response.data
      } catch (error) {
        console.error('Failed to get heatmap, using mock data:', error)
        return this._getMockHeatmap(index)
      }
    },

    _isDataEmpty(data) {
      if (!Array.isArray(data) || data.length === 0) return true
      const sum = data.flat().reduce((a, b) => a + b, 0)
      return sum === 0
    },

    _getMockHeatmap(index) {
      const mockResult = mockEvaluationData.getHeatmap(index)
      this.heatmapData = mockResult
      return mockResult
    },

    setPage(index) {
      this.currentPage = index
    }
  }
})
