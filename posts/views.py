from django.views.generic import ListView, DetailView
from .models import InstagramPost, Comment, Like
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import InstagramPostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(LoginRequiredMixin,ListView):
    """
    Barcha InstagramPost ob'ektlarini ro'yxatini ko'rsatadi.
    Eng so'nggi postlar birinchi bo'lib ko'rinadi (modeldagi 'ordering' tufayli).
    """
    model = InstagramPost
    template_name = 'posts/post_list.html'  # Ishlatiladigan template nomi
    context_object_name = 'posts'  # Template ichida ishlatiladigan o'zgaruvchi nomi
    
class PostDetailView(LoginRequiredMixin,DetailView):
    model = InstagramPost
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Postga tegishli sharhlar sonini qo'shimcha kontekstga kiritadi.
        """
        context = super().get_context_data(**kwargs)
        
        # Obyektni olamiz (ya'ni, post)
        post = self.get_object() 
        
        # post.comments.count ni oldindan hisoblab, kontekstga qo'shamiz
        context['comment_count'] = post.comments.count() 
        
        return context
    

# Comment
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(InstagramPost, pk=pk)
    
    # ... (user check) ...
    
    try:
        data = json.loads(request.body)
        comment_text = data.get('text', '').strip()
        parent_id = data.get('parent_id', None) # Frontenddan parent_id keladimi?
    except:
        return JsonResponse({'success': False, 'error': 'Xato ma\'lumot'}, status=400)

    if not comment_text:
        return JsonResponse({'success': False, 'error': 'Bo\'sh sharh'}, status=400)
    
    # Ota sharhni aniqlash
    parent_comment = None
    if parent_id:
        try:
            parent_comment = Comment.objects.get(id=parent_id)
        except Comment.DoesNotExist:
            pass

    # Sharh yaratish
    new_comment = Comment.objects.create(
        post=post,
        author=request.user,
        text=comment_text,
        parent=parent_comment # Agar javob bo'lsa, ota sharh ulanadi
    )
    
    return JsonResponse({
        'success': True,
        'comment': {
            'author_username': new_comment.author.username,
            'text': new_comment.text,
            # Avatar URLini ham qo'shish kerak (yoki default)
            'avatar_url': new_comment.author.profile.avatar.url if hasattr(new_comment.author, 'profile') and new_comment.author.profile.avatar else "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg",
            'parent_id': parent_id
        }
    })
    
    # 5. Muvaffaqiyatli javobni qaytarish (Sharhni frontendda ko'rsatish uchun)
    return JsonResponse({
        'success': True,
        'comment': {
            'author_username': new_comment.author.username,
            'text': new_comment.text,
            'created_at': new_comment.created_at.strftime('%Y-%m-%d %H:%M'),
            # Agar sizda avatar URL bo'lsa, uni ham qo'shishingiz mumkin
        }
    })





# Like
@require_POST
def toggle_like(request, pk):
    """
    Postga like qo'shadi yoki olib tashlaydi.
    """
    post = get_object_or_404(InstagramPost, pk=pk)

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Avtorizatsiya talab qilinadi.'}, status=401)
        
    user = request.user
    liked = False
    
    # 1. Avvalgi like mavjudligini tekshirish
    try:
        existing_like = Like.objects.get(post=post, user=user)
        existing_like.delete() # Agar mavjud bo'lsa, uni o'chiramiz (Unlike)
        liked = False
    except Like.DoesNotExist:
        Like.objects.create(post=post, user=user) # Agar mavjud bo'lmasa, yangi like qo'shamiz
        liked = True

    # 2. Yangi like sonini hisoblash
    new_like_count = post.likes.count()
    
    # 3. Frontendga javob qaytarish
    return JsonResponse({
        'success': True,
        'liked': liked, # True (qo'shildi) yoki False (olib tashlandi)
        'new_count': new_like_count
    })




# Create Post

@login_required 
def post_create(request):
    if request.method == 'POST':
        # YANGI FORMA KLASSIDAN FOYDALANAMIZ
        form = InstagramPostCreateForm(request.POST, request.FILES) 
        
        if form.is_valid():
            new_post = form.save(commit=False)
            
            # Avtomatik ravishda hozirgi foydalanuvchini (muallifni) o'rnatamiz
            new_post.author = request.user
            
            new_post.save()
            
            return redirect('posts:post_list') 
    else:
        # YANGI FORMA KLASSIDAN FOYDALANAMIZ
        form = InstagramPostCreateForm()
    
    return render(request, 'posts/post_create.html', {'form': form})

# ... (qolgan view'lar: post_list, post_detail, toggle_like, add_comment) ...