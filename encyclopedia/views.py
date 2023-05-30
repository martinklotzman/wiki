from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def wiki(request, title):
    # Retrieve the wiki entry using get_entry
    wiki = util.get_entry(title)
    
    if wiki is None:
        # If the entry does not exist, show an error message
        return render(request, "encyclopedia/error.html", {
            "error_message": f"Sorry, the entry <b>{title}</b> does not exist."
        })
        
    else:
        # If the entry exists, convert it from markdown to HTML and display
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "wiki": wiki
        })
        
def search(request):
    # Get the search query from the GET data
    query = request.GET.get("q", "").lower()
    
    # Get the list of all entries
    entries = util.list_entries()
    
    # Direct user to wiki page if search result exists, else list related search results
    if query in (entry.lower() for entry in entries):
        return redirect('wiki', title=query)
    else:
        matching_entries = [entry for entry in entries if query in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "query": query
        })
