from lins_tasks.tasksmodel import TasksModel
from rest_flex_fields import FlexFieldsModelSerializer


class TasksSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TasksModel
        fields = ['id', 'task', 'created_at', 'status', 'meta', 'result']
