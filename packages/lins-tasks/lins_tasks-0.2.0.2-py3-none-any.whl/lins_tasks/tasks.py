from lins_tasks.tasksmodel import TasksModel
from lins_tasks.tasksserializer import TasksSerializer
import threading
from django.http import JsonResponse
from datetime import datetime, timedelta


class Tasks:
    @staticmethod
    def __update_task(id_task, data):
        model = TasksModel.objects.get(pk=id_task)
        objeto = TasksSerializer(model, data=data, partial=True)
        objeto.is_valid(raise_exception=True)
        objeto.save()

    def __executar_tarefa(self, target, id_task, *args):
        result = None
        try:
            self.__update_task(id_task=id_task, data={'status': 1})
            result = target(id_task, *args)
        except Exception as erro:
            self.__update_task(id_task=id_task, data={'status': 3, 'result': str(erro)})
        else:
            self.__update_task(id_task=id_task, data={"status": 2, 'result': str(result)})
        return result

    def create_task(self, target, args, task_name):
        model = TasksModel.objects.filter(task=task_name).first()
        if model and (not (model.status in [2, 3])):
            return JsonResponse({"task": task_name, "task_id": model.id, "status": 'PENDING'})
        self.__clear_tasks()
        model = TasksModel.objects.create(task=task_name, meta=str(args), status=0)
        params = [target, model.id, args]
        t = threading.Thread(target=self.__executar_tarefa, args=params)
        t.start()
        return JsonResponse({"task": task_name, "task_id": model.id, "status": 'STARTED'})

    @staticmethod
    def __clear_tasks():
        d = datetime.today() - timedelta(days=7)
        models = TasksModel.objects.filter(created_at__lte=d)
        if models:
            for model in models:
                model.delete()
