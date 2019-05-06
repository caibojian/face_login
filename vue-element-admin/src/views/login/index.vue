<template>
  <div class="login-container">
    <el-form ref="loginForm" class="login-form" auto-complete="on" label-position="left">
      <div class="title-container">
        <h3 class="title">{{ $t('login.title') }}</h3>
        <lang-select class="set-language"/>
      </div>
      <!--人脸识别start-->
      <div v-if="showVideo" v-loading="panel_loading">
        <el-card :body-style="{ padding: '0px' }">
          <video id="video" width="100%" height="100%" ref="video"></video>
          <div>
            <el-row v-if="showProgress">
              <el-col :span="24">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="repeat*20"
                  color="rgba(142, 113, 199, 0.7)"
                ></el-progress>
              </el-col>
            </el-row>
            <el-row v-if="!isRegister">
              <el-col :span="24">
                <el-button
                  :loading="loading"
                  type="primary"
                  style="width:100%;margin-bottom:10px;margin-top:10px;"
                  @click.native.prevent="login"
                >{{ $t('login.logIn') }}</el-button>
              </el-col>
            </el-row>
          </div>
        </el-card>
        <canvas hidden="true" id="canvas" width="450" height="300" ref="canvas"></canvas>
      </div>
      <!--人脸识别start-->
      <el-form-item prop="username" v-if="isRegister" style="margin-top:10px;">
        <span class="svg-container">
          <svg-icon icon-class="user"/>
        </span>
        <el-input
          ref="username"
          v-model="username"
          :placeholder="$t('login.username')"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-button
        v-if="isRegister"
        type="primary"
        style="width:100%;margin-bottom:10px;"
        @click.native.prevent="register"
      >开始注册</el-button>
      <el-button
        v-if="!showVideo"
        type="primary"
        style="margin-bottom:10px;"
        @click.native.prevent="startFace"
      >人脸识别登陆</el-button>
      <el-button
        :loading="loading"
        v-if="!showVideo"
        type="primary"
        style="margin-bottom:10px;"
        @click.native.prevent="registerView"
      >人脸注册</el-button>
    </el-form>

    <el-dialog :title="$t('login.thirdparty')" :visible.sync="showDialog">
      {{ $t('login.thirdpartyTips') }}
      <br>
      <br>
      <br>
      <social-sign/>
    </el-dialog>
  </div>
</template>

<script>
import { validUsername } from "@/utils/validate";
import LangSelect from "@/components/LangSelect";
import SocialSign from "./components/SocialSignin";
import { registerFace } from "@/api/user";
export default {
  name: "Login",
  components: { LangSelect, SocialSign },
  data() {
    return {
      loading: false,
      showDialog: false,
      redirect: undefined,
      showVideo: false,
      showProgress: false,
      imgDatas: [],
      repeat: 0,
      mediaStreamTrack: null,
      isRegister: false,
      username: "",
      panel_loading: false
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {},
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  },
  methods: {
    registerView() {
      this.isRegister = true;
      this.startFace();
    },
    register() {
      var that = this;
      that.showProgress = true;
      that.imgDatas = [];
      that.repeat = 0;
      var timer = setInterval(function() {
        that.getPic();
        if (that.repeat == 5) {
          clearInterval(timer);
          that.headRegister();
        }
      }, 500);
    },
    headRegister() {
      var that = this;
      this.loading = true;
      this.panel_loading = true;
      registerFace({
        imgData: this.imgDatas,
        username: this.username
      })
        .then(res => {
          console.log(res);
          this.loading = false;
          this.panel_loading = false;
          this.isRegister = false;
        })
        .catch(() => {
          this.loading = false;
          this.panel_loading = false;
        });
    },
    startFace() {
      var that = this;
      if (
        navigator.mediaDevices.getUserMedia ||
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia
      ) {
        //调用用户媒体设备, 访问摄像头
        that.getUserMedia(
          { video: { width: 480, height: 320 } },
          that.success,
          that.error
        );
      } else {
        alert("不支持访问用户媒体");
      }
      that.showVideo = true;
    },
    getPic() {
      var that = this;
      that.repeat++;
      let canvas = that.$refs.canvas;
      let context = canvas.getContext("2d");
      canvas.width = 450;
      canvas.height = 300;
      context.drawImage(that.$refs.video, 0, 0, 450, 300);
      var imgData = canvas.toDataURL();
      that.imgDatas.push(imgData);
    },
    login() {
      var that = this;
      that.showProgress = true;
      that.imgDatas = [];
      that.repeat = 0;
      var timer = setInterval(function() {
        that.getPic();
        if (that.repeat == 5) {
          clearInterval(timer);
          that.handleLogin();
        }
      }, 500);
    },
    handleLogin() {
      var that = this;
      this.loading = true;
      this.panel_loading = true;
      this.$store
        .dispatch("user/facelogin", {
          imgData: this.imgDatas
        })
        .then(() => {
          this.$router.push({ path: this.redirect || "/" });
          this.loading = false;
          this.panel_loading = false;
        })
        .catch(() => {
          this.loading = false;
          this.panel_loading = false;
        });
    },
    //访问用户媒体设备的兼容方法
    getUserMedia: function(constraints, success, error) {
      if (navigator.mediaDevices.getUserMedia) {
        //最新的标准API
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(success)
          .catch(error);
      } else if (navigator.webkitGetUserMedia) {
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints, success, error);
      } else if (navigator.mozGetUserMedia) {
        //firfox浏览器
        navigator.mozGetUserMedia(constraints, success, error);
      } else if (navigator.getUserMedia) {
        //旧版API
        navigator.getUserMedia(constraints, success, error);
      }
    },
    success: function(stream) {
      //兼容webkit核心浏览器
      let CompatibleURL = window.URL || window.webkitURL;
      //将视频流设置为video元素的源
      console.log(stream);

      //video.src = CompatibleURL.createObjectURL(stream);
      this.mediaStreamTrack = stream;
      this.$refs.video.srcObject = stream;
      this.$refs.video.play();
    },
    error: function(error) {
      console.log(`访问用户媒体设备失败${error.name}, ${error.message}`);
    },
    openFullScreen() {
      this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
    }
  }
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    .set-language {
      color: #fff;
      position: absolute;
      top: 3px;
      font-size: 18px;
      right: 0px;
      cursor: pointer;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
