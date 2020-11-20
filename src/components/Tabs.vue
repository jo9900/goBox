<template>
    <div id="tab">
        <div class="el-tabs el-tabs--card el-tabs--top">
            <div class="el-tabs__header is-top">
                <div class="el-tabs__nav-wrap is-top">
                    <div class="el-tabs__nav-scroll">
                        <div class="el-tabs__nav is-top" role="tablist" style="transform: translateX(0px);">
                            <div id="tab-first" @click="changeTab(0)" v-show="$store.state.show0" role="tab" tabindex="0" :class="[$store.state.index == 0? 'is-active': '','el-tabs__item is-top']">
                                <router-link to="/" tag="div">
                                    <span class="text">导航</span>
                                </router-link>
                            </div>
                            <div id="tab-second" @click="changeTab(1)" v-show="$store.state.show1" @dblclick="close(1)" role="tab" tabindex="1" :class="[$store.state.index == 1? 'is-active': '','el-tabs__item is-top']">
                                <router-link to="/boxes" tag="div">
                                    <span class="text">货柜设置</span>
                                </router-link>
                            </div>
                            <div id="tab-third" @click="changeTab(2)" v-show="$store.state.show2" @dblclick="close(2)" role="tab" tabindex="2" :class="[$store.state.index == 2? 'is-active': '','el-tabs__item is-top']">
                                <router-link to="/bills" tag="div">
                                    <span class="text">订单管理</span>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: "Tabs",
    data() {
      return {
      }
    },
    methods: {
      changeTab(index) {
        this.$store.commit('changeTab', index)
      },
      close(index) {
        this[`show${index}`] = false
        this.changeTab(0) // 关闭标签后回到导航页面
      }
    }
  }
</script>

<style scoped lang="less">
    #tab-first, #tab-second, #tab-third{
        padding: 0;
    }
    .text {
        display: block;
        text-align: center;
        padding: 0 20px;
    }
</style>