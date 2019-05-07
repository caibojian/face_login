import Vue from 'vue'
import App from './App.vue'
import '@/styles/weui.css'
import '@/styles/page.css'
import router from './router'
import store from './store'
import './permission' // permission control
import Vconsole from 'vconsole'

let vConsole = new Vconsole()


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

export default vConsole