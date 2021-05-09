import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.productionTip = false
// 请求基准路径的配置
axios.defaults.baseURL = 'http://localhost:5000/'
// 将axios挂载到Vue的原型对象上
Vue.prototype.$http = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
