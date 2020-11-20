<template>
    <div id="app">
        <my-tab></my-tab>
        <keep-alive>
            <router-view></router-view>
        </keep-alive>
    </div>
</template>
<script>
  import Tabs from './components/Tabs';
  export default {
    components:{
      'my-tab': Tabs
    }
  };
</script>
<style lang="less">
    .el-table .warning-row {
        background: #ff5555;
    }
</style>
