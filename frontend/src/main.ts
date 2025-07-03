import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'
import router from './router'

// Import Quasar css
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

// Import AMS Theme
import './css/ams-theme.scss'

import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: {
    Notify
  },
  config: {
    brand: {
      primary: '#003d7a',    // AMS Dunkelblau
      secondary: '#0066cc',  // AMS Hellblau
      accent: '#00a8e1',     // AMS Akzentblau
      dark: '#1D1D1D',
      positive: '#4caf50',
      negative: '#f44336',
      info: '#00a8e1',
      warning: '#ff9800'
    }
  }
})

app.mount('#app')