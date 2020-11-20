<template>
    <div id="boxes">
        <div class="btns" ref="btns">
            <label>货柜名称&nbsp;</label>
            <el-input v-model.trim="name"
                      placeholder="货柜名称"
                      clearable
                      size="mini"
                      style="width: 200px; margin: 5px"
                      @keyup.enter.native="searchDevices()"></el-input>
            <el-button type="primary" size="mini" @click="searchDevices()" plain>查询</el-button>
            <el-button type="primary" size="mini" @click="openOuterDialog(true)" plain>创建</el-button>
            <el-button type="primary" size="mini" @click="openOuterDialog(false)" plain>编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteDevices()" plain>删除</el-button>
        </div>
        <!--货柜表格-->
        <div class="devices-table">
            <el-table
                    @selection-change="handleSelectionChange"
                    ref="devicesTable"
                    size="mini"
                    border
                    stripe
                    :height="table_height"
                    :data="devicesTableData"
                    empty-text="-"
                    tooltip-effect="dark"
                    style="width: 100%">
                <el-table-column
                        fixed
                        type="selection"
                        width="55">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        align="center"
                        prop="id"
                        label="货柜ID"
                        width="100">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="name"
                        label="货柜名称"
                        width="180">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        align="center"
                        prop="set_of_book"
                        label="账套号"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="dev_id"
                        label="设备ID"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="store_name"
                        label="仓库"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="bank_name"
                        label="收款账户"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="member_name"
                        label="会员"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="employee_name"
                        label="员工"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="bill_type_name"
                        label="发票类型"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="created_at"
                        label="创建时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="created_user"
                        label="创建用户"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="updated_at"
                        label="更新时间"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="updated_user"
                        label="更新用户"
                        width="180">
                </el-table-column>
            </el-table>
        </div>
        <div class="pagination" ref="pagination">
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[30, 50, 100]"
                    :page-size="default_limit"
                    layout="total, sizes,prev, pager, next, jumper"
                    :total="totalDevicesTable">
            </el-pagination>
        </div>
        <!--货柜表格 over-->
        <!--创建编辑货柜弹窗-->
        <div class="createDialog">
            <el-dialog title="货柜设置" :visible.sync="showOuterDialog" width="70%">
                <el-form :model="outerDialogFormData" label-width="100px">
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="货柜名称">
                                <el-input v-model.trim="outerDialogFormData.name"
                                          placeholder="货柜名称" clearable size="mini"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="设备ID">
                                <el-input v-model.trim="outerDialogFormData.dev_id"
                                          placeholder="设备ID" clearable size="mini"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="仓库">
                                <el-input v-model.trim="outerDialogFormData.store_name" :disabled="true"
                                          clearable size="mini"></el-input>
                                <i class="el-icon-search" @click="openInnerDialog('store')"></i>
                                <!--内层模态框-->
                                <el-dialog
                                        width="30%"
                                        title="仓库查询"
                                        :visible.sync="show_store"
                                        append-to-body>
                                    <el-input
                                            placeholder="请输入仓库名"
                                            @keyup.enter.native="filterInnerDialog(queryStrStore, 'store')"
                                            v-model.trim="queryStrStore"
                                            clearable>
                                    </el-input>
                                    <el-table
                                            max-height="400"
                                            ref="singleTable"
                                            :data="innerList"
                                            highlight-current-row
                                            @current-change="select_store"
                                            style="width: 100%">
                                        <el-table-column
                                                property="id"
                                                width="100"
                                                label="ID">
                                        </el-table-column>
                                        <el-table-column
                                                property="name"
                                                label="名称">
                                        </el-table-column>
                                    </el-table>

                                    <el-pagination
                                            @current-change="change_index_store"
                                            small
                                            :page-size="default_limit_in_search"
                                            :current-page="currentPageInnerDialog"
                                            layout="prev, pager, next"
                                            :total="totalInnerDialog">
                                    </el-pagination>
                                </el-dialog>
                                <!--内层模态框 over-->
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="收款账户">
                                <el-input v-model.trim="outerDialogFormData.bank_name" :disabled="true"
                                          clearable size="mini"></el-input>
                                <i class="el-icon-search" @click="openInnerDialog('bank')"></i>
                                <!--内层模态框-->
                                <el-dialog
                                        width="30%"
                                        title="账户查询"
                                        :visible.sync="show_bank"
                                        append-to-body>
                                    <el-input
                                            placeholder="请输入账户名"
                                            @keyup.enter.native="filterInnerDialog(queryStrBank, 'bank')"
                                            v-model.trim="queryStrBank"
                                            clearable>
                                    </el-input>
                                    <el-table
                                            max-height="400"
                                            ref="singleTable"
                                            :data="innerList"
                                            highlight-current-row
                                            @current-change="select_bank"
                                            style="width: 100%">
                                        <el-table-column
                                                property="id"
                                                width="100"
                                                label="ID">
                                        </el-table-column>
                                        <el-table-column
                                                property="name"
                                                label="名称">
                                        </el-table-column>
                                    </el-table>

                                    <el-pagination
                                            @current-change="change_index_bank"
                                            small
                                            :page-size="default_limit_in_search"
                                            :current-page="currentPageInnerDialog"
                                            layout="prev, pager, next"
                                            :total="totalInnerDialog">
                                    </el-pagination>
                                </el-dialog>
                                <!--内层模态框 over-->
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="会员">
                                <el-input v-model.trim="outerDialogFormData.member_name" :disabled="true"
                                          clearable size="mini"></el-input>
                                <i class="el-icon-search" @click="openInnerDialog('member')"></i>
                                <!--内层模态框-->
                                <el-dialog
                                        width="30%"
                                        title="会员查询"
                                        :visible.sync="show_member"
                                        append-to-body>
                                    <el-input
                                            placeholder="请输入会员名"
                                            @keyup.enter.native="searchMember(1, true)"
                                            v-model.trim="queryStrMember"
                                            clearable>
                                    </el-input>
                                    <el-table
                                            max-height="400"
                                            ref="singleTable"
                                            :data="innerList"
                                            highlight-current-row
                                            @current-change="select_member"
                                            style="width: 100%">
                                        <el-table-column
                                                property="id"
                                                width="100"
                                                label="ID">
                                        </el-table-column>
                                        <el-table-column
                                                property="name"
                                                label="名称">
                                        </el-table-column>
                                    </el-table>

                                    <el-pagination
                                            @current-change="change_index_member"
                                            small
                                            :page-size="default_limit_in_search"
                                            :current-page="currentPageInnerDialog"
                                            layout="prev, pager, next"
                                            :total="totalInnerDialog">
                                    </el-pagination>
                                </el-dialog>
                                <!--内层模态框 over-->
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="员工">
                                <el-input v-model.trim="outerDialogFormData.employee_name" :disabled="true"
                                          clearable size="mini"></el-input>
                                <i class="el-icon-search" @click="openInnerDialog('employee')"></i>
                                <!--内层模态框-->
                                <el-dialog
                                        width="30%"
                                        title="员工查询"
                                        :visible.sync="show_employee"
                                        append-to-body>
                                    <el-input
                                            placeholder="请输入员工名"
                                            @keyup.enter.native="filterInnerDialog(queryStrEmployee, 'employee', true)"
                                            v-model.trim="queryStrEmployee"
                                            clearable>
                                    </el-input>
                                    <el-table
                                            max-height="400"
                                            ref="singleTable"
                                            :data="innerList"
                                            highlight-current-row
                                            @current-change="select_employee"
                                            style="width: 100%">
                                        <el-table-column
                                                property="id"
                                                width="100"
                                                label="ID">
                                        </el-table-column>
                                        <el-table-column
                                                property="name"
                                                label="名称">
                                        </el-table-column>
                                    </el-table>

                                    <el-pagination
                                            @current-change="change_index_employee"
                                            small
                                            :page-size="default_limit_in_search"
                                            :current-page="currentPageInnerDialog"
                                            layout="prev, pager, next"
                                            :total="totalInnerDialog">
                                    </el-pagination>
                                </el-dialog>
                                <!--内层模态框 over-->
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-form-item label="发票类型">
                                <el-select v-model="outerDialogFormData.bill_type" size="mini" placeholder="请选择发票类型">
                                    <el-option
                                            v-for="bill_type in bill_type_list"
                                            :label="bill_type.name"
                                            :value="bill_type.val"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button size="small" @click="toggleCreateDialog()">取 消</el-button>
                    <el-button size="small" v-if="isCreate" type="primary" @click="createDevices()">创 建</el-button>
                    <el-button size="small" v-else type="success" @click="editDevices()">更 新</el-button>
                </div>
            </el-dialog>
        </div>
        <!--创建编辑货柜弹窗 over-->
    </div>
