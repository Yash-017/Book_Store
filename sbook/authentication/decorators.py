from django.shortcuts import redirect
from functools import wraps
from .models import UploadedFile
from django.contrib import messages

def redirect_if_no_files(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user has uploaded any files
        if not UploadedFile.objects.filter(user=request.user).exists():
            messages.info(request, 'You need to upload files first to see them.')
            # Redirect to upload_books view if no files are uploaded
            return redirect('upload_books')  # Adjust the URL name as needed

        # Call the original view function if files are uploaded
        return view_func(request, *args, **kwargs)

    return _wrapped_view
