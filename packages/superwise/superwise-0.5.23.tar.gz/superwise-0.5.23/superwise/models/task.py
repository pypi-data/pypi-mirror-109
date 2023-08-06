""" This module implement Task model  """
from superwise.models.base import BaseModel


class Task(BaseModel):
    """ Task model class, model  for tasks data """

    def __init__(
        self,
        external_id=None,
        task_id=None,
        title=None,
        task_description=None,
        task_type_id=0,
        label=None,
        prediction=None,
        allow_label_overwrite=0,
        allow_prediction_update=0,
        ongoing_label=0,
        fictive_label_mapper=None,
        monitor_delay=None,
        time_units=None,
        **kwargs
    ):
        """
        constructer for Version class

        :param external_id:
        :param task_id:
        :param title:
        :param task_description:
        :param task_type_id:
        :param label:
        :param allow_label_overwrite:
        :param allow_prediction_update:
        :param ongoing_label:
        :param fictive_label_mapper:
        :param monitor_delay:
        :param time_units:
        """
        self.external_id = external_id
        self.title = title
        self.task_id = task_id or None
        self.task_description = task_description
        self.task_type_id = self.get_enum_value(task_type_id)
        self.label = label or []
        self.prediction = prediction or []
        self.allow_label_overwrite = allow_label_overwrite
        self.allow_prediction_update = allow_prediction_update
        self.ongoing_label = ongoing_label
        self.fictive_label_mapper = fictive_label_mapper
        self.monitor_delay = monitor_delay
        self.time_units = time_units  # defailty in back ["D", "7D"]