</template>

<script>
    /* eslint-disable prettier/prettier */

    export default {
        name: "boxes",
        data() {
            return {
                queryStrStore: "",
                queryStrBank: "",
                queryStrEmployee: "",
                queryStrMember: "",
                isFilterSearch: false, // 如果是过滤的搜索 就不显示下面的翻页
                show: "none",
                currentRow: null,
                isCreate: true,
                table_height: 500,
                name: "",
                new_start: 0,
                default_limit: 50,
                default_limit_in_search: 50,
                totalDevicesTable: 50,
                currentPage: 1,
                currentPageInnerDialog: 1,
                innerList: [], // inner模态框表格的数据
                devicesTableData: [], // 货柜信息表格
                multipleSelection: [], // 多选 选中的行
                outerDialogFormData: {}, // 创建编辑弹窗的数据
                showOuterDialog: false,
                show_bank: false,
                show_store: false,
                show_member: false,
                show_employee: false,
                innerVisible: false,
                isFilterIndexChange: false, // 筛选后的分页切换 默认false，只有当回车搜索时会赋值true，当页面关闭后再次为false
                bill_type_list: [
                    {
                        name: "收据",
                        val: 0
                    }, {
                        name: "发票",
                        val: 1
                    }, {
                        name: "增值税发票",
                        val: 2
                    }
                ],
                cache: [],
                id_arr: [],
                totalInnerDialog: 0, // inner的数据总数
                allFilterData: [], // 过滤后符合的数据
                filter_count: 0 // 过滤后符合的数量
            }
        },
        mounted() {
            this.cache = this.$root.$data.infoData.cache
            this.searchDevices()
            this.$nextTick(() => {
                let autoHeight = document.documentElement.clientHeight
                    - this.$refs.btns.offsetHeight
                    - this.$refs.pagination.offsetHeight
                    - 56
                this.table_height = autoHeight
            });
        },
        watch: {
            queryStrStore: {
                handler(nVal, oVal) {
                    if ( nVal === "" && nVal !== oVal ) { // 清空时显示正常的第一页数据
                        this.isFilterSearch = false
                        this.change_index_store(1)
                    }
                }
            },
            queryStrBank: {
                handler(nVal, oVal) {
                    if ( nVal === "" && nVal !== oVal ) {
                        this.isFilterSearch = false
                        this.change_index_bank(1)
                    }
                }
            },
            queryStrBankEmployee: {
                handler(nVal, oVal) {
                    if ( nVal === "" && nVal !== oVal ) {
                        this.isFilterSearch = false
                        this.change_index_employee(1)
                    }
                }
            },
            queryStrMember: {
                handler(nVal, oVal) {
                    if ( nVal === "" && nVal !== oVal ) {
                        this.isFilterSearch = false
                        this.change_index_member(1)
                    }
                }
            }
        },
        methods: {
            clearQueryStr() {
                this.queryStrStore = ""
                this.queryStrBank = ""
                this.queryStrEmployee = ""
                this.queryStrMember = ""
            },
            openOuterDialog(bool) { // 打开outer模态框
                if ( !bool ) { // 编辑
                    if ( this.multipleSelection.length !== 1 ) {
                        return alert("请选中一行")
                    }
                    this.outerDialogFormData = Object.assign({}, this.outerDialogFormData, this.multipleSelection[0])
                }
                else {
                    this.outerDialogFormData = {} // 编辑和创建共用一个组件 创建时清空表单
                }
                this.showOuterDialog = true
                this.isCreate = bool
            },
            openInnerDialog(item_name) { // 打开Inner模态框 同时获取对应缓存数据 银行 会员 员工 仓库
                this['show_' + item_name] = true
                this.isFilterIndexChange = false
                this.clearQueryStr()
                if ( item_name === 'member' ) {
                    this.searchMember(1)
                    return
                }
                this.searchInDialog(1, item_name) // 打开显示第一页
            },
            select_store(val) {
                if ( val ) {
                    this.currentRow = val; // 获取当前行
                    this.outerDialogFormData.store_name = val.name
                    this.outerDialogFormData.store_id = val.id
                    this.show_store = false
                }
            },
            select_bank(val) {
                if ( val ) {
                    this.currentRow = val;
                    this.outerDialogFormData.bank_name = val.name
                    this.outerDialogFormData.bank_id = val.id
                    this.show_bank = false
                }
            },
            select_member(val) {
                if ( val ) {
                    this.currentRow = val;
                    this.outerDialogFormData.member_name = val.name
                    this.outerDialogFormData.member_id = val.id
                    this.show_member = false
                }
            },
            select_employee(val) {
                if ( val ) {
                    this.currentRow = val;
                    this.outerDialogFormData.employee_name = val.name
                    this.outerDialogFormData.employee_id = val.id
                    this.show_employee = false
                }
            },
            change_index_store(page) {
                this.changeIndex(page, 'store')
            },
            change_index_bank(page) {
                this.changeIndex(page, 'bank')
            },
            change_index_employee(page) {
                this.changeIndex(page, 'employee')
            },
            change_index_member(page) {
                this.changeIndex(page, 'member')
            },
            changeIndex(page, item_name) {
                this.currentPageInnerDialog = page || this.currentPageInnerDialog
                if ( item_name !== "member" ) {
                    this.searchInDialog(page, item_name)  // 员工、银行、仓库的搜索框里的分页切换
                    return
                }
                this.searchMember(page) // 会员搜索框里的分页切换 ——会员是通过请求获取的 其他是通过本地缓存
            },
            searchMember(page = 1, bool = false) { // 只有回车触发时为true
                if ( bool ) this.isFilterIndexChange = bool
                let start = ( page - 1 ) * this.default_limit_in_search
                let params = {
                    name__icontains: this.isFilterIndexChange ? this.queryStrMember : "",
                    start: start,
                    limit: this.default_limit_in_search
                }
                this.$axios({
                    url: "/api/members",
                    params: params
                }).then(res => {
                    if ( res.state === 1 ) {
                        this.totalInnerDialog = res.total
                        this.innerList = res.root
                        return
                    }
                    alert(res.errmsg)
                })
            },
            searchInDialog(page = 1, item_name) { // 员工 银行 等搜索框里的查询
                let start = ( page - 1 ) * this.default_limit_in_search
                let end = page * this.default_limit_in_search
                if ( this.isFilterIndexChange ) { // 过滤后的翻页
                    this.totalInnerDialog = this.filter_count
                    if ( end >= this.totalInnerDialog ) {
                        end = this.totalInnerDialog
                    }
                    this.innerList = this.allFilterData.slice(start, end)
                }
                else { // 正常翻页
                    this.totalInnerDialog = Object.getOwnPropertyNames(this.cache[item_name]).length;
                    if ( end >= this.totalInnerDialog ) {
                        end = this.totalInnerDialog
                    }
                    let arr = []
                    for ( let i in this.cache[item_name] ) {
                        arr.push(this.cache[item_name][i])
                    }
                    this.innerList = arr.slice(start, end)
                }
            },
            filterInnerDialog(str, item_name, bool) { // 仓库的过滤 回车触发
                if ( str === "" ) return
                this.isFilterSearch = true
                if ( bool ) this.isFilterIndexChange = true
                this.innerList = []
                this.allFilterData = []
                this.filter_count = 0
                for ( let i in this.cache[item_name] ) {
                    if ( this.cache[item_name][i].name.includes(str) ) {
                        this.filter_count++
                        this.allFilterData.push(this.cache[item_name][i])
                    }
                }
                this.totalInnerDialog = this.filter_count
                let end = ( end >= this.totalInnerDialog ) ? this.totalInnerDialog : this.default_limit_in_search
                this.innerList = this.allFilterData.slice(0, end)
            },
            deleteDevices() { // 删除货柜
                this.ajaxFunction(null, "DELETE", "删除货柜", "/api/devices/")
            },
            getSelectedID() {
                if ( !this.multipleSelection.length ) {
                    alert("请至少选中一行")
                    return false
                }
                this.id_arr = []
                this.multipleSelection.forEach((val) => {
                    this.id_arr.push(val.id)
                })
                return true
            },
            async ajaxFunction(action, method, text, url = "") {
                if ( !this.getSelectedID() ) return
                let count_failed = 0
                let count_succeed = 0
                let _total = 0
                for await ( let id of this.id_arr ) {
                    this.$axios({
                        method: method,
                        url: url ? url + id : `/api/devices/${id}?action=${action}`
                    }).then(res => {
                        if ( res.state === 1 ) {
                            count_succeed++
                            return
                        }
                        count_failed++
                        alert(res.errmsg)
                    }).finally(() => {
                        _total++
                        if ( _total == this.id_arr.length ) {
                            this.handleCurrentChange(1)
                            alert(`共${this.id_arr.length}条，成功${text}${count_succeed}条，失败${count_failed}条`)
                        }
                    })
                }
                this.multipleSelection = []
            },
            createDevices() {
                let data = JSON.parse(JSON.stringify(this.outerDialogFormData))
                this.$axios({
                    url: "/api/devices",
                    method: "POST",
                    data: data
                }).then(res => {
                    if ( res.state === 1 ) {
                        this.handleCurrentChange(1)
                        this.$message({
                            message: '创建成功',
                            type: 'success'
                        });
                        return
                    }
                    alert(res.errmsg)
                })
                this.toggleCreateDialog()
            },
            editDevices() {
                this.$axios({
                    url: "/api/devices/" + this.multipleSelection[0].id,
                    method: "PUT",
                    data: this.outerDialogFormData
                }).then(res => {
                    if ( res.state === 1 ) {
                        this.handleCurrentChange(1)
                        this.$message({
                            message: '更新成功',
                            type: 'success'
                        });
                        return
                    }
                    alert(res.errmsg)
                })
                this.toggleCreateDialog()
            },
            toggleCreateDialog() { // 显示隐藏编辑新建的模态框
                this.showOuterDialog = !this.showOuterDialog
                this.isCreate = true
            },
            handleSelectionChange(val) { // 货柜表格的多选
                this.multipleSelection = val;
            },
            handleSizeChange(val) {
                this.default_limit = val
            },
            handleCurrentChange(val) { // 货柜表格的分页
                this.currentPage = val || this.currentPage
                this.new_start = ( this.currentPage - 1 ) * this.default_limit
                this.searchDevices()
            },
            changeToName(obj, itemName, id) { // 根据id显示name
                let key = itemName.split('_')[0]
                obj[key + '_name'] = this.cache[key][id].name
            },
            searchDevices() {
                this.devicesTableData = []
                this.$axios({
                    url: "/api/devices",
                    params: {
                        name: this.name,
                        start: this.new_start,
                        limit: this.default_limit
                    }
                }).then(res => {
                    if ( res.state === 1 ) {
                        this.totalDevicesTable = res.total
                        res.root.forEach((val) => {
                            for ( let keyName in val ) {
                                val[keyName] = val[keyName] == null ? "" : val[keyName]
                                if ( keyName === 'bill_type' ) {
                                    val.bill_type_name = this.bill_type_list[val.bill_type].name
                                }
                                if ( keyName === 'store_id' || keyName === 'bank_id' || keyName === 'employee_id' ) {
                                    // 根据id显示name
                                    this.changeToName(val, keyName, val[keyName])
                                }
                            }
                        })
                        this.devicesTableData = res.root
                        return
                    }
                    alert(res.errmsg)
                })
            }
        }
    }
</script>

<style scoped lang="less">
    .createDialog {
        .el-dialog__body {
            padding: 5px 10px;
        }
        .el-dialog__header {
            padding: 5px 20px;
        }
        .el-icon-search {
            position: absolute;
            top: 11px;
            font-size: 20px;
        }
        .el-col-12 {
            width: 45%;
        }
    }

    .btns {
        padding: 0 10px;
    }
</style>