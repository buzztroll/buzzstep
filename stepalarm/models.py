import uuid

import django.db.models as djmodels


# Create your models here.

class Scale(djmodels.Model):
    id = djmodels.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_time = djmodels.DateTimeField(
        auto_now_add=True, auto_now=False, blank=True, db_index=True)
    zero_offset = djmodels.FloatField(null=True)
    step_weight = djmodels.FloatField(null=True)
    threshold = djmodels.FloatField(default=0.5)
