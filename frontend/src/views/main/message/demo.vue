<template>

  <div class="talk" v-show="flag">

      <div class="talk-header">
          <div class="talk-header-icon">
              <svg class="icon" aria-hidden="true">
                  <use xlink:href="#icon-gengduocaozuo"></use>
              </svg>
              <svg class="icon" aria-hidden="true" @click="exit">
                  <use xlink:href="#icon-guanbi"></use>
              </svg>
          </div>
      </div>

      <div class="talk-content ">
          <div v-for="item  in contentDiv" style="margin-top: 20px">
              <div style="text-align: center">
                  <p style="font-size: 1px;color: #9b9b9b"> {{item.time}}</p>
              </div>
              <div style="display: flex;">
                  <div class="name_right" v-if="item.show">
                      <p style="font-size: 1px; "> {{item.name}} </p>
                  </div>
                  <div class="url_right" v-if="item.show">
                      <el-avatar shape="circle" :size="30" :src="item.url"></el-avatar>
                  </div>
                  <div class="url_left" v-if="!item.show">
                      <el-avatar shape="circle" :size="30" :src="item.url"></el-avatar>
                  </div>
                  <div class="name_left" v-if="!item.show">
                      <p style="font-size: 1px;"> {{item.name}} </p>
                  </div>
              </div>
              <div v-html="item.content" class="content_left" v-if="!item.show"></div>
              <div v-html="item.content" class="content_right" v-if="item.show"></div>
          </div>
      </div>


      <div class="talk-message">
          <div class="talk-message-face">
              <svg class="icon" aria-hidden="true" @click="isShow">
                  <use xlink:href="#icon-biaoqing"></use>
              </svg>
              <emotion :emotionIsShow="emotionIsShow" @sendEmotionSelect="getValue"></emotion>
          </div>
          <div class="talk-message-content">
              <el-input
                      v-model="textarea"
                      resize="none"
                      type="textarea"
                      rows="1"
                      @keyup.enter.native="submit"
              ></el-input>
          </div>
          <div class="flex-grow"></div>
          <div class="talk-message-send">
              <el-button type="primary" round @click="submit">??????</el-button>
          </div>
      </div>

  </div>
</template>

<script>
  import emotion from "../../../components/emotion.vue";
  import "../../../styles/talk.css";
  import '../../../assets/iconfont';

  export default {

      components: {
          emotion
      },


      data() {
          return {
              url: "https:/rescdn.qqmail.com/node/wwopen/wwopenmng/images/qq_emotion/qq/",
              eList: ['??????', '??????', '??????', '???', '??????', '??????', '??????', '??????', '??????', '???', '??????',
                  '??????', '??????', '??????', '??????', '??????', '??????', '???', '??????', '??????', '???', '??????', '??????',
                  '??????', '??????', '??????', '???', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '???',
                  '???', '??????', '???', '??????', '??????', '??????', '??????', '??????', '??????', '?????????', '??????', '?????????',
                  '?????????', '??????', '??????', '??????', '?????????', '??????', '??????', '???', '??????', '??????', '??????', '??????',
                  '??????', '??????', '??????', '???', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????',
                  '???', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '???', '???', '??????', '??????', '??????', '??????',
                  '??????', '??????', '??????', 'NO', 'OK', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????',
                  '??????', '??????', '??????', '?????????', '?????????'],
              contentDiv: [],
              textarea: "",
              textarea1: "",
              emotionIsShow: false, // ????????????????????????
              divIptEmotion: [], // ????????????????????????????????????
              a: [],
              flag: true,
              show: true,
              closeChat: this.close
          }
      },
      created() {
      },
      mounted() {
          this.scrollToBottom()
      },
      updated() {
          this.scrollToBottom()
      },
      methods: {
          scrollToBottom() {
              this.$nextTick(() => {
                  let box = this.$el.querySelector(".talk-content")
                  box.scrollTop = box.scrollHeight
              })
          },
          sendInfo() {
              alert("aaa")
          },
          isShow() {
              if (this.emotionIsShow === false) {
                  this.emotionIsShow = true;
              } else {
                  this.emotionIsShow = false;
              }
              // this.emotionIsShow = !this.emotionIsShow;
          },
          iptFocus() {
              this.emotionIsShow = true;
          },
          getValue(val, item) {
              let img = '<img src="' + this.url + val + '.png"  style= "width: 22px;height: 22px">';
              let el = '[' + item + ']'
              this.emotionIsShow = false;
              this.textarea = this.textarea + el;
              this.textarea1 += img;
          },
          submit() {
              let a = this.textarea;
              let pre = 0;
              let last = 0;
              let flag = false;
              while (true) {
                  if (!a.match("]")) {
                      break;
                  }
                  pre = a.indexOf("[");
                  last = a.indexOf("]");

                  let face = a.substring(pre + 1, last);
                  let b;
                  for (let j = 0; j < this.eList.length; j++) {
                      if (face == this.eList[j]) {
                          b = j;
                          break;
                      }
                  }
                  let img = '<img src="' + this.url + b + '.png"  style= "width: 22px;height: 22px">';
                  a = a.substring(0, pre) + img + a.substring(last + 1, a.length);
                  pre = 0;
                  last = 0;
                  flag = false;


              }

              let c = {
                  "name": "???",
                  "url": "https://img0.baidu.com/it/u=3953639057,245238928&fm=15&fmt=auto&gp=0.jpg",
                  "content": a,
                  "show": true,
                  "time": "2021-7-12 17:12:12"
              };

              let d = {
                  "name": "??????1",
                  "url": "https://img0.baidu.com/it/u=1741172190,3962404342&fm=26&fmt=auto&gp=0.jpg",
                  "content": "????????????",
                  "show": false,
                  "time": "2021-7-12 17:12:46"
              };

              this.textarea = "";
              this.textarea1 = "";
              this.contentDiv.push(c);
              this.contentDiv.push(d);
          },

          exit() {
             this.$emit('close',this.fleg)
          }

      }

  }
</script>


<style scoped>

</style>