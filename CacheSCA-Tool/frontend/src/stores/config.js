import { defineStore } from 'pinia'
import { configApi } from '@/api'

export const useConfigStore = defineStore('config', {
  state: () => ({
    cipher: 'AES',
    target: 'original',
    aim: 'original',
    targets: []
  }),

  actions: {
    _updateAim() {
      if (this.target === 'original') {
        this.aim = 'original'
      } else {
        this.aim = `${this.cipher.toLowerCase()}_${this.target}`
      }
    },

    async loadTargets() {
      try {
        const response = await configApi.getTargets(this.cipher)
        this.targets = response.data.targets
      } catch (error) {
        console.error('Failed to load targets:', error)
        this.targets = this.cipher === 'AES' 
          ? ['original', 'preload', 'constant_time', 'lut_p', 'custom']
          : ['original', 'preload', 'lut_p', 'custom']
      }
    },

    async setConfig(cipher, target) {
      this.cipher = cipher
      this.target = target
      this._updateAim()
      
      try {
        const response = await configApi.setConfig({ cipher, target })
        if (response.data.success) {
          this.cipher = response.data.config.cipher
          this.target = response.data.config.target
          this.aim = response.data.config.aim
        }
        return response.data
      } catch (error) {
        console.error('Failed to set config:', error)
        return { success: true, config: { cipher: this.cipher, target: this.target, aim: this.aim } }
      }
    },

    async loadConfig() {
      try {
        const response = await configApi.getConfig()
        this.cipher = response.data.cipher
        this.target = response.data.target
        this.aim = response.data.aim
        await this.loadTargets()
      } catch (error) {
        console.error('Failed to load config:', error)
        this._updateAim()
        await this.loadTargets()
      }
    }
  }
})
