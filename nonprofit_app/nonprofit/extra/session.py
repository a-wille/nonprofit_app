

def load_context(request):
    context = {}
    context['username'] = request.user.username
    return context