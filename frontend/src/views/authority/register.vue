<template>
  <div class="register">
    <span class="text-5xl"> -- REGISTER -- </span>
  </div>

  <div class="input-box">
    <el-form :model="form" label-width="120px">
      <el-form-item label="CodeName">
        <el-input v-model="form.CodeName" @blur="checkSyntax(form.CodeName)"/>
      </el-form-item>
      <el-form-item label="Password">
        <el-input v-model="form.Password" :show-password="true"/>
      </el-form-item>
      <el-form-item label="Password again">
        <el-input v-model="form.PwConfirm" :show-password="true"/>
      </el-form-item>
      <el-form-item label="Class">
        <el-select v-model="form.Class" placeholder="please select your class">
          <el-option v-for="op in class_options" :label="op.zhcn" :value="op.eng"/>
        </el-select>
      </el-form-item>
      <el-form-item label="Region">
        <el-select v-model="form.Region" placeholder="please select your zone">
          <el-option v-for="op in region_options" :label="op.zhcn" :value="op.eng"/>
        </el-select>
      </el-form-item>
      <el-form-item label="Race">
        <el-select v-model="form.Race" placeholder="please select your zone">
          <el-option v-for="op in race_options" :label="op.zhcn" :value="op.eng"/>
        </el-select>
      </el-form-item>
      <el-form-item label="Description">
        <div class="test-box">
          <el-input v-model="form.Description" type="textarea" autosize=""/>
        </div>
      </el-form-item>
    </el-form>
  </div>

  <div class="Button">
    <Button
        tabindex="-1"
        class="transition !duration-300 focus:outline-none w-full py-3 rounded font-bold text-white bg-blue-400 ring-4 ring-blue-500 ring-opacity-50 cursor-pointer hover:bg-indigo-400 hover:ring-indigo-500 transform hover:scale-110 hover:-translate-y-1 hover:shadow-xl hover:opacity-80 shadow-indigo-500"
        @click="onSubmit()">
      register
    </Button>
  </div>

  <div class="jump">
    <p style="color: #888888">yes i already have an account</p>
    <el-button
        tabindex="-1"
        @click="back()">
      click me to log in
    </el-button>
  </div>
</template>

<script setup>
import {useRouter} from "vue-router";
import {register} from "../../api/manager";
import {NOTATION} from "../../composable/utils";
import {reactive} from "@vue/reactivity";
import {ref} from "vue";

const router = useRouter()

let registerFlag = ref(1)

const form = reactive({
  CodeName: '',
  Password: '',
  PwConfirm: '',
  Class: '',
  Region: '',
  Race: '',
  Description: ''
})

const back = () => {
  router.push("/login")
}

