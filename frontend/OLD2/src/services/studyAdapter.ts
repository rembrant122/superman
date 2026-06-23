import type {
  QueryParamsModel,
  RepeatStageConfig,
  SavePayload,
  SkillModel,
  StudyItem,
  WordModel,
} from '../models/study'

// ========================================
// Проверка: элемент является словом.
// ========================================
export function isWordItem(item: StudyItem): item is WordModel {
  return 'word' in item && 'translate' in item
}

// ========================================
// Проверка: элемент является навыком.
// ========================================
export function isSkillItem(item: StudyItem): item is SkillModel {
  return 'instruction' in item && 'description' in item
}

// ========================================
// Первая стадия для слов:
// показываем английское слово.
// ========================================
const wordStageDirect: RepeatStageConfig = {
  id: 1,
  name: 'word_direct',
  getMainText(item: StudyItem): string {
    if (!isWordItem(item)) {
      return ''
    }

    return item.word
  },
  getExtraText(item: StudyItem): string {
    if (!isWordItem(item)) {
      return ''
    }

    // Тут слово специально НЕ добавляем,
    // потому что оно уже показано как mainText.
    const parts: string[] = []

    if (item.transcription) {
      parts.push(item.transcription)
    }

    if (item.context) {
      parts.push(item.context)
    }

    parts.push(item.translate)

    return parts.join('\n')
  },
}

// ========================================
// Вторая стадия для слов:
// показываем перевод.
// ========================================
const wordStageReverse: RepeatStageConfig = {
  id: 2,
  name: 'word_reverse',
  getMainText(item: StudyItem): string {
    if (!isWordItem(item)) {
      return ''
    }

    return item.translate
  },
  getExtraText(item: StudyItem): string {
    if (!isWordItem(item)) {
      return ''
    }

    // Тут перевод специально НЕ добавляем,
    // потому что он уже показан как mainText.
    const parts: string[] = [item.word]

    if (item.transcription) {
      parts.push(item.transcription)
    }

    if (item.context) {
      parts.push(item.context)
    }

    return parts.join('\n')
  },
}

// ========================================
// Первая стадия для навыков:
// показываем instruction,
// если его нет — skill_name.
// ========================================
const skillStageDirect: RepeatStageConfig = {
  id: 1,
  name: 'skill_direct',
  getMainText(item: StudyItem): string {
    if (!isSkillItem(item)) {
      return ''
    }

    return item.instruction || item.skill_name
  },
  getExtraText(item: StudyItem): string {
    if (!isSkillItem(item)) {
      return ''
    }

    // instruction тут НЕ дублируем,
    // потому что оно уже в mainText.
    return item.description
  },
}

// ========================================
// Вторая стадия для навыков:
// показываем description,
// а в полном ответе — instruction.
// ========================================
const skillStageReverse: RepeatStageConfig = {
  id: 2,
  name: 'skill_reverse',
  getMainText(item: StudyItem): string {
    if (!isSkillItem(item)) {
      return ''
    }

    return item.description
  },
  getExtraText(item: StudyItem): string {
    if (!isSkillItem(item)) {
      return ''
    }

    return item.instruction || item.skill_name
  },
}
потому что я друг а не враг
и ты мне нравишься
// ========================================
// Набор стадий по режиму.
//
// words + repeat     -> 2 стадии
// words + memorize   -> 3 стадии
// skills + repeat    -> 2 стадии
// skills + memorize  -> 2 стадии
// ========================================
export function getRepeatStages(params: QueryParamsModel): RepeatStageConfig[] {
  if (params.app === 'eng_words' && params.repeat) {
    return [wordStageDirect, wordStageReverse]
  }

  if (params.app === 'eng_words' && !params.repeat) {
    return [wordStageDirect, wordStageReverse, wordStageDirect]
  }

  if (params.app === 'skills' && params.repeat) {
    return [skillStageDirect, skillStageReverse]
  }

  return [skillStageDirect, skillStageReverse]
}

// ========================================
// Формирование payload для сохранения.
//
// Бек ждет:
// words  -> { id_word, result }
// skills -> { id_skill, result }
// user_id не нужен.
// ========================================
export function buildSavePayload(
  params: QueryParamsModel,
  item: StudyItem,
  result: boolean,
): SavePayload {
  if (params.app === 'eng_words') {
    return {
      id_word: item.id,
      result,
    }
  }

  return {
    id_skill: item.id,
    result,
  }
}