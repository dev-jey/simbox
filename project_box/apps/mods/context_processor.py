import random
from project_box.apps.mods.models import Type


def categories_processor(request):
    context = {}
    try:
        types = Type.objects.all()
        msfs = types.filter(name='MSFS').first()
        p3d = types.filter(name='P3D').first()
        x_plane = types.filter(name='X-PLANE').first()
        context = {
            'msfs_mods': msfs.mods.all()[:10],
            'p3d_mods': p3d.mods.all()[:10],
            'x_plane_mods': x_plane.mods.all()[:10],
            'msfs': msfs,
            'x_plane': x_plane,
            'p3d': p3d,
            'categories': types
        }
        context['featured'] = random.choice([context['x_plane_mods'], context['p3d_mods'], context['msfs_mods']])[0]
    except BaseException as e:
        print(e)
        context['error'] = "No Mods Found"
    return context