const checkSyntax = (str) => {
  const pattern = /^[A-za-z0-9][A-za-z0-9'.\s]*$/
  if (str !== '') {
    if (!pattern.test(str)) {
      NOTATION(0, 'contains only alnum and . and space')
      registerFlag.value = 0
    } else {
      registerFlag.value = 1
    }
  } else {
    registerFlag.value = 0
    NOTATION(0, 'CodeName shouldn\'t be null')
  }
}

const onSubmit = () => {
  if (form.Password === '') {
    NOTATION(0, "passwords not null")
  }
  if (form.Password !== form.PwConfirm) {
    NOTATION(0, "passwords do not coordinate")
  } else if (!registerFlag.value) {
    NOTATION(0, "please check your CodeName")
  } else {
    register(form)
        .then(res => {
          console.log(res)

          if (res.status !== 200 && res.status !== 201) {
            if ("details" in res.data) {
              NOTATION(0, res.data.details)
            } else {
              NOTATION(0, "ops~! other error")
            }
          } else {
            // message
            NOTATION(1, "registered successfully")

            // jump
            router.push("/login")
          }
        })
        .catch(err => {
          console.log(err)
          NOTATION(0, err.msg)
        })
  }
}

const class_options = ref([
  {zhcn: "????????????", eng: "Guard"},
  {zhcn: "????????????", eng: "Sniper"},
  {zhcn: "????????????", eng: "Defender"},
  {zhcn: "????????????", eng: "Medic"},
  {zhcn: "????????????", eng: "Supporter"},
  {zhcn: "????????????", eng: "Caster"},
  {zhcn: "????????????", eng: "Specialist"},
  {zhcn: "????????????", eng: "Vanguard"},
])

const region_options = ref([
  {zhcn: '???', eng: 'Yan'},
  {zhcn: '????????????', eng: 'Columbia'},
  {zhcn: '????????????', eng: 'Kazimierz'},
  {zhcn: '?????????', eng: 'Kjerag'},
  {zhcn: '?????????', eng: 'Laterano'},
  {zhcn: '????????????', eng: 'Leithanien'},
  {zhcn: '????????????', eng: 'Rim Billiton'},
  {zhcn: '??????', eng: 'Sami'},
  {zhcn: '?????????', eng: 'Minos'},
  {zhcn: '????????????', eng: 'Bol??var'},
  {zhcn: '?????????', eng: 'Sargon'},
  {zhcn: '?????????', eng: 'Siracusa'},
  {zhcn: '????????????', eng: 'Victoria'},
  {zhcn: '????????????', eng: 'Kazdel'},
  {zhcn: '????????????', eng: 'Iberia'},
  {zhcn: '?????????', eng: '??gir'},
  {zhcn: '?????????', eng: 'Rhodes Island'},
  {zhcn: '??????', eng: 'Unknown'},
])

const race_options = ref([
  {zhcn: '???', eng: 'Lung'},
  {zhcn: '?????????', eng: 'Liberi'},
  {zhcn: '??????', eng: 'Lupo'},
  {zhcn: '???', eng: 'Oni'},
  {zhcn: '???????????????', eng: 'Archosauria'},
  {zhcn: '?????????', eng: 'Sankta'},
  {zhcn: '?????????', eng: 'Sarkaz'},
  {zhcn: '??????', eng: 'Feline'},
  {zhcn: '?????????', eng: 'Vouivre'},
  {zhcn: '?????????', eng: 'Draco'},
  {zhcn: '?????????', eng: 'Vulpo'},
  {zhcn: '??????', eng: 'Durin'},
  {zhcn: '?????????', eng: 'Zalak'},
  {zhcn: '?????????', eng: 'Kuranta'},
  {zhcn: '?????????', eng: 'Cautus'},
  {zhcn: '????????????', eng: 'Caprinae'},
  {zhcn: '??????', eng: 'Perro'},
  {zhcn: '??????', eng: 'Forte'},
  {zhcn: '?????????', eng: 'Ursus'},
  {zhcn: '?????????', eng: 'Aslan'},
  {zhcn: '??????', eng: 'Kylin'},
  {zhcn: '?????????', eng: '??gir'},
  {zhcn: '??????', eng: 'Unknown'}
])

</script>

<style scoped>
.register {
  margin-top: 8%;
  margin-bottom: 4%;
  text-align: center;
}

.input-box {
  margin-left: 32%;
  text-align: center;
}

.test-box {
  width: 40%;
  text-align: center;
}

.el-input {
  width: 250px;
  text-align: center
}


.Button {
  margin-top: 2%;
  margin-bottom: 4%;
  max-width: 8%;
  max-height: 3%;
  margin-left: 46%;
  text-align: center;
}

.jump {
  margin-top: 2%;
  text-align: center;
}

.transition {
  -webkit-transition-property: background-color, border-color, color, fill, stroke, opacity, -webkit-box-shadow, -webkit-transform, filter, backdrop-filter;
  -o-transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, -webkit-box-shadow, transform, -webkit-transform, filter, backdrop-filter;
  -webkit-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -o-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -webkit-transition-duration: 150ms;
  -o-transition-duration: 150ms;
  transition-duration: 150ms;
}

</style>