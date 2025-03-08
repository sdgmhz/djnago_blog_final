from django.shortcuts import render
from django.views import generic


class PostListView(generic.ListView):
    pass

class PostDetailView(generic.DetailView):
    pass
