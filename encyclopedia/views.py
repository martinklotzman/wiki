from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    # Retrieve the wiki entry using get_entry
    entry = util.get_entry(title)
    
    if entry is None:
        # If the entry does not exist, show an error message
        return render(request, "encyclopedia/error.html", {
            "error_message": f"Sorry, the entry <b>{title}</b> does not exist."
        })
        
    else:
        # If the entry exists, convert it from markdown to HTML and display
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
