from django.shortcuts import render
from django.http import HttpResponse
import subprocess

# Views
def home(request):
    return render(request, 'bank/home.html')

def run_tkinter(request):
    """Run the Tkinter application."""
    try:
        # Replace 'schnorr_app.py' with the path to your script
        subprocess.Popen(["python", r"bank\schnorr_app.py"])  # Non-blocking
        return HttpResponse("Pease enter and register your passkey ,Tkinter app is running!", content_type="text/plain")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")





