# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import subprocess
import traceback

from django.conf import settings
from threading import Timer
from mimetypes import guess_type
from urllib import pathname2url
from tempfile import NamedTemporaryFile


class ConversionError(Exception):
    """Raise when conversion was unsuccessful."""
    pass


class MissingPILError(Exception):
    """Raise when could not import PIL package."""
    pass


def guess_mimetype(document_path):
    """Guess mime type for a file in local filesystem.

    Return string containing valid mime type.
    """
    document_url = pathname2url(document_path)
    return guess_type(document_url)[0]


def render_document(document_path, extension="png"):
    """Render document using `unconv` converter.

    Package `unoconv` has to be installed and available on system
    path. Return `NamedTemporaryFile` instance.
    """

    # workaround: https://github.com/dagwieers/unoconv/issues/167
    # first convert a document to PDF and continue
    if extension == "pdf":
        temp_path = document_path
    elif guess_mimetype(document_path) == 'application/pdf':
        temp_path = document_path
    else:
        temp = render_document(document_path, extension="pdf")
        temp_path = temp.name

    # spawn subprocess and render the document
    output = NamedTemporaryFile(suffix='.{}'.format(extension))
    if settings.UNOCONV_ENABLE:
        timeout = None
        try:
            def kill(process):
                return process.kill()

            unoconv = subprocess.Popen(
                [settings.UNOCONV_EXECUTABLE, "-v", "-e", "PageRange=1-2",
                    "-f", extension, "-o", output.name, temp_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            timeout = Timer(settings.UNOCONV_TIMEOUT, kill, [unoconv])
            timeout.start()
            stdout, stderr = unoconv.communicate()
        except Exception as e:
            traceback.print_exc()
            raise ConversionError(str(e))
        finally:
            if timeout:
                timeout.cancel()

    return output


def generate_thumbnail_content(image_path, size=(200, 150)):
    """Generate thumbnail content from an image file.

    Return the entire content of the image file.
    """
    from cStringIO import StringIO

    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise MissingPILError()

    try:
        image = Image.open(image_path)
        source_width, source_height = image.size
        target_width, target_height = size

        if source_width != target_width or source_width != target_height:
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

        output = StringIO()
        image.save(output, format='PNG')
        content = output.getvalue()
        output.close()
        return content
    except BaseException:
        return None
