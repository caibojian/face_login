<template>
  <div class="page">
    <div class="page__hd">
      <h1 class="page__title">人脸识别系统</h1>
      <p class="page__desc">v1.0.0</p>
    </div>
    <div class="page__bd">
      <div>
        <div class="weui-toptips weui-toptips_warn js_tooltips">错误提示</div>
        <!--人脸识别start-->
        <div v-if="showVideo" align="center">
          <video class="video_class" id="video" ref="video"></video>
          <canvas hidden="true" id="canvas" width="200" height="200" ref="canvas"></canvas>
        </div>
        <div v-if="showProgress" class="weui-progress" style="margin:10px">
          <div class="weui-progress__bar">
            <div class="weui-progress__inner-bar js_progress" :style="progress"></div>
          </div>
        </div>
        <div class="weui-cells" v-if="isRegister">
          <div class="weui-cell">
            <div class="weui-cell__bd">
              <input
                class="weui-input"
                ref="username"
                v-model="username"
                name="username"
                type="text"
                tabindex="1"
                auto-complete="on"
                placeholder="输入注册名称"
              >
            </div>
          </div>
        </div>
        <div style="margin-top:20px;padding:10px">
          <a v-if="showVideo&&!isRegister" class="weui-btn weui-btn_primary" v-on:click="login">验证</a>
          <a v-if="isRegister" class="weui-btn weui-btn_primary" v-on:click="register">注册</a>
          <a class="weui-btn weui-btn_primary" v-if="showVideo" v-on:click="closeCamera">关闭视频</a>
        </div>
        <div class="weui-flex">
          <div class="weui-flex__item">
            <div class="placeholder" style="padding:5px">
              <a v-if="!showVideo" class="weui-btn weui-btn_primary" v-on:click="startFace">人脸识别</a>
            </div>
          </div>
          <div class="weui-flex__item">
            <div class="placeholder" style="padding:5px">
              <a v-if="!showVideo" class="weui-btn weui-btn_primary" v-on:click="registerView">人脸注册</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="loadingToast" class v-if="loading">
      <div class="weui-mask_transparent mask"></div>
      <div class="weui-toast">
        <i class="weui-loading weui-icon_toast"></i>
        <p class="weui-toast__content">数据加载中</p>
      </div>
    </div>

    <!--BEGIN dialog2-->
    <div class="js_dialog" id="iosDialog2" v-if="showDilog">
      <div class="weui-mask"></div>
      <div class="weui-dialog">
        <div class="weui-dialog__bd">{{dialogMsg}}</div>
        <div class="weui-dialog__ft">
          <a
            href="javascript:;"
            class="weui-dialog__btn weui-dialog__btn_primary"
            v-on:click="closeDialog"
          >知道了</a>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { registerFace } from "@/api/user";
export default {
  name: "Login",
  data() {
    return {
      loading: false,
      redirect: undefined,
      showVideo: false,
      showProgress: false,
      imgDatas: [],
      repeat: 0,
      progress: "",
      mediaStreamTrack: null,
      isRegister: false,
      username: "",
      panel_loading: false,
      dialogMsg: "",
      showDilog: false
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
  methods: {
    //访问用户媒体设备的兼容方法
    getUserMedia: function(constraints, success, error) {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        this.msg = "1";
        //最新的标准API
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(success)
          .catch(error);
      } else if (navigator.webkitGetUserMedia) {
        this.msg = "2";
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints, success, error);
      } else if (navigator.mozGetUserMedia) {
        this.msg = "3";
        //firfox浏览器
        navigator.mozGetUserMedia(constraints, success, error);
      } else if (navigator.getUserMedia) {
        this.msg = "4";
        //旧版API
        navigator.getUserMedia(constraints, success, error);
      }
    },
    success: function(stream) {
      this.video_buffer = stream;
      //兼容webkit核心浏览器
      let CompatibleURL = window.URL || window.webkitURL;
      //将视频流设置为video元素的源
      // this.$refs.video.src = CompatibleURL.createObjectURL(stream);
      this.$refs.video.srcObject = stream;
      this.$refs.video.play();
      this.loading = false;
    },
    error: function(error) {
      this.loading = false;
      console.error(`访问用户媒体设备失败${error.name}, ${error.message}`);
      this.showDilog = true;
      this.dialogMsg = "访问用户媒体设备失败";
    },
    closeCamera: function() {
      if (this.video_buffer) {
        console.log(this.video_buffer.getTracks());
        if (this.showProgress) {
          return;
        }
        this.isRegister = false;
        this.showVideo = false;
        this.video_buffer && this.video_buffer.getTracks()[0].stop(); //关闭摄像头
      }
    },
    registerView() {
      this.isRegister = true;
      this.startFace();
    },
    register() {
      var that = this;
      if (this.showProgress) {
        return;
      }
      if (!this.username) {
        that.showDilog = true;
        that.dialogMsg = "用户名不能为空，请输入用户名。";
        return;
      }
      that.showProgress = true;
      that.imgDatas = [];
      that.repeat = 0;
      that.progress = "width: 0%;";
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

      registerFace({
        imgData: this.imgDatas,
        username: this.username
      })
        .then(res => {
          if (!res.success) {
            that.showDilog = true;
            that.dialogMsg = res.msg;
          }
          this.loading = false;
          this.showProgress = false;
          this.isRegister = false;
        })
        .catch(() => {
          this.loading = false;
          this.showProgress = false;
        });
    },
    startFace() {
      var that = this;
      console.log(navigator.mediaDevices);
      console.log(navigator.getUserMedia);
      console.log(navigator.webkitGetUserMedia);
      console.log(navigator.mozGetUserMedia);
      if (
        (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) ||
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia
      ) {
        this.loading = true;
        //调用用户媒体设备, 访问摄像头
        that.getUserMedia(
          {
            video: { width: 300, height: 300, facingMode: "user" } //调用前置摄像头，后置摄像头使用video: { facingMode: { exact: "environment" } }
          },
          that.success,
          that.error
        );
      } else {
        this.loading = false;
        console.error("不支持访问用户媒体");
        this.showDilog = true;
        this.dialogMsg = "不支持访问用户媒体";
      }
      that.showVideo = true;
    },
    getPic() {
      var that = this;
      that.repeat++;
      that.progress = "width: " + that.repeat * 20 + "%;";
      let canvas = that.$refs.canvas;
      let context = canvas.getContext("2d");
      canvas.width = 300;
      canvas.height = 300;
      context.drawImage(that.$refs.video, 0, 0, 300, 300);
      var imgData = canvas.toDataURL();
      that.imgDatas.push(imgData);
    },
    login() {
      var that = this;
      if (this.showProgress) {
        return;
      }
      that.showProgress = true;
      that.imgDatas = [];
      that.repeat = 0;
      that.progress = "width: 0%;";
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
      this.$store
        .dispatch("user/facelogin", {
          imgData: this.imgDatas
        })
        .then(() => {
          console.log(this.$store.getters.token);
          this.showProgress = false;
          that.closeCamera();
          if (this.$store.getters.token) {
            this.$router.push({ path: this.redirect || "/" });
          } else {
            that.showDilog = true;
            that.dialogMsg = "验证失败，请重试！";
          }
          this.loading = false;
        })
        .catch(() => {
          that.closeCamera();
          this.loading = false;
          this.showProgress = false;
        });
    },
    closeDialog() {
      this.showDilog = false;
    }
  }
};
</script>
<style>
.video_class {
  border-radius: 50%;
  width: 300;
  height: 300;
  border: 2px solid #e4007e;
}

.mask {
  background: rgba(17, 17, 17, 0.7);
}
</style>
