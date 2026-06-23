import type {
  AppMode,
  QueryParamsModel,
  SavePayload,
  SkillModel,
  StudyItem,
  WordModel,
} from '../models/study'

// ========================================
// Получаем query-параметры из URL.
// ========================================
function getQueryParams(): QueryParamsModel {
  const urlParams = new URLSearchParams(window.location.search)

  return {
    token: urlParams.get('token') || '',
    app: (urlParams.get('app') || 'eng_words') as AppMode,
    repeat: urlParams.get('repeat') === 'true',
  }
}

// ========================================
// Заголовки для запросов.
// ========================================
function getHeaders(token: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}

// ========================================
// Ручка загрузки.
// ========================================
function getLoadUrl(app: AppMode, repeat: boolean): string {
  if (app === 'eng_words' && repeat) {
    return '/get_list_words_for_repeat'
  }

  if (app === 'eng_words' && !repeat) {
    return '/get_list_words_for_memorize_eng'
  }

  if (app === 'skills' && repeat) {
    return '/get_skill_for_repeat'
  }

  return '/get_skill_for_memorize'
}

// ========================================
// Ручка сохранения.
// ========================================
function getSaveUrl(app: AppMode, repeat: boolean): string {
  if (app === 'eng_words' && repeat) {
    return '/save_result_repeat_word'
  }

  if (app === 'eng_words' && !repeat) {
    return '/save_result_memorize'
  }

  if (app === 'skills' && repeat) {
    return '/save_result_repeat_skill'
  }

  return '/save_result_memorize_skill'
}

// ========================================
// Проверка на объект.
// ========================================
function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

// ========================================
// Приводим ответ бека к массиву элементов.
//
// Варианты:
// 1) DictionaryModel -> data.words
// 2) один SkillModel
// 3) обертка { data: ... }
// ========================================
function getItemsFromResponse(data: unknown): StudyItem[] {

  // ----------------------------
  // Слова: { words: [...] }
  // ----------------------------
  if (isObject(data) && Array.isArray(data.words)) {
    return data.words as WordModel[]
  }

  // ----------------------------
  // Слова: { data: { words: [...] } }
  // ----------------------------
  if (
    isObject(data) &&
    isObject(data.data) &&
    Array.isArray(data.data.words)
  ) {
    return data.data.words as WordModel[]
  }

  // ----------------------------
  // Навык: один объект напрямую
  // ----------------------------
  if (
    isObject(data) &&
    typeof data.id === 'number' &&
    ('instruction' in data || 'description' in data || 'skill_name' in data)
  ) {
    return [data as SkillModel]
  }
навык доверия
  // ----------------------------
  // Навык: { data: {...} }
  // ----------------------------
  if (
    isObject(data) &&
    isObject(data.data) &&
    typeof data.data.id === 'number' &&
    (
      'instruction' in data.data ||
      'description' in data.data ||
      'skill_name' in data.data
    )
  ) {
    return [data.data as SkillModel]
  }

  return []
}

// ========================================
// Загружаем элементы.
// ========================================
export async function loadStudyItems(): Promise<{
  items: StudyItem[]
  params: QueryParamsModel
}> {
  const params = getQueryParams()

  const response = await fetch(getLoadUrl(params.app, params.repeat), {
    method: 'GET',
    headers: getHeaders(params.token),
  })

  if (!response.ok) {
    throw new Error(`Ошибка загрузки: ${response.status}`)
  }

  const data = await response.json()

  return {
    items: getItemsFromResponse(data),
    params,
  }
}
просто расслабь булки
// ========================================
// Сохраняем один результат.
// ========================================
export async function saveStudyResult(
  params: QueryParamsModel,
  payload: SavePayload,
): Promise<void> {
  const response = await fetch(getSaveUrl(params.app, params.repeat), {
    method: 'POST',
    headers: getHeaders(params.token),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Ошибка сохранения: ${response.status}`)
  }
}