from flask import Flask, render_template, redirect, request, url_for
from database import load_posts, save_posts

app = Flask(__name__)

# Load all posts once at startup
blog_posts = load_posts()


@app.route('/')
def index():
    """Render the index page with all blog posts."""
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle adding a new blog post via GET (form) or POST (submit)."""
    if request.method == 'POST':
        # get form data from HTML form and trim whitespace
        title = request.form.get("title", "").strip()
        if not title:
            return "Title cannot be empty", 400

        author = request.form.get("author", "").strip()
        if not author:
            return "Author cannot be empty", 400

        content = request.form.get("content", "").strip()
        if not content:
            return "Content cannot be empty", 400

        # create new ID (safe if list is empty)
        if blog_posts:
            new_id = max(post["id"] for post in blog_posts) + 1
        else:
            new_id = 1

        # build dictionary for post
        new_post = {"id": new_id, "title": title, "author": author, "content": content}

        # append new post to list of dictionaries (blog_posts)
        blog_posts.append(new_post)

        # save updated posts list to JSON
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by its ID and update the JSON file."""
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)

    # save updated posts list to JSON
    save_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post by ID via GET (form) or POST (save changes)."""
    # search for post
    post = None
    for p in blog_posts:
        if p["id"] == post_id:
            post = p
            break

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # get form data and trim whitespace
        title = request.form.get("title", "").strip()
        if title:
            post["title"] = title

        author = request.form.get("author", "").strip()
        if author:
            post["author"] = author

        content = request.form.get("content", "").strip()
        if content:
            post["content"] = content

        # save updated posts list to JSON
        save_posts(blog_posts)

        return redirect(url_for('index'))

    # if GET → show form
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)