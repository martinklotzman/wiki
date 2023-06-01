from django.shortcuts import render, redirect
from django import forms
from . import util
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

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
        
def entry(request):
    # If this is a POST request, try to process the form data
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Extract title and content from the form
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Check if an entry with this title exists
            if util.get_entry(title) is not None:
                # If the entry exists, render the form again with an error message
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "existing_entry": True
                })
            # Save the new entry
            util.save_entry(title, content)
            # Redirect to the newly created entry page
            return redirect('wiki', title=title)
    # If this is a GET request or the form is invalid, render a new form
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/new_entry.html", {
        "form": form
    })
    
def edit(request, title):
    # Check if the request method is POST
    if request.method == 'POST':
        # In that case, the form is submitted, so bind the POST data to a form instance
        form = NewEntryForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # If the form is valid, retrieve the cleaned data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Save the new entry using the utility function
            util.save_entry(title, content)
            # Redirect the user to the entry's page
            return redirect('wiki', title=title)
    else:
        # Retrieve the existing entry using get_entry utility function
        content = util.get_entry(title)
        # If the request method is not 'POST' (i.e., the user is just opening the edit page),
        # create a form instance with the current title and content of the entry as initial data
        form = NewEntryForm(initial={'title': title, 'content': content})
    
    # Render the form with the context data
    return render(request, 'encyclopedia/edit.html', {'form': form})

def random_entry(request):
    # Save all entries into a variable called 'entries'
    entries = util.list_entries()
    # Select a random entry from the list of entries
    random_entry = random.choice(entries)
    # We're passing the title of the random entry as an argument to match the <str:title> parameter in the URL pattern
    return redirect("wiki", title=random_entry)