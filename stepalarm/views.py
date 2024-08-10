import logging
from django.shortcuts import render
import stepalarm.models as models

from django.http import HttpResponse
import django.template.loader as djtemplateloader
import django.http as djhttp



_g_logger = logging.getLogger(__name__)

# Create your views here.

def get_reading():
    return 100

def _get_scale():
    try:
        s = models.Scale.objects.latest("creation_time")
        _g_logger.info("Found Scale")
        return s
    except models.Scale.DoesNotExist:
        _g_logger.info("There is no Scale")
        return None


def get_state(scale_db_obj):
    if scale_db_obj.zero_offset is None:
        return "NEEDS_ZERO"
    elif scale_db_obj.step_weight is None:
        return "NEEDS_STEP"
    else:
        diff = scale_db_obj.step_weight - scale_db_obj.zero_offset
        thresh = diff * scale_db_obj.threshold
        if scale_db_obj.zero_offset + thresh > get_reading():
            return "ACTIVE"
        else:
            return "INACTIVE"


def zeroscale(request):
    context = {}

    scale_db_obj = _get_scale()
    if scale_db_obj is None:
        # you need to add a scale
        scale_db_obj = models.Scale()

    if request.method == "POST":
        if "zero_it" in request.POST:
            scale_db_obj.zero_offset = get_reading()
        elif "stepped_on" in request.POST:
            scale_db_obj.step_weight = get_reading()
        scale_db_obj.save()

    context['creation_time'] = scale_db_obj.creation_time
    context['zero_offset'] = scale_db_obj.zero_offset
    context['threshold'] = scale_db_obj.threshold
    context['stepped_weight'] = scale_db_obj.step_weight
    context['stepped_weight'] = scale_db_obj.step_weight
    context['current_reading'] = get_reading()
    context['state'] = get_state(scale_db_obj)

    template = djtemplateloader.get_template("zero.html")
    return djhttp.HttpResponse(template.render(context, request))
