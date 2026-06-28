import {ref} from "vue";
import type {SkillStudySession} from "../models/skills";
import {SkillModel} from "../models/skills";
import {request} from "../api";
import {shuffleArray} from "./shuffleArray";

import {StudyState} from "../models/StudyState";
import {wordStudySession} from "./cardsManger";

export const skillStudySession = ref<SkillStudySession>({
  // skills: [],
  skillNow: null,
  result: null,
  state: StudyState.LOADING,

})

//
export async function loadNewSkill(): void{
    const session = skillStudySession.value







}

//
// export function setNextSkill(): void {
//   const session = skillStudySession.value
//
//   if (session.skills.length === 0) {
//     session.skillNow = null
//     session.state = StudyState.NO_WORDS
//     return
//   }
//
//   session.skills = shuffleArray(session.skills)
//
//   session.skillNow = session.skills.shift() ?? null
//   session.result = null
//
//   session.state = StudyState.STUDY
// }
//
// export async function resultSkill(result: boolean): Promise<void> {
//   const session = skillStudySession.value
//   const skill = session.skillNow
//
//   if (skill === null) return
//
//   session.result = result
//
//   await request({
//     url: '/save_result_skill',
//     method: 'POST',
//     body: {
//       skill_id: skill.id,
//       result,
//     },
//   })
//
//   setNextSkill()
// }
