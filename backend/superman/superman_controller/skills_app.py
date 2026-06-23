from apiflask import APIBlueprint

from app_flask.api_post import api_route
from app_flask.auth_user import get_user
from app_flask.save_and_send_app import send_message
from db.db_all import Skill, get_skill_for_memorize_db, get_skill_for_repeat_db
from db.db_basic import session_scope
from superman.models.models_superman import ResultRepeatSkill, SkillModel
from superman.superman_controller.random_words import prepare_skills
from superman.superman_controller.steps import get_next_step_time

skills_blueprint = APIBlueprint("skills", __name__)

@api_route(
    skills_blueprint,
    "/get_skill_for_repeat",
    method="get",
    output_model=SkillModel,
)
def get_skill_for_repeat():
    with session_scope() as session:

        user = get_user(session)
        ready_skill_db = get_skill_for_repeat_db(session, user.id)
        skill=prepare_skills(ready_skill_db)

    return send_message(skill)

@api_route(
    skills_blueprint,
    "/get_skill_for_memorize",
    method="get",
    output_model=SkillModel,
)

def get_skill_for_memorize():
    with session_scope() as session:

        user = get_user(session)
        skill_db = get_skill_for_memorize_db(session, user.id)
        skill=prepare_skills(skill_db)

    return send_message(skill)

@api_route(
    skills_blueprint,
    "/save_result_skill",
    input_model=ResultRepeatSkill,
)
def save_result_skill(skill_model: ResultRepeatSkill):
    with session_scope() as session:
        skill_db: Skill | None = Skill.find_by_id(session, skill_model.id_skill)

        if skill_db is None:
            return send_message()

        new_step = get_next_step_time(skill_db.stage, skill_model.result)
        skill_db.stage = new_step.step
        skill_db.next_date_time_for_repeat = new_step.new_date_time

    return send_message()
#
# @api_route(
#     skills_blueprint,
#     "/save_result_memorize_skill",
#     input_model=ResultRepeatSkill,
# )
# def save_result_memorize(result_skill_model: ResultRepeatSkill):
#     with session_scope() as session:
#         skill_db: Skill | None = Skill.find_by_id(session, result_skill_model.id_skill)
#
#         if skill_db is None:
#             return send_message()
#
#         skill_db.stage += 1
#
#     return send_message()
#
# @api_route(
#     skills_blueprint,
#     "/save_result_repeat_skill",
#     input_model=ResultRepeatSkill,
# )
# def save_result_repeat_skill(skill_model: ResultRepeatSkill):
#     with session_scope() as session:
#         skill_db: Skill | None = Skill.find_by_id(session, skill_model.id_skill)
#
#         if skill_db is None:
#             return send_message()
#
#         new_step = get_next_step_time(skill_db.stage, skill_model.result)
#         skill_db.stage = new_step.step
#         skill_db.next_date_time_for_repeat = new_step.new_date_time
#
#     return send_message()
#
# @api_route(
#     skills_blueprint,
#     "/save_result_memorize_skill",
#     input_model=ResultRepeatSkill,
# )
# def save_result_memorize(result_skill_model: ResultRepeatSkill):
#     with session_scope() as session:
#         skill_db: Skill | None = Skill.find_by_id(session, result_skill_model.id_skill)
#
#         if skill_db is None:
#             return send_message()
#
#         skill_db.stage += 1
#
#     return send_message()
