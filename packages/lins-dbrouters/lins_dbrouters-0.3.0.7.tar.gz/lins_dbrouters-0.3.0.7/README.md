O que há neste pacote?
============

Router para definir quais models utilizam determinadas bases de dados

Definir no settings:
------------

DATABASE_MAPPING = {'app1': 'db1', 'app2': 'db2'}


Definir field:
------------

Chamado database no model:

~~~python
from django.db import models

class Banca(models.Model):
    class Meta:
        db_table = 'producao_banca'
        managed = False

    [...]

    database = 'pompeia'
~~~
