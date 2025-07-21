import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import pinia from './stores'
import naive from 'naive-ui'


let app = createApp(App)
app.use(router)
app.use(naive)
app.use(pinia)
app.mount('#app')
