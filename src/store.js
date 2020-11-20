import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    show0: true,
    show2: false,
    show3: false,
    index: 0
  },
  mutations: {
    changeTab(state, index) {
      this.state.index = index;
      this.state[`show${index}`] = true;
    }
  }
});
