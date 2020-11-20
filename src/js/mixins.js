const Mixins = {
  data() {
    return {
      newToken: ""
    };
  },
  watch: {},
  mounted() {
    this.$nextTick(() => {});
  },
  methods: {
    getToken(infoData) {
      let referrerUrl = document.referrer;
      let url = referrerUrl.slice(0, referrerUrl.indexOf("/static"));
      let userInfo = infoData.user;
      this.$axios({
        url: "/api/access_token",
        params: {
          url: url,
          set_of_book: userInfo.set_of_book,
          user_name: userInfo.name
        },
        headers: {
          Token: userInfo.token
        }
      })
        .then(res => {
          if (res.data.state === 1) this.newToken = res.data.token;
          else alert(res.data.errmsg);
        })
        .catch(err => {
          console.log("err", err);
        });
    }
  }
};

export default Mixins;
