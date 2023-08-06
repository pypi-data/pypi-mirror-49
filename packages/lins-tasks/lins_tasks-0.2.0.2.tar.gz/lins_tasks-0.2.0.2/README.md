O que há neste pacote?
============

Execução de tarefas em segundo plano para django rest framework.

TasksView:
------------

Definição de Endpoint para manutenção das Tasks

~~~python
from lins_tasks import tasksview

router = SimpleRouter()
router.register('tasks', tasksview.TasksView, base_name='tasks')

urlpatterns = [
    url(r'^', include(router.urls)),
]
~~~


Tasks:
------------

Cria nova Task assincrona:

~~~python
from lins_tasks.tasks import Tasks

def criar_carga(self, request, *args, **kwargs):
    dados = request.data
    return Tasks().create_task(target=CriarCarga().criar, args=[dados], task_name='<<CARGA_NOVA>>' +
                       str(dados.get('id_usuario')))
~~~
