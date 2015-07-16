from django.db.models.fields.files import ImageFieldFile
from rest_framework import renderers


class ImageRenderer(renderers.BaseRenderer):
    # TODO: Support other image formats
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'image' in data and isinstance(data['image'], ImageFieldFile):
            return data['image'].file.read()
        else:
            return None
