from lins_tasks.tasksmodel import TasksModel
from lins_tasks.tasksserializer import TasksSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_flex_fields.views import FlexFieldsMixin


class TasksView(FlexFieldsMixin, ModelViewSet):
    serializer_class = TasksSerializer
    queryset = TasksModel.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id', 'task', 'created_at', 'status')
    filter_fields = ('id', 'task', 'created_at')
