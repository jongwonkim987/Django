from django.shortcuts import render, get_object_or_404
# from django.http import http404

from bookmark.bookmark.models import Bookmark


# Create your views here.
def bookmark_list(request):
    bookmarks = Bookmark.objects.all()

    context = {'bookmarks': bookmarks}
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except Bookmark.DoesNotExist:
    #     raise http404

    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark': bookmark}
    return render(request, 'bookmark_detail.html', context)