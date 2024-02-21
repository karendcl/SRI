from django.shortcuts import render, HttpResponse

# pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from ..code import search_model


def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'main.html')



def search(request):
    if request.method =='POST':
        search = request.POST['search']
        model = request.POST['model']

        docs = search_model.search(query=search, model=model)

        paginator = Paginator(docs, 3)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, "search.html", {"page_obj": page_obj})




    # return documents in a paginator
    documents = ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5', 'Document 6', 'Document 7']

    paginator = Paginator(documents, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, "search.html", {"page_obj": page_obj})

