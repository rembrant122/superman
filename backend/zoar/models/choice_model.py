from models.basic_models import AutomatisationBaseModel


class ChoiceModel(AutomatisationBaseModel):

    id: int  # ид шага
    text_button: str  # текст на кнопке
