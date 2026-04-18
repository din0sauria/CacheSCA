import { defineStore } from 'pinia'
import { performanceApi } from '@/api'
import { mockPerformanceData } from '@/mock/data'
import { useConfigStore } from './config'

export const usePerformanceStore = defineStore('performance', {
  state: () => ({
    results: {},
    comparisonData: {},
    testing: false,
    useMockData: false
  }),

  actions: {
    async runTest(datafile = 'data') {
      this.testing = true
      try {
        const response = await performanceApi.runTest({ datafile })
        if (response.data.success) {
          const results = response.data.results
          if (!results || Object.keys(results).length === 0 || this._isResultsEmpty(results)) {
            console.log('Using mock data: empty results')
            return this._useMockResults()
          }
          this.results = results
          this.useMockData = false
        }
        return response.data
      } catch (error) {
        console.error('Failed to run test, using mock data:', error)
        return this._useMockResults()
      } finally {
        this.testing = false
      }
    },

    _isResultsEmpty(results) {
      const values = Object.values(results)
      if (values.length === 0) return true
      return values.every(v => v === 0)
    },

    _useMockResults() {
      const configStore = useConfigStore()
      const aim = configStore.aim || 'original'
      this.results = mockPerformanceData.getMockResults(aim)
      this.useMockData = true
      return { success: true, results: this.results, mock: true }
    },

    async compareResults(files) {
      try {
        const response = await performanceApi.compareResults(files)
        if (response.data.success) {
          this.comparisonData = {
            ...this.comparisonData,
            ...response.data.comparison_data
          }
        }
        return response.data
      } catch (error) {
        console.error('Failed to compare results:', error)
        return { success: false }
      }
    },

    async saveResult(filepath) {
      try {
        const response = await performanceApi.saveResult({
          results: this.results,
          filepath
        })
        return response.data
      } catch (error) {
        console.error('Failed to save result:', error)
        return { success: false }
      }
    },

    clearComparison() {
      this.comparisonData = {}
    }
  }
})
