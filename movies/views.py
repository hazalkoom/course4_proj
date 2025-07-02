import urllib.parse

from celery.exceptions import TimeoutError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from course4_proj.celery import app
from movies.models import Movie
from movies.tasks import search_and_save

# Create your views here.

def search(request):
    search_term = request.GET["search_term"]
    print(f"DEBUG_DJANGO: Search term received: {search_term}") # <--- أضف هذا
    
    res = search_and_save.delay(search_term)
    print(f"DEBUG_DJANGO: Task sent to Celery. Task ID: {res.id}") # <--- أضف هذا

    try:
        res.get(timeout=2)
    except TimeoutError:
        print("DEBUG_DJANGO: Task still pending after 2 seconds. Redirecting to search_wait.") # <--- أضف هذا
        return redirect(
            reverse("search_wait", args=(res.id,))
            + "?search_term="
            + urllib.parse.quote_plus(search_term)
        )
    
    print("DEBUG_DJANGO: Task completed within 2 seconds. Redirecting to search_results.") # <--- أضف هذا
    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term),
        permanent=False,
    )

    
    
def search_wait(request, result_uuid):
    search_term = request.GET["search_term"]
    res = app.AsyncResult(result_uuid)

    try:
        res.get(timeout=-1)
    except TimeoutError:
        return HttpResponse("Task pending, please refresh.", status=200)

    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term)
    )
    
def search_results(request):
    search_term = request.GET["search_term"]
    movies = Movie.objects.filter(title__icontains=search_term)
    return HttpResponse(
        "\n".join([movie.title for movie in movies]), content_type="text/plain"
    )
