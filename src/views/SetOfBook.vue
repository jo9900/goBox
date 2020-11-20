<template>
    <div id="set_of_books">
        <el-table
                border
                :data="tableData"
                style="width: 100%">
            <el-table-column
                    align="center"
                    prop="id"
                    label="账套">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="set_of_book"
                    label="账套号">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="app_key"
                    label="密钥">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="user_name"
                    label="用户名">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="access_token"
                    label="令牌">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="token_created_at"
                    label="令牌获取时间">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="expired_at"
                    label="令牌过期时间">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="token"
                    label="本地令牌">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="updated_at"
                    label="更新时间">
            </el-table-column>
            <el-table-column
                    align="center"
                    prop="updated_user"
                    label="更新用户">
            </el-table-column>
            <el-table-column label="操作" align="center">

                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="handleEdit(scope.$index, scope.row)">编辑
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog
                title="编辑店铺"
                :visible.sync="dialogVisible"
                width="50%">
            <el-form ref="form" :model="postData" label-width="120px" size="mini">
                <el-form-item label="CRM令牌">
                    <el-input v-model.trim="postData.user_token"></el-input>
                </el-form-item>
                <el-form-item label="默认仓库">
                    <el-select v-model="postData.default_store_id" placeholder="请选择默认仓库">
                        <el-option
                                v-for="store in storeList"
                                :label="store.name"
                                :value="store.id"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="默认发票类型">
                    <el-select v-model="postData.default_bill_type" placeholder="请选择默认发票类型">
                        <el-option
                                v-for="bill_type in bill_type_list"
                                :label="bill_type.name"
                                :value="bill_type.val"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
            <el-button @click="resetForm()">取 消</el-button>
            <el-button type="primary" @click="submitForm()">确 定</el-button>
  </span>
        </el-dialog>
    </div>
</template>

<script>
  export default {
    name: "set_of_books",
    data() {
      return {
        storeList: [],
        dialogVisible: false,
        postData: {
            app_key: "",
            user_name: ""
        },
        tableData: [],
        bill_type_list: [
          {
            name: "收据",
            val: 0
          },{
            name: "发票",
            val: 1
          },{
            name: "增值税发票",
            val: 2
          },
        ],
        rowIndex: 0
      }
    },
    mounted() {
      this.getSetOfBookDate()
    },
    methods: {
      resetForm() {
        for(let key in this.postData) {
          this.postData[key] = ""
        }
        this.dialogVisible = false
      },
      submitForm() {
        let id = this.tableData[this.rowIndex].id
        this.$axios({
          url: "/api/set_of_books/" + id,
          method: "PUT",
          data: this.postData
        }).then(res => {
          if ( res.state === 1 ) {
            this.dialogVisible = false
            this.getSetOfBookDate()
            this.$message({
              message: '更新成功',
              type: 'success'
            });
            return
          }
          alert(res.errmsg)
        })
      },
      handleEdit(index, row) {
        this.rowIndex = index
        this.dialogVisible = true
      },
      getSetOfBookDate() { // 获取账套信息
        let infoData = this.$root.$data.infoData
        this.tableData = []
        this.$axios({
          url: '/api/set_of_books',
          params: {
            set_of_book: infoData.user.set_of_book
          }
        }).then(res => {
          this.tableData.push(res)
        })
      }
    }
  }
</script>

<style scoped lang="less">
</style>
