from django.conf import settings
from django.apps import apps


class RouterByModel(object):
    """
    Router para definir quais models utilizam determinadas bases de dados
    Definir no settings:

    DATABASE_MAPPING = {'app1': 'db1', 'app2': 'db2'}

    Definir field chamado database no model:

    from django.db import models


    class Banca(models.Model):
        class Meta:
            db_table = 'producao_banca'
            managed = False

        [...]

        database = 'pompeia'
    """

    def db_for_read(self, model, **hints):

        if hasattr(model, 'database') and model.database in settings.DATABASE_MAPPING:
            return settings.DATABASE_MAPPING[model.database]
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, 'database') and model.database in settings.DATABASE_MAPPING:
            return settings.DATABASE_MAPPING[model.database]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = None
        if hasattr(obj1, 'database') and obj1.database in settings.DATABASE_MAPPING:
            db_obj1 = settings.DATABASE_MAPPING.get(obj1.database)
        db_obj2 = None
        if hasattr(obj2, 'database') and obj2.database in settings.DATABASE_MAPPING:
            db_obj2 = settings.DATABASE_MAPPING.get(obj2.database)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        model = apps.get_model(app_label=app_label, model_name=model_name)
        if db in settings.DATABASE_MAPPING.values():
            return (not hasattr(model, 'database')) or (hasattr(model, 'database') and model.database and \
                   settings.DATABASE_MAPPING.get(model.database) == db)
        elif hasattr(model, 'database') and model.database and model.database in settings.DATABASE_MAPPING:
            return False
        return None
