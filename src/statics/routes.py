import os
from flask import send_from_directory
from src.statics import bp


@bp.route('/uploads/<path:filename>')
def serve_image(filename):
    dir = os.path.abspath('./public/uploads/')
    print(dir)
    return send_from_directory(dir, filename)
