<template>
  <div>
    <el-button @click="dialogFormVisible = true" style="margin-left: 85%;margin-top: 2%" type="primary"
               size="large" plain>
      <el-icon>
        <Edit/>
      </el-icon>
      New Post
    </el-button>
    <div class="block">
      <el-timeline>
        <template v-if="itemKey === 0">
          <el-timeline-item :timestamp="blog.PostDate" placement="top" v-for="blog in blogs">
            <el-card>
              <router-link :to="'bulletin/singlePage/'+blog.PId">
                <p class="text-xl font-extrabold">{{ blog.Title }}</p>
              </router-link>
              <p style="color: #888888">author: {{ blog.Poster }}</p>
              <p style="color: #888888">date: {{ blog.PostDate }}</p>
              <p style="color: #888888">type: {{ blog.Type }}</p>
              <!--            <p>{{ blog.description }}</p>-->
            </el-card>
          </el-timeline-item>
          <p>{{ blogs.value }}</p>
        </template>
        <template v-if="itemKey === 1">
          <el-timeline-item :timestamp="blog.PostDate" placement="top" v-for="blog in blogs">
            <el-card>
              <router-link :to="'bulletin/singlePage/'+blog.PId">
                <p class="text-xl font-extrabold">{{ blog.Title }}</p>
              </router-link>
              <p style="color: #888888">author: {{ blog.Poster }}</p>
              <p style="color: #888888">date: {{ blog.PostDate }}</p>
              <p style="color: #888888">type: {{ blog.Type }}</p>
              <!--            <p>{{ blog.description }}</p>-->
            </el-card>
          </el-timeline-item>
          <p>{{ blogs.value }}</p>
        </template>

      </el-timeline>
    </div>
    <el-pagination class="mpage"
                   background
                   layout="prev, pager, next"
                   v-model:current-page="currentPageNum"
                   :page-size="pageArticleSize"
                   :total="totalPageNum"
                   @current-change="changePage"
    >
    </el-pagination>
  </div>

  <el-dialog width="90%" v-model="dialogFormVisible" title="EDIT PASSAGE">
    <el-form :model="tableForm">
      <el-form-item label="title" :label-width="60">
        <el-input v-model="tableForm.Title"/>
      </el-form-item>
      <el-form-item label="author" :label-width="60">
        <el-input v-model="tableForm.Poster" disabled/>
      </el-form-item>
      <el-form-item label="type" :label-width="60">
        <el-input v-model="tableForm.Type"/>
      </el-form-item>
      <el-form-item label="content" :label-width="60">
        <div class="editor">
          <v-md-editor
              :placeholder="placeholder"
              :disabled-menus="[]"
              v-model="tableForm.Content"
              :height="height"
              :width="width"
              @change="handleChange"></v-md-editor>
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="dialogConfirm">Confirm</el-button>
        </span>
    </template>
  </el-dialog>
</template>

<script lang='ts' setup>
import {useRouter} from "vue-router";
import {computed, ref} from "vue";
import {getToken} from "../../../composable/auth";
import {NOTATION} from "../../../composable/utils";
import {getSinglePage} from "../../../api/posts";
import {newPost, getCurrentPage} from "../../../api/posts";
import store from "../../../store/index.js";

const currentPageNum = ref(1)
let blogs = ref(store.state['passageList'])
let pageArticleSize = 5
const totalPageNum = ref(store.state['totalPageNum'] * pageArticleSize)
let itemKey = ref(0)
console.log("currentPageNum", currentPageNum.value)
console.log("totalPageNum", totalPageNum)

const changePage = (val: number) => {
  console.log("changePage ", currentPageNum.value, val)
  getCurrentPage(getToken(), val)
      .then(res => {
        console.log("getCurrentPage ", res)

        if (res.status !== 200) {
          if ("details" in res.data) {
            NOTATION(0, res.data.details)
          } else {
            NOTATION(0, "ops~! other error")
          }
        } else {
          // message
          NOTATION(1, "success")
          totalPageNum.value = res.data['totalPage'] * pageArticleSize
          blogs.value = res.data['pageObj']
          currentPageNum.value = val
          itemKey.value = 1 - itemKey.value
        }
      })
      .catch(err => {
        console.log("getCurrentPage err ", err)
        NOTATION(0, err.detail)
      })
}


let dialogFormVisible = ref(false)
let tableForm = ref({
  //PId: '',
  Title: '',
  Poster: '',
  //PostDate: '',
  Content: '',
  LastEditor: '',
  //LastEditTime: '',
  Type: ''
})
tableForm.value.Poster = store.state.user['CodeName']
tableForm.value.LastEditor = store.state.user['CodeName']

interface Props {
  modelValue: string
  height?: string // ??????????????????
  width?: string // ??????????????????
  placeholder?: string
}

interface EmitEvent {
  (e: 'update:modelValue', params: string): void
}

const props = withDefaults(defineProps<Props>(), {
  height: '700px',
  width: '500px',
  placeholder: '???????????????'
})

const emit = defineEmits<EmitEvent>()

const newValue = computed({
  get() {
    return props.modelValue
  },
  set(value: string) {
    emit('update:modelValue', value)
  }
})

// ?????????????????????????????????text ?????????????????????html ?????????????????? html ????????????
const handleChange = (text: string, html: string) => {
  // console.log(JSON.stringify(text))
  console.log(html)
  // ???????????????????????????????????????????????????
}

const dialogConfirm = () => {
  newPost(getToken(), tableForm)
      .then(res => {
        console.log("newPost ", res)
        console.log("newPost ", tableForm)

        if (res.status !== 201) {
          if ("details" in res.data) {
            NOTATION(0, res.data.details)
          } else {
            NOTATION(0, "ops~! other error")
          }
        } else {
          // message
          NOTATION(1, res.data)
        }
      })
      .catch(err => {
        console.log("newPost err ", err)
        NOTATION(0, err.detail)
      })
}

</script>

<style scoped>
.block {
  margin-left: 5%;
  margin-right: 5%;
}

.mpage {
  margin-bottom: 4%;
  text-align: center;
  margin-left: 5%;
}


.editor {
  flex: auto;
  align-content: center;
}
</style>