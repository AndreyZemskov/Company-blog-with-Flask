# blog_posts/views.py
import os

from flask import render_template, url_for, flash, request, redirect, Blueprint, send_file, abort
from flask_login import current_user, login_required
from companyblog import db
from companyblog.models import BlogPost
from companyblog.blog_posts.forms import BlogPostForm
from werkzeug.utils import secure_filename


upload_folder = '/home/username/PycharmProjects/companyblog/static/upload_folder'


blog_posts = Blueprint('blog_posts', __name__)

# CREATE
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
            form = BlogPostForm()

            if form.file.data == "":
                blog_post_nf = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id,
                                                                                    upload=form.file.default)
                db.session.add(blog_post_nf)
                db.session.commit()
                flash('Blog Post Created')
                return redirect(url_for('core.index'))

            if form.file.data != "":
                blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id,
                                                                                 upload=form.file.data.filename)

                filename = os.path.join(upload_folder, secure_filename(blog_post.upload))
                form.file.data.save(filename)
                db.session.add(blog_post)
                db.session.commit()
                flash('Blog Post Created')
                return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)



# BLOG POST (VIEW)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                            date=blog_post.date, post=blog_post,
                            upload=blog_post.upload)

# DOWNLOAD
@blog_posts.route('/<int:blog_post_id>/return-file',  methods=['GET'])
def download(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.upload == 'File has not been attached':
        abort(404)

    if request.method == 'GET':
        dir = '/home/username/PycharmProjects/companyblog/static/upload_folder' # Download file storage
        file = blog_post.upload
        return send_file(dir + file, attachment_filename=file)

# UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)

# DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))