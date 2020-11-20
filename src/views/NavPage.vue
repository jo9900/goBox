<template>
    <div id="navPage">
        <div class="card" @click="changeTo('boxes', 1)">货柜设置</div>
        <div class="card" @click="changeTo('bills', 2)">订单管理</div>
    </div>
</template>

<script>
export default {
    name: "NavPage",
    methods: {
      changeTo(path, index) {
        this.$store.commit("changeTab", index)
        this.$router.push(path)
      }
    }
};
</script>

<style scoped>
    .card {
        height: 200px;
        width: 200px;
        border: 1px solid #ebeef5;
        background-color: #fff;
        -webkit-box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.1);
        box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.1);
        color: #303133;
        line-height: 200px;
        text-align: center;
        float: left;
        margin: 10px 20px;
        border-radius: 4px;
        -webkit-transition: all ease 0.2s;
        transition: all ease 0.2s;
        cursor: default;
        font-size: 16px;
    }
    .card:hover {
        color: #4da3fb;
        -webkit-box-shadow: 0 0 12px 0 rgba(64, 158, 255, 0.1);
        box-shadow: 0 0 12px 0 rgba(64, 158, 255, 0.1);
    }
</style>