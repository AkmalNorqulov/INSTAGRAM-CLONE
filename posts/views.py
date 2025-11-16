from django.views.generic import ListView, DetailView
from .models import InstagramPost, Comment, Like
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json



class PostListView(ListView):
    """
    Barcha InstagramPost ob'ektlarini ro'yxatini ko'rsatadi.
    Eng so'nggi postlar birinchi bo'lib ko'rinadi (modeldagi 'ordering' tufayli).
    """
    model = InstagramPost
    template_name = 'posts/post_list.html'  # Ishlatiladigan template nomi
    context_object_name = 'posts'  # Template ichida ishlatiladigan o'zgaruvchi nomi
    
class PostDetailView(DetailView):
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
    """
    Berilgan postga (pk) yangi sharh qo'shadi. 
    POST so'rovini qabul qiladi (odatiy AJAX chaqiruvi).
    """
    # 1. Postni topish
    post = get_object_or_404(InstagramPost, pk=pk)

    # 2. Foydalanuvchi tekshiruvi
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Avtorizatsiyadan o\'ting.'}, status=401)
        
    # 3. POST ma'lumotlarini olish
    try:
        # Ajax orqali JSON formatida kelayotgan bo'lishi mumkin
        data = json.loads(request.body)
        comment_text = data.get('text', '').strip()
    except:
        # Agar oddiy POST data bo'lsa (kamdan kam)
        comment_text = request.POST.get('text', '').strip()

    if not comment_text:
        return JsonResponse({'success': False, 'error': 'Sharh matni bo\'sh bo\'lishi mumkin emas.'}, status=400)
    
    # 4. Sharhni bazaga saqlash
    new_comment = Comment.objects.create(
        post=post,
        author=request.user,
        text=comment_text
    )
    
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