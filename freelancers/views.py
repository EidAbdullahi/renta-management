from django.shortcuts import render
from .models import Freelancer
from .models import Freelancer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Freelancer, Comment
from .forms import CommentForm

def freelancer_list(request):
    freelancers = Freelancer.objects.all()
    return render(request, 'freelancers/list.html', {'freelancers': freelancers})




def freelancer_detail(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)
    comments = Comment.objects.filter(freelancer=freelancer).order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.freelancer = freelancer
            new_comment.save()
            return redirect('users/freelancer_detail', pk=pk)

    # For star display
    

    return render(request, 'detail.html', {
        'freelancer': freelancer,
        'comments': comments,
        'comment_form': comment_form,
        
    })
