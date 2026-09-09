from django.http import JsonResponse


def health(request):
    return JsonResponse({"service": "foundry360-api", "status": "ok"})
