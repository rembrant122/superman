let allWords = []
let currentWords = []
let nextRoundWords = []

let repeatIndex = 0
let repeatStage = 1

const firstRoundResults = {}
let isFirstFullRound = true

const urlParams = new URLSearchParams(window.location.search)
const token = urlParams.get("token") || ""
const app = urlParams.get("app") || ""
const repeat = urlParams.get("repeat") === "true"

function getHeaders() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  }
}

function getLoadUrl() {
  if (app === "eng_words" && repeat) {
    return "/get_list_words_for_repeat"
  }

  if (app === "eng_words" && !repeat) {
    return "/get_list_words_for_memorize_eng"
  }

  if (app === "skills" && repeat) {
    return "/get_skill_for_repeat"
  }

  if (app === "skills" && !repeat) {
    return "/get_skill_for_memorize"
  }

  throw new Error("Неизвестный режим приложения")
}

function getSaveUrl() {
  if (app === "eng_words" && repeat) {
    return "/save_result_repeat_word"
  }

  if (app === "eng_words" && !repeat) {
    return "/save_result_memorize"
  }

  if (app === "skills" && repeat) {
    return "/save_result_repeat_skill"
  }

  if (app === "skills" && !repeat) {
    return "/save_result_memorize_skill"
  }

  throw new Error("Неизвестный режим приложения")
}

function getItemsFromResponse(data) {
  if (Array.isArray(data?.words)) {
    return data.words
  }

  if (Array.isArray(data?.data?.words)) {
    return data.data.words
  }

  if (Array.isArray(data?.data)) {
    return data.data
  }

  if (Array.isArray(data)) {
    return data
  }

  return []
}

async function load() {
  const response = await fetch(getLoadUrl(), {
    method: "GET",
    headers: getHeaders(),
  })

  const data = await response.json()
  allWords = getItemsFromResponse(data)

  if (allWords.length === 0) {
    document.getElementById("repeat-mode").innerHTML =
      "<div class='word'>Нет элементов для показа</div>"
    return
  }

  currentWords = [...allWords]
  renderRepeatWord()
}

function getMainText(item) {
  if (repeatStage === 1) {
    return item.word ?? item.name ?? item.text ?? ""
  }

  return item.translate ?? item.description ?? item.answer ?? ""
}

function getExtraText(item) {
  if (repeatStage === 1) {
    return item.translate ?? item.description ?? item.answer ?? ""
  }

  return item.word ?? item.name ?? item.text ?? ""
}

function renderRepeatWord() {
  if (repeatIndex >= currentWords.length) {
    if (repeatStage === 1) {
      repeatStage = 2
      repeatIndex = 0
    } else {
      if (isFirstFullRound) {
        isFirstFullRound = false
      }

      currentWords = [...nextRoundWords]
      nextRoundWords = []
      repeatStage = 1
      repeatIndex = 0

      if (currentWords.length === 0) {
        finishRepeat()
        return
      }
    }
  }

  const currentWord = currentWords[repeatIndex]

  document.getElementById("repeat-main").innerText = getMainText(currentWord)
  document.getElementById("repeat-extra").style.display = "none"
  document.getElementById("repeat-buttons").style.display = "block"
  document.getElementById("next-after-fail").style.display = "none"
}

function rememberWord(result) {
  const currentWord = currentWords[repeatIndex]

  if (isFirstFullRound && result === false) {
    firstRoundResults[currentWord.id] = false
  }

  if (result) {
    if (
      isFirstFullRound &&
      firstRoundResults[currentWord.id] === undefined &&
      repeatStage === 2
    ) {
      firstRoundResults[currentWord.id] = true
    }

    repeatIndex++
    renderRepeatWord()
    return
  }

  addWordToNextRound(currentWord)

  const extra = document.getElementById("repeat-extra")
  extra.innerText = getExtraText(currentWord)

  extra.style.display = "block"
  document.getElementById("repeat-buttons").style.display = "none"
  document.getElementById("next-after-fail").style.display = "block"
}

function nextRepeatWord() {
  repeatIndex++
  renderRepeatWord()
}

function addWordToNextRound(word) {
  if (!nextRoundWords.some(w => w.id === word.id)) {
    nextRoundWords.push(word)
  }
}

function buildSavePayload(item) {
  if (app === "eng_words" && repeat) {
    return {
      user_id: 0,
      id_word: item.id,
      result: firstRoundResults[item.id] ?? true,
    }
  }

  if (app === "eng_words" && !repeat) {
    return {
      user_id: 0,
      id_word: item.id,
      result: firstRoundResults[item.id] ?? true,
    }
  }

  if (app === "skills" && repeat) {
    return {
      user_id: 0,
      id_skill: item.id,
      result: firstRoundResults[item.id] ?? true,
    }
  }

  if (app === "skills" && !repeat) {
    return {
      user_id: 0,
      id_skill: item.id,
      result: firstRoundResults[item.id] ?? true,
    }
  }

  throw new Error("Неизвестный режим приложения")
}

async function finishRepeat() {
  document.getElementById("repeat-mode").innerHTML =
    "<div class='word'>Готово</div>"

  const saveUrl = getSaveUrl()

  for (const word of allWords) {
    await fetch(saveUrl, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(buildSavePayload(word)),
    })
  }
}

load()
