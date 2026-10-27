import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageCms, ImageDraw

PK = '/home/claude/pacchetto_pilota_v1'
_srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()


def save_srgb(im, path, jpg=False):
    """Esporta in sRGB con profilo ICC incorporato."""
    im = im.convert('RGB')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if jpg:
        im.save(path, 'JPEG', quality=94, subsampling=0, icc_profile=_srgb)
    else:
        im.save(path, 'PNG', icc_profile=_srgb, optimize=True)
    return path


def fit_size(lines, maxw, size, weight='Bold', minsize=40):
    """Riduce il corpo finché la riga più lunga entra in maxw."""
    from ae_lib import font
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    while size > minsize and max(d.textlength(l, font=font(weight, size)) for l in lines) > maxw:
        size -= 2
    return size
