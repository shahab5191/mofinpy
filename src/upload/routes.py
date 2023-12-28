import os
from src.extensions import db
from uuid import uuid4
from flask import current_app, request
from src.models.image_meta import ImageMeta
from src.upload import bp
from src.utils.protect_route import protected_route
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}


def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return str(uuid4()) + "." + ext


@bp.route('/upload/', methods=['POST'])
@protected_route
def upload_image():
    if 'file' not in request.files:
        return {"err": "You should provide a file"}, 400
    file = request.files['file']

    if file.filename == '':
        return {"err": "You should provide a file"}, 400

    if not allowed_file(file.filename):
        return {"err": "File format is not allowed"}, 400

    filename = generate_filename(file.filename)
    meta_data = ImageMeta(filename)
    db.session.add(meta_data)
    db.session.commit()
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                           filename))

    return {"image": meta_data.json()}, 201
