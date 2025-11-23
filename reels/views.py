from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import F
import json

# Modellar
from .models import Reel  # Bizning Proxy Modelimiz
from posts.models import Like, Comment  # Asosiy Like va Comment jadvallari
from .forms import ReelCreateForm

# ==========================================
# 1. REEL LIST (LENTA)
# ==========================================
def reel_list(request):
    """
    Barcha videolarni ko'rsatadi.
    Optimallashtirish:
    - select_related('author'): Muallifni bitta so'rovda oladi.
    - prefetch_related('likes', 'comments'): Like va Commentlarni optimallashtiradi.
    """
    reels = Reel.objects.select_related('author').prefetch_related('likes', 'comments').all()
    return render(request, 'reels/reel_list.html', {'reels': reels})


# ==========================================
# 2. REEL CREATE (YUKLASH)
# ==========================================
@login_required
def reel_create(request):
    """
    Yangi video yuklash sahifasi.
    """
    if request.method == 'POST':
        form = ReelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_reel = form.save(commit=False)
            new_reel.author = request.user
            # Proxy model save() metodida 'post_type' avtomatik 'REEL' bo'ladi
            new_reel.save()
            return redirect('reels:reel_list')
    else:
        form = ReelCreateForm()
    
    return render(request, 'reels/reel_create.html', {'form': form})


# ==========================================
# 3. REEL DETAIL (TO'LIQ KO'RISH)
# ==========================================
def reel_detail(request, pk):
    """
    Videoni to'liq ekran qilib ko'rish.
    """
    reel = get_object_or_404(Reel.objects.select_related('author'), pk=pk)

    # 1. Ko'rishlar sonini oshirish (Atomic Update - xatosiz hisoblash)
    Reel.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    reel.refresh_from_db()

    # 2. Like holatini tekshirish
    is_liked = False
    if request.user.is_authenticated:
        # 'likes' - bu Post modelidagi related_name, Reel uchun ham ishlaydi
        is_liked = reel.likes.filter(user=request.user).exists()

    # 3. Sharhlar (Faqat ota sharhlar, Replylar prefetch qilinadi)
    comments = reel.comments.filter(parent=None)\
        .select_related('author')\
        .prefetch_related('replies__author')\
        .order_by('-created_at')

    context = {
        'reel': reel,
        'is_liked': is_liked,
        'comments': comments,
    }
    return render(request, 'reels/reel_detail.html', context)


# ==========================================
# 4. AJAX LIKE (REELS UCHUN)
# ==========================================
@login_required
@require_POST
def like_reel(request, pk):
    """
    Reelga like bosish (JSON qaytaradi).
    """
    reel = get_object_or_404(Reel, pk=pk)
    
    # Biz 'Reel' obyektini 'post' maydoniga beraveramiz, chunki u InstagramPost'dan voris olingan
    like_obj, created = Like.objects.get_or_create(post=reel, user=request.user)

    if not created:
        # Agar like bor bo'lsa -> O'chiramiz (Unlike)
        like_obj.delete()
        liked = False
    else:
        # Yangi like -> (Like)
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'new_count': reel.likes.count()
    })


# ==========================================
# 5. AJAX COMMENT (REELS UCHUN)
# ==========================================
@login_required
@require_POST
def comment_reel(request, pk):
    """
    Reelga sharh yoki javob (reply) yozish.
    """
    reel = get_object_or_404(Reel, pk=pk)

    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        parent_id = data.get('parent_id', None)
    except:
        return JsonResponse({'success': False, 'error': 'JSON xatosi'}, status=400)

    if not text:
        return JsonResponse({'success': False, 'error': 'Matn yo‘q'}, status=400)

    # Reply (Javob) ekanligini tekshirish
    parent_comment = None
    if parent_id:
        try:
            parent_comment = Comment.objects.get(id=parent_id)
        except Comment.DoesNotExist:
            pass

    # Yangi sharh yaratish (Posts ilovasidagi Comment jadvaliga tushadi)
    new_comment = Comment.objects.create(
        post=reel, # Reel bu Post bo'lgani uchun to'g'ri ishlaydi
        author=request.user,
        text=text,
        parent=parent_comment
    )

    # Profil rasmini aniqlash (Frontend uchun)
    if hasattr(request.user, 'profile_picture') and request.user.profile_picture:
        avatar_url = request.user.profile_picture.url
    else:
        avatar_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"

    return JsonResponse({
        'success': True,
        'comment': {
            'id': new_comment.id,
            'author_username': new_comment.author.username,
            'text': new_comment.text,
            'avatar_url': avatar_url,
            'parent_id': parent_id,
            'created_at': new_comment.created_at.strftime('%B %d, %Y')
        }
    })