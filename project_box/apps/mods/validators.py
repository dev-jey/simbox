from django.core.exceptions import ValidationError


def validate_file_size_10mb(value):
    filesize = value.size

    # 10Mb limit
    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def validate_file_size_4mb(value):
    filesize = value.size

    # 10Mb limit
    if filesize > 4194304:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value
