from django.core.exceptions import ValidationError


def mb_to_megabytes(mb):
    return mb * 1024 * 1024


def max_file_size_in_five_mb_validator(image):
    megabytes_limit = 5.0

    filesize = image.file.size

    if filesize > mb_to_megabytes(megabytes_limit):
        raise ValidationError(f"Max file size is {megabytes_limit}MB")
