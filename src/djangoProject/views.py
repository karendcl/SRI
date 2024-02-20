from django.shortcuts import render, HttpResponse

# pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage


def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'main.html')



def search(request):
    if request.method =='POST':
        search = request.POST['search']
        model = request.POST['model']
        #wire it up to the model

        return HttpResponse(f'{search} {model}')

    # return documents in a paginator
    documents = ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5', 'Document 6', 'Document 7']

    paginator = Paginator(documents, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, "search.html", {"page_obj": page_obj})

