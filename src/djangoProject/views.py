from django.shortcuts import render, HttpResponse

# pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage

from Document.models import Documents

from pathlib import Path
import sys
import os
import json

#Add another file that is outside of the project
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, 'code'))

import search_model


def main(request):
    return render(request, 'main.html')

def about(request):

    docs = Documents.objects.all()

    paginator = Paginator(docs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'about.html', {'page_obj': page_obj})




def search(request):
    if request.method =='POST':
        search = request.POST['search']
        model = request.POST['model']

        index = search_model.search(query=search, model=model)
        docs = Documents.objects.filter(id__in=index)

    else:
        docs = Documents.objects.all()

    #truncate the description
    for doc in docs:
        if len(doc.content) > 300:
            doc.content = doc.content[:300] + "..."

    paginator = Paginator(docs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, "search.html", {"page_obj": page_obj})

