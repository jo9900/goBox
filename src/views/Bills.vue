<template>
    <div id="bill">
        <div class="mainForm" ref="mainForm">
            <div class="item">
                <label>设备ID&nbsp;</label>
                <el-input v-model.trim="mainForm.dev_id"
                          placeholder="设备id" clearable size="mini"></el-input>
            </div>
            <div class="item">
                <label>交易编号&nbsp;</label>
                <el-input v-model.trim="mainForm.trans_id"
                          placeholder="交易编号" clearable size="mini"></el-input>
            </div>
            <div class="item">
                <label>开始时间&nbsp;</label>
                <el-date-picker
                        size="mini"
                        value-format="yyyy-MM-dd"
                        v-model="mainForm.start_date"
                        type="date">
                </el-date-picker>
            </div>
            <div class="item">
                <label>截止时间&nbsp;</label>
                <el-date-picker
                        size="mini"
                        value-format="yyyy-MM-dd"
                        v-model="search_end_date"
                        type="date">
                </el-date-picker>
            </div>
            <div class="item">
                <label>交易状态&nbsp;</label>
                <el-select v-model="mainForm.status" clearable size="mini">
                    <el-option
                            v-for="item in statusList"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="item">
                <label>导入状态&nbsp;</label>
                <el-select v-model="mainForm.is_imported" clearable size="mini">
                    <el-option label="已导入" value="1"></el-option>
                    <el-option label="未导入" value="0"></el-option>
                </el-select>
            </div>
        </div>
        <div class="btns" ref="btns">
            <el-button type="primary" size="mini" @click="searchOrder()" plain>查询</el-button>
            <el-button type="primary" size="mini" @click="showDownload = true" plain>订单下载</el-button>
            <el-button type="primary" size="mini" @click="resetStatus()" plain>状态重置</el-button>
            <el-button type="warning" size="mini" @click="importC8()" plain>订单导入</el-button>
            <el-button type="danger" size="mini" @click="deleteOrder()" plain>订单删除</el-button>
        </div>

        <div class="subTable">
            <el-table
                    @selection-change="handleSelectionChange"
                    ref="subTable"
                    size="mini"
                    border
                    :height="table_height"
                    :data="subTable"
                    :row-class-name="tableRowClassName"
                    empty-text="-"
                    tooltip-effect="dark"
                    style="width: 100%">
                <el-table-column
                        fixed
                        type="selection"
                        width="55">
                </el-table-column>
                <el-table-column type="expand" fixed>
                    <template slot-scope="{row}">
                        <span class="err" v-if="!row.products.items.length">无商品明细</span>
                        <table class="table-inline" v-else>
                            <thead>
                            <tr>
                                <th>商品名称</th>
                                <th>产品码</th>
                                <th>商品数量</th>
                                <th>交易金额</th>
                                <th>商品成本</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="pro in row.products.items">
                                <td>{{pro.name}}</td>
                                <td class="t-center">{{pro.barcode}}</td>
                                <td class="t-right">{{pro.num}}</td>
                                <td class="t-right">{{pro.amount}}</td>
                                <td class="t-right">{{pro.cost}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </template>
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="retail_code"
                        label="零售单单号"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="trans_id"
                        label="交易号"
                        width="200">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        align="center"
                        prop="e_id"
                        label="用户ID"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="dev_id"
                        label="设备ID"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        align="right"
                        prop="total_amount"
                        label="订单总金额"
                        width="120">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        align="center"
                        prop="status_name"
                        label="订单状态"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="create_time"
                        label="订单创建时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="update_time"
                        label="最终更新时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="created_at"
                        label="订单下载时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="created_user"
                        label="下载用户"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="is_imported"
                        label="是否已导入"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="imported_at"
                        label="导入时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="imported_user"
                        label="导入用户"
                        width="120">
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
                    :total="totalSubTable">
            </el-pagination>
        </div>

        <!--下载弹窗-->
        <el-dialog title="订单下载" :visible.sync="showDownload" width="70%" class="downLoadDialog">
            <el-form :model="downloadForm" label-width="100px">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="设备ID号">
                            <el-input v-model.trim="downloadForm.dev_id"
                                      placeholder="设备ID号" clearable size="mini"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="交易ID">
                            <el-input v-model.trim="downloadForm.trans_id"
                                      placeholder="交易ID" clearable size="mini"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="开始时间">
                            <el-date-picker
                                    style="width: 100%;"
                                    size="mini"
                                    value-format="yyyy-MM-dd HH:mm:ss"
                                    v-model="downloadForm.start_date"
                                    type="datetime">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="截止时间">
                            <el-date-picker
                                    style="width: 100%;"
                                    size="mini"
                                    value-format="yyyy-MM-dd HH:mm:ss"
                                    v-model="down_end_date"
                                    type="datetime">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="交易状态">
                            <el-select v-model="downloadForm.status" clearable size="mini">
                                <el-option
                                        v-for="item in statusList"
                                        :label="item.label"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showDownload = false">取 消</el-button>
                <el-button type="primary" @click="startDownload()">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
  name: "bills",
  data() {
    return {
      table_height: 500,
      totalSubTable: 0,
      default_limit: 50,
      new_start: 0,
      mainForm: {
        dev_id: "",
        trans_id: "",
        status: "",
        start_date: "",
        end_date: "",
        is_imported: "",
        start: "",
        limit: ""
      },
      statusList: [
        {
          label: "支付成功",
          value: "100"
        },
        {
          label: "等待支付",
          value: "101"
        },
        {
          label: "等待退款",
          value: "102"
        },
        {
          label: "退款成功",
          value: "103"
        },
        {
          label: "退款失败",
          value: "104"
        },
        {
          label: "交易关闭",
          value: "105"
        },
        {
          label: "支付失败",
          value: "107"
        },
        {
          label: "交易异常",
          value: "109"
        },
        {
          label: "重新退款",
          value: "110"
        }
      ],
      subTable: [],
      multipleSelection: [], // 多选 选中的行
      currentPage: 1,
      id_arr: [],
      showDownload: false,
      down_end_date: "",
      search_end_date: "",
      fail_id_arr: [],
      downloadForm: {
        dev_id: "",
        trans_id: "",
        start_date: "",
        end_date: "",
        status: "100"
      }
    };
  },
  mounted() {
    this.setDefaultDate();
    this.searchOrder();
    this.$nextTick(() => {
      let autoHeight =
        document.documentElement.clientHeight -
        this.$refs.btns.offsetHeight -
        this.$refs.mainForm.offsetHeight -
        this.$refs.pagination.offsetHeight -
        64;
      this.table_height = autoHeight;
    });
  },
  methods: {
      tableRowClassName({row, rowIndex}) {
          if (this.fail_id_arr.includes(row.id)) {
              return 'warning-row';
          }
          return '';
      },
      setDefaultDate() {
      // 本月1号至今
      let myDate = new Date();
      let year = myDate.getFullYear();
      let month = myDate.getMonth() + 1;
      let date = myDate.getDate() + 1;
      let sTime = `${year}-${month}-${date - 1}`;
      this.mainForm.start_date = `${year}-${month}-1`;
      this.downloadForm.start_date = sTime + ' 00:00:00';
      // 展示在界面上的截止日期
      this.down_end_date = `${year}-${month}-${date - 1} 00:00:00`;
      this.search_end_date = `${year}-${month}-${date - 1}`;
    },
    startDownload() {
      this.showDownload = false;
      this.downloadOrder();
    },
    handleSizeChange(val) {
      this.default_limit = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val || this.currentPage;
      this.new_start = (this.currentPage - 1) * this.default_limit;
      this.searchOrder(false);
    },
    handleSelectionChange(val) {
      // 多选
      this.multipleSelection = val;
    },
    getSelectedID() {
      if (!this.multipleSelection.length) {
        alert("请至少选中一行");
        return false;
      }
      this.id_arr = [];
      this.multipleSelection.forEach(val => {
        this.id_arr.push(val.id);
      });
      return true;
    },
    downloadOrder(page = 1) {
      let params = JSON.parse(JSON.stringify(this.downloadForm));
      params.page = page;
      params.per_page = 50;
      params.end_date = this.down_end_date
      if (!this.checkDateDuration(params.start_date, this.down_end_date))
        return;
      this.$axios({
        url: `/api/orders?action=get_orders`,
        params: params
      }).then(res => {
        if (res.state === 1) {
          if (res.page) {
            this.downloadOrder(page++);
          }
          if (res.page == null) {
            this.$notify({
              title: "下载列表完成",
              type: "success"
            });
          }
          return;
        }
        alert(res.errmsg);
      });
    },
    deleteOrder() {
      // 删除
      this.ajaxFunction(null, "DELETE", "删除订单", "/api/orders/");
    },
    resetStatus() {
      // 状态重置
      this.ajaxFunction("init_order", "GET", "重置状态");
    },
    importC8() {
      // 导入c8
      this.ajaxFunction("import", "GET", "导入C8");
    },
    async ajaxFunction(action, method, text, url = "") {
      if (!this.getSelectedID()) return;
      let count_failed = 0;
      let count_succeed = 0;
      let _total = 0;
      this.fail_id_arr = [];
      for await (let id of this.id_arr) {
        this.$axios({
          method: method,
          url: url ? url + id : `/api/orders/${id}?action=${action}`
        })
          .then(res => {
            if (res.state === 1) {
              count_succeed++;
              return;
            }
            count_failed++;
            this.fail_id_arr.push(id)
            for (let j = 0, len2 = this.subTable.length; j <len2; j++) { // 错误单子设置Title
              if (this.subTable[j].id === id) {
                document.getElementsByClassName('el-table__row')[j].setAttribute('title', res.errmsg)
              }
            }
          })
          .finally(() => {
            _total++;
            if (_total === this.id_arr.length) {
              alert(
                `共${this.id_arr.length}条，成功${text}${count_succeed}条，失败${count_failed}条`
              );
            }
          });
      }
      await this.handleCurrentChange(1);
      this.multipleSelection = [];
    },
    addDate(end_date) {
          var _end_date = new Date(end_date);
          var millSeconds = Math.abs(_end_date) + 24 * 60 * 60 * 1000;
          var added = new Date(millSeconds);
          let year = added.getFullYear();
          let month = added.getMonth() + 1;
          let date = added.getDate();
          let eTime = `${year}-${month}-${date}`;
          return eTime;
    },
    checkDateDuration(start, end) {
      if (!start || !end) {
        alert("请选择查询日期，范围不能超过7天");
        return false;
      }
      if (
        (new Date(end + " 00:00:00") - new Date(start + " 00:00:00")) /
          (1000 * 60 * 60 * 24) >=
        7
      ) {
        alert("所选日期范围不能超过7天");
        return false;
      }
      return true;
    },
    searchOrder(bool = true) {
      // 查询订单
      this.mainForm.limit = this.default_limit;
      this.mainForm.start = this.new_start;
      let params = JSON.parse(JSON.stringify(this.mainForm));
      params.end_date = this.search_end_date? this.addDate(this.search_end_date) : "";
      if (Date.parse(params.end_date) - Date.parse(params.start_date) < 0) {
        // end不选择时 会变为1970-1-1
        alert("请选择正确的截止时间");
        return;
      }
      this.$axios({
        url: "/api/orders?action=trade_view",
        params: params
      }).then(res => {
        if (res.state === 1) {
          this.totalSubTable = Number(res.total);
          res.root.forEach(val => {
            for (let keyName in val) {
              val[keyName] = val[keyName] == null ? "" : val[keyName];
              if (typeof val[keyName] === "boolean") {
                val[keyName] = val[keyName] == true ? "是" : "否";
              }
              if (keyName === "status") {
                for (let i in this.statusList) {
                  if (val[keyName] == this.statusList[i].value) {
                    val.status_name = this.statusList[i].label;
                  }
                }
              }
            }
          });
          this.subTable = res.root;
          return;
        }
        alert(res.errmsg);
      });
      if (bool) { // 点击查询时 清空错误信息
          this.fail_id_arr = []
          for (let j = 0, len2 = this.subTable.length; j < len2; j++) {
              document.getElementsByClassName('el-table__row')[j].setAttribute('title','')
          }
      }
    }
  }
};
</script>

<style scoped lang="less">
#bill,
.mainForm {
  overflow: hidden;
}

.mainForm {
  .item {
    float: left;
    overflow: hidden;
    width: 300px;
    margin: 2px 0;
    label {
      width: 100px;
      text-align: right;
      display: inline-block;
    }
    .el-input,
    .el-select {
      width: 200px;
    }
  }
}

.btns {
  width: 100%;
  margin: 4px 0;
  padding: 0 10px;
}

.subTable {
  .table-inline {
    width: 50%;
    margin-left: 43px;
    padding-left: 8px;
    background-color: #409eff;
    text-align: center;
    th {
      text-align: center;
    }
    th:first-child {
      width: 40%;
    }
    .t-right {
      text-align: right;
    }
    .t-center {
      text-align: center;
    }
  }
  .err {
    color: red;
  }
  .el-table--mini td,
  .el-table--mini th {
    padding: 4px 0;
  }
}

.downLoadDialog {
  .el-form-item {
    margin-bottom: 0;
  }
}
</style>
