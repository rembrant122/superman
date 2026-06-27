<template>
  <main class="app">
    <SkillCard />
  </main>
</template>

<script setup lang="ts">
import {onMounted} from 'vue'

import SkillCard from './components/SkillCard.vue'

// import {loadnew, skillStudySession,} from './services/skillmanager'

// import {StudyState} from './models/words.ts'

import {getStartStageType} from "./getStartStageType";
import {loadNewSkill, skillStudySession} from "./services/skillManager";

//запуск прилы
onMounted(async (): Promise<void> => {
  console.log('Приложение запущено')
  skillStudySession.value.stageType = getStartStageType() // определяем что делаем
  console.log('Тип режима:', skillStudySession.value.stageType)
  await loadNewSkill()
})
</script>
