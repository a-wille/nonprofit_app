
from .session import load_context

def my_context(request):
	if not request.session.get('context', False):
		return load_context(request)
	context = request.session.get('context')
	return context

