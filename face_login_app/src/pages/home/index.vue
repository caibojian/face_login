<template>
  <div class="page">
    <div class="weui-msg">
      <div class="weui-msg__icon-area">
        <i class="weui-icon-success weui-icon_msg"></i>
      </div>
      <div class="weui-msg__text-area">
        <h2 class="weui-msg__title">操作成功</h2>
        <p class="weui-msg__desc">
          欢迎
          <b>{{username}}</b>
          登陆
        </p>
      </div>
      <div class="weui-msg__opr-area">
        <p class="weui-btn-area">
          <a class="weui-btn weui-btn_default" v-on:click="logout">退出系统</a>
        </p>
      </div>
      <div class="weui-msg__extra-area">
        <div class="weui-footer">
          <p class="weui-footer__links">
            <a href="javascript:void(0);" class="weui-footer__link">底部链接文本</a>
          </p>
          <p class="weui-footer__text">Copyright &copy; 2008-2016 weui.io</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { getInfo } from "@/api/user";
export default {
  name: "home",
  data() {
    return {
      username: ""
    };
  },
  methods: {
    getUserInfo() {
      getInfo().then(res => {
        console.log(res);
        this.username = res.data.name;
      });
    },
    logout() {
      this.$store
        .dispatch("user/logout", {
          imgData: this.imgDatas
        })
        .then(() => {
          location.reload();
        })
        .catch(() => {});
    }
  },
  mounted() {
    this.getUserInfo();
  },
  created() {},
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  }
};
</script>
