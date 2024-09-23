import { createApp } from 'vue'
import './style.css'
import App from './VueUpload.vue'
import Vueform from '@vueform/vueform'
import vueformConfig from './../vueform.config'

const app = createApp(App)
app.use(Vueform, vueformConfig)
app.mount('#plugin-VueCode')