from django.shortcuts import render

# Create your views here.
def posts_lists(request):
    return render(request,'posts/posts_lists.html')