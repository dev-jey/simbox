import random
from project_box.apps.mods.models import Mod, Type


def categories_processor(request):
    context = {}
    try:
        mods = Mod.objects.all()
        simulators = Type.objects.all()
        # msfs = mods.filter(name='MSFS').first()
        # p3d = mods.filter(name='P3D').first()
        # x_plane = mods.filter(name='X-PLANE').first()
        context = {
            # 'msfs_mods': msfs,
            # 'p3d_mods': p3d,
            # 'x_plane_mods': x_plane,
            # 'msfs': msfs,
            # 'x_plane': x_plane,
            # 'p3d': p3d,
            'categories': simulators
        }
        context['featured'] = random.choice(mods)
    except BaseException as e:
        print(e)
        context['error'] = "No Mods Found"
    return context
