from flask import Flask, render_template, request, redirect , url_for, session
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import markdown


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Used for session management


# initialise firebase 🔥🔥🔥🔥
cred = credentials.Certificate("./firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# set th upload  folder and allowed image extension
app.config['UPLOAD_FOLDER'] ='static/uploads'
app.config['ALLOWED_EXTENSIONS'] ={'png','jpg','jpeg','gif','webp'}


def allowed_file(filename):
    """Check th file has the valid extension"""
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/base")
def base():
    return render_template("base.html")



ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def allowed_file(filename):
    """Check if the file has the valid extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Admin login route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True  # Set admin session
            return redirect(url_for("home"))  # Redirect to home or admin page
        else:
            error = "Invalid credentials, please try again."
            return render_template("admin.html", error=error)

    return render_template("admin.html")


# Logout route to destroy session
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))



# Admin access check
def is_admin():
    return session.get("admin_logged_in", False)


@app.route("/allposts")
def allposts():
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


    # Pass all posts
    return render_template("allposts.html", posts=posts, tags_count=tags_count)



@app.route("/")
def home():
    print("home started 😎")
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
    
    return render_template("home.html", posts=posts, recent_post=recent_post, tags_count=tags_count)








# add posts
@app.route("/add", methods=["GET", "POST"])
def add_post():
    if not is_admin():
        return redirect(url_for("admin"))
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        summary = request.form["summary"]
        tags = request.form["tags"].split(",")
        tags = [tag.strip() for tag in tags]
        content_html = markdown.markdown(content)

        # handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                image_filename = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
                file.save(image_filename)

        # add to fire store
        db.collection("posts").add({
            "title" :title ,  
            "content" : content_html,
            "summary": summary,
            "image": image_filename,
            "tags" : tags,
        })

        return redirect(url_for("home"))
    return render_template("add_post.html")


#delete a post
@app.route("/delete/<string:post_id>")
def delete_post(post_id):

    if not is_admin():
        return redirect(url_for("admin"))
    

    # delete from firestore
    try:
        db.collection("posts").document(post_id).delete()
        return redirect(url_for("home"))
    except Exception as e:
        print(f"Error deleting post :{e}")
        return redirect(url_for("home"))
        
# update a post
@app.route("/edit/<post_id>", methods=["GET","POST"])
def edit_post (post_id):
    if not is_admin():
        return redirect(url_for("admin"))
    
    # find post to edit
    post_doc = db.collection("posts").document(post_id)
    post = post_doc.get()
    if not post.exists:
        return redirect(url_for("home"))
    
    post_data = post.to_dict()
    
    if request.method =="POST":
        # update the post with new data
        content = request.form["content"]
        content_html = markdown.markdown(content)
        updated_data = {
            "title" : request.form["title"],
            "summary": request.form["summary"],
            "content" :content_html,
        }

        # handle the image upload 
        if 'image' in request.files:
            file =request.files['image']
            if file and allowed_file(file.filename):
                #save image to static folder
                image_filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_filename))
                updated_data["image"] = image_filename
            

        post_doc.update(updated_data)
        return redirect(url_for("home"))
    
    return render_template("edit_post.html", post ={"id" :post_id, **post_data})


# search with tags
@app.route  ("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    posts_ref = db.collection("posts").stream()
    results = []
    for doc in posts_ref:
        post =doc.to_dict()
        post["id"] = doc.id

        #search in title content tags
        if query in post["title"].lower() or query in post["content"].lower() or query in [tag.lower() for tag in post.get("tags",[])]:
            results.append(post)

    return render_template("search_results.html", query=query, post=results)

if __name__ == "__main__":
    app.run(debug=True) 