import { computed, ref } from 'vue'
import { loadStudyItems, saveStudyResult } from '../services/api'
import { buildSavePayload, getRepeatStages, isSkillItem, isWordItem } from '../services/studyAdapter'
import { createStudyEngine } from '../services/studyEngineFactory'
import type { QueryParamsModel, RepeatStageConfig, StudyItem } from '../models/study'
import type { RepeatEngine } from '../services/repeatEngine'
import {StudyCardState} from "../models/study";


export function useStudySession():StudyCardState {
  const allItems = ref<StudyItem[]>([])
  const stageConfigs = ref<RepeatStageConfig[]>([])
  const engine = ref<RepeatEngine<StudyItem> | null>(null)

  const showExtra = ref<boolean>(false)
  const isLoading = ref<boolean>(true)
  const isFinished = ref<boolean>(false)
  const errorText = ref<string>('')
  const params = ref<QueryParamsModel | null>(null)

  const currentStageIndex = computed<number>(() => {
    return engine.value?.currentStageIndex ?? 0
  })

  const currentItem = computed<StudyItem | null>(() => {
    return engine.value?.currentItem ?? null
  })

  const currentStage = computed<RepeatStageConfig | null>(() => {
    return stageConfigs.value[currentStageIndex.value] ?? null
  })

  const mainText = computed<string>(() => {
    if (!currentItem.value || !currentStage.value) {
      return ''
    }

    return currentStage.value.getMainText(currentItem.value)
  })

  const extraText = computed<string>(() => {
    if (!currentItem.value || !currentStage.value) {
      return ''
    }

    return currentStage.value.getExtraText(currentItem.value)
  })

  const fullCard = computed<FullCardModel>(() => {
    const emptyCard: FullCardModel = {
      word: '',
      translate: '',
      transcription: '',
      context: '',
    }

    const item = currentItem.value

    if (!item) {
      return emptyCard
    }

    if (isWordItem(item)) {
      return {
        word: item.word ?? '',
        translate: item.translate ?? '',
        transcription: item.transcription ?? '',
        context: item.context ?? '',
      }
    }

    if (isSkillItem(item)) {
      return {
        word: item.skill_name ?? item.instruction ?? '',
        translate: item.description ?? '',
        transcription: '',
        context: '',
      }
    }

    return emptyCard
  })


  function processRepeat(result: boolean): void {
    const currentEngine = engine.value

    if (!currentEngine || !currentItem.value) {
      return
    }

    if (!result) {
      showExtra.value = true
      currentEngine.remember(false)
      return
    }

    showExtra.value = false
    currentEngine.remember(true)

    if (currentEngine.isFinished) {
      void finish()
    }
  }

  function nextAfterFail(): void {
    showExtra.value = false
  }

  async function finish(): Promise<void> {
    if (!params.value) {
      return
    }

    isFinished.value = true

    const failedIds = new Set(engine.value?.failedIds ?? [])

    for (const item of allItems.value) {
      const result = !failedIds.has(item.id)
      const payload = buildSavePayload(params.value, item, result)

      await saveStudyResult(params.value, payload)
    }
  }

  async function init(): Promise<void> {
    try {
      isLoading.value = true
      errorText.value = ''
      isFinished.value = false
      showExtra.value = false

      const response = await loadStudyItems()

      params.value = response.params
      allItems.value = response.items
      stageConfigs.value = getRepeatStages(response.params)
      engine.value = createStudyEngine(response.items, stageConfigs.value.length)

      if (allItems.value.length === 0) {
        isFinished.value = true
      }
    } catch (error) {
      errorText.value = error instanceof Error ? error.message : 'Ошибка загрузки'
    } finally {
      isLoading.value = false
    }
  }
главный текст - про любовь
  return {
    mainText,
    extraText,
    fullCard,
    showExtra,
    isLoading,
    isFinished,
    errorText,
    processRepeat,
    nextAfterFail,
    init,
  }
}