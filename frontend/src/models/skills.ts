import {StudyState} from "./StudyState";

export enum SkillType {
  LIST_WORDS_FOR_MEMORIZ = 'LIST_WORDS_FOR_MEMORIZ',
  LIST_WORD_FOR_IMAGENATED = 'LIST_WORD_FOR_IMAGENATED',
  EXERCISE = 'EXERCISE',
}

export type SkillModel = {

  id: number

  instruction: string
  description: string
  skill_name: string

  time_show: number
  time_for_remember: number

  skill_type: SkillType

  items: string[] | null

}

export type SkillStudySession={

  skills:SkillModel[]
  skillNow:SkillModel|null
  result:boolean|null
  state: StudyState

}
