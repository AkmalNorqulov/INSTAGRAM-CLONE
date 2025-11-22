from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Reel
from .forms import ReelForm


def reel_list(request):
    reels = Reel.objects.select_related('user').prefetch_related('likes')[:100]
    return render(request, 'reels/list.html', {'reels': reels})


def reel_detail(request, pk):
    reel = get_object_or_404(Reel, pk=pk)
    return render(request, 'reels/detail.html', {'reel': reel})


@login_required
def reel_upload(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.user = request.user
            reel.save()
            return redirect('reels:list')
    else:
        form = ReelForm()
    return render(request, 'reels/upload.html', {'form': form})


@require_POST
@login_required
def reel_like_toggle(request, pk):
    reel = get_object_or_404(Reel, pk=pk)
    user = request.user
    if reel.likes.filter(pk=user.pk).exists():
        reel.likes.remove(user)
        liked = False
    else:
        reel.likes.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'count': reel.like_count()})



def reels_page(request):
    reels = Reel.objects.all()
    return render(request, "reels/reels_list.html", {"reels": reels})