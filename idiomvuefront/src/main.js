import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false;
// 请求基准路径的配置
axios.defaults.baseURL = 'http://localhost:5000/';
// 将axios挂载到Vue的原型对象上
Vue.prototype.$http = axios;
Vue.use(ElementUI);

// Echarts
Vue.prototype.$echarts = window.echarts

new Vue({
  render: h => h(App),
}).$mount('#app');
