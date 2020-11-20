import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import router from "./router";
import store from "./store";
import "./registerServiceWorker";
import "./assets/main.less";
import Mixins from "./js/mixins";

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
Vue.use(ElementUI);

function ready(infoData) {
  var vm = new Vue({
    router,
    store,
    data: {
      infoData: infoData
    },
    mixins: [Mixins],
    render: h => h(App),
    mounted() {
      this.$router.replace('/')
      this.getToken(infoData);
      this.interceptors(); // 拦截器
    },
    methods: {
      interceptors() {
        this.$axios.interceptors.request.use(
          config => {
            config.headers["Token"] = this.newToken;
              this.$loading({
                  text: '加载中...',
                  spinner: 'el-icon-loading',
                  background: 'rgba(0, 0, 0, 0.7)'
              });
            return config;
          },
          error => {
            return Promise.reject(error);
          }
        );
        this.$axios.interceptors.response.use(
          response => {
            this.$loading({
                text: '加载中...',
                background: 'rgba(0, 0, 0, 0.1)'
            }).close();
            return response.data;
          },
          error => {
            return Promise.reject(error.response);
          }
        );
      }
    }
  }).$mount("#app");
}

//event 参数中有 data 属性，就是父窗口发送过来的数据
window.addEventListener(
  "message",
  function(event) {
    if (typeof event.data === "string")
      ready(JSON.parse(event.data));
  },
  false
);
