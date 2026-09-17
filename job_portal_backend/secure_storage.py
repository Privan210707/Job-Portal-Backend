import os
import cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class SecureResumeStorage(RawMediaCloudinaryStorage):
    def _upload(self, name, content):
        options = {
            'use_filename': True,
            'resource_type': 'raw',
            'type': 'authenticated',
            'unique_filename': True,
        }
        folder = os.path.dirname(name)
        if folder:
            options['folder'] = folder
        response = cloudinary.uploader.upload(
            content,
            **options
        )
        return response

    def url(self, name):
        resource = cloudinary.CloudinaryResource(
            name,
            resource_type='raw',
            type='authenticated'
        )
        return resource.build_url(
            secure=True,
            sign_url=True
        )