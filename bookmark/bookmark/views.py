from django.shortcuts import render

# Create your views here.
def bookmark_list(request):
    return render(request, 'bookmark_list.html')

def bookmark_detail(request, number):
    context = {'number': number}
    return render(request, 'bookmark_detail.html', context)