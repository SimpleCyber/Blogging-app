from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.conf import settings
import os

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

import base64
import markdown


load_dotenv()

# loading the credentials
firebase_credentials = {
  "type": "service_account",
  "project_id": os.getenv("FIREBASE_PROJECT_ID"),
  "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
  "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.getenv("FIREBASE_CLIENT_ID"),
  "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
  "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
  "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
  "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create your views here.
def index(request):
    
    post_ref = db.collection("posts").stream()
    posts = []
    tags_count = {}
    
    for doc in post_ref:
        post = doc.to_dict()
        post["id"] = doc.id
        for tag in post.get("tags", []):
            tags_count[tag] = tags_count.get(tag, 0) + 1
        posts.append(post)
    
    posts = sorted(posts, key=lambda x: x.get("timestamp", 0), reverse=True)[:4]

    recent_post = posts[-1] if posts else None

    context = {
        "posts": posts,
        "recent_post": recent_post,
        "tags_count": tags_count,
    }
    
    return render(request,"index.html", context)
    
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html")
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")

def allposts(request):
    post_ref = db.collection("posts").stream()
    posts = []
    tags_count = {}
    
    for doc in post_ref:
        post = doc.to_dict()
        post["id"] = doc.id
        # Count tags
        for tag in post.get("tags", []):
            tags_count[tag] = tags_count.get(tag, 0) + 1
        posts.append(post)
    
    # Sort posts by timestamp (most recent first)
    posts = sorted(posts, key=lambda x: x.get("timestamp", 0), reverse=True)

    context = {
        "posts": posts,
        "tags_count": tags_count,
    }
    return render(request, "allposts.html",context)

def encode_image_to_base64(file):
    """Encode the uploaded file to Base64 string."""
    return base64.b64encode(file.read()).decode('utf-8')

def allowed_file(filename):
    """Check if the file has a valid image extension."""
    ALLOWED_EXTENSIONS = [
        "jpeg", "jpg", "png", "gif", "bmp", "webp", "tiff", "svg", "heif", "heic"
    ]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_post(request):
    if request.user.is_anonymous:
        return redirect("/login")
        
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        summary = request.POST.get("summary")
        tags = request.POST.get("tags").split(",")
        tags = [tag.strip() for tag in tags]
        content_html = markdown.markdown(content)

        # Handle image upload
        image_data = None
        image = request.FILES.get("image")
        if image and allowed_file(image.name):
            image_data = encode_image_to_base64(image)

        # add to fire store
        db.collection("posts").add({
            "title" :title ,  
            "content" : content_html,
            "summary": summary,
            "image": image_data,
            "tags" : tags,
        })

        print(title, content, summary, image, tags)

        return redirect("/")
    return render(request, "add_post.html")

def delete_post(request,post_id):
    # post_id
    if request.user.is_anonymous:
        return redirect("/login")

    try:
        db.collection("posts").document(post_id).delete()
        print("Post deleted successfully")
        return redirect("/allposts")
    except Exception as e:
        print(f"Error deleting post :{e}")
        return redirect("/allposts")
    
def edit_post (request, post_id):

    if request.user.is_anonymous:
        return redirect("/login")   


    post_doc = db.collection("posts").document(post_id)
    post = post_doc.get()


    if not post.exists:
        return redirect("/allposts")
    
    # Get the existing post data
    post_data = post.to_dict()
    post_data['id'] = post_id 

    print(post_data)

    
    if request.method == "POST":
        content = request.POST.get("content")
        content_html = markdown.markdown(content)
        updated_data = {
            "title": request.POST.get("title"),
            "summary": request.POST.get("summary"),
            "content": content_html,
        }

        image = request.FILES.get("image")
        if image and allowed_file(image.name):
            image_data = encode_image_to_base64(image)
            updated_data["image"] = image_data

        post_doc.update(updated_data)
        return redirect("/allposts")
    
    return render(request, "edit_post.html", {"post": post_data, "post_id": post_id})

def search(request):
    query = request.GET.get("q", "").lower()
    posts_ref = db.collection("posts").stream()
    results = []
    for doc in posts_ref:
        post =doc.to_dict()
        post["id"] = doc.id
        if query in post["title"].lower() or query in post["content"].lower() or query in [tag.lower() for tag in post.get("tags",[])]:
            results.append(post)

    return render(request,"search_results.html", {"query": query, "posts": results})
