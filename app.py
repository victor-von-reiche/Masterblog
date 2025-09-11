import json

from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

with open("posts.json", encoding="utf-8") as fileobj:
    blog_posts = json.load(fileobj)


@app.route('/')
def index():
    """Render the index page with all blog posts."""
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle adding a new blog post via GET or POST."""
    if request.method == 'POST':
        # get form data from HTML form
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        # create new ID
        new_id = max(post["id"] for post in blog_posts) + 1

        # build dictionary for post
        new_post = {"id": new_id, "title": title, "author": author, "content": content}

        # append new post to list of dictionaries (blog_posts)
        blog_posts.append(new_post)

        # open posts.json and save the new list including new_post
        with open("posts.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by its ID and update the JSON file."""
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
    # Find the blog post with the given id and remove it from the list
    with open("posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post by ID via GET or POST."""
    # search for post
    post = None
    for p in blog_posts:
        if p["id"] == post_id:
            post = p
            break

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # get form data
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        # update values
        post["title"] = title
        post["author"] = author
        post["content"] = content

        # save back to JSON
        with open("posts.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    # if GET → show form
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
