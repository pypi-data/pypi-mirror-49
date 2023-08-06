from django.db import models


class TasksModel(models.Model):
    class Meta:
        managed = False
        db_table = 'tasks'
        ordering = ['-id']

    id = models.AutoField(db_column='id', primary_key=True, editable=False)
    task = models.CharField(db_column='task', max_length=50)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True)
    status = models.IntegerField(db_column='status')
    meta = models.TextField(db_column='meta', null=True)
    result = models.TextField(db_column='result', null=True)
