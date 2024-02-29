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
import recommend


def main(request):
    return render(request, 'main.html')

def about(request):
    '''
    This function is used to display the documents in the database

    Args:
        - request: HttpRequest object

    Returns:
        - render: HttpResponse object
    '''

    docs = Documents.objects.all()

    paginator = Paginator(docs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'about.html', {'page_obj': page_obj})




def search(request, first = None):
    '''
    This function is used to search for documents in the database

    Args:
        - request: HttpRequest object
        - first: boolean, if true, the function will display all the documents in the database

    Returns:
        - render: HttpResponse object
    '''
    if request.method =='POST':
        search = request.POST['search']
        model = request.POST['model']

        docus = Documents.objects.all()
        docss = [doc.content for doc in docus]
        docs = search_model.search(query=search, model=model, documents = docss)
        docs = [i+1 for i in docs]
        request.session['docs'] = docs

        docs = Documents.objects.filter(id__in=docs)

    else:
        if first:
            docs = Documents.objects.all()
            docs = [i.id for i in docs]
            request.session['docs'] = docs
        else:
            docs = request.session['docs']
            docs = [i for i in docs]

        docs = Documents.objects.filter(id__in=docs)

    #truncate the description
    for doc in docs:
        if len(doc.content) > 300:
            doc.content = doc.content[:300] + "..."

    paginator = Paginator(docs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, "search.html", {"page_obj": page_obj})


def recommendation(request):
    '''
    This function is used to display the recommendations for the documents in the session

    Args:
        - request: HttpRequest object

    Returns:
        - render: HttpResponse object
    '''
    #try to retrieve the docs from the session
    try:
        docs = request.session['docs']
    except:
        print("No docs in session")
        return render(request, "recommendation.html", {"page_obj": None})

    #get the recommendations
    print(docs)
    rec, authors, genres = recommend.get_recommendations(docs)
    print(authors)

    paginator = Paginator(rec, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, "recommendation.html", {"page_obj": page_obj, "authors": authors, "genres": genres})