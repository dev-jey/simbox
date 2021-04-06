import re
from operator import attrgetter


class HeaderMixin():
    '''Mixin for HTML meta tags.'''

    instance = None
    title: str = None
    description: str = None
    keywords: str = None
    og_image: str = None
    og_url: str = None

    def get_context_data(self, **kwargs):
        '''Calls the get_context_data function from the view to pass the meta
        tags into the context. '''
        context = super().get_context_data(**kwargs)

        # If no instance is given, call the current instance used in the view.
        if self.instance is None:
            self.instance = self.get_object()

        context['meta_tags'] = self.get_meta_data(self.instance)

        return context

    def get_meta_data(self, instance):
        if self.title is None:
            self.title = 'Simbox'
        else:
            title = attrgetter(self.create_lookup_string(self.title))(instance)
            self.title = re.sub(r"\<([A-Za-z0-9_]+)\>", title, self.title)
            self.title += ' - Simbox'

        if self.description is None:
            self.description = 'Simbox - your one stop website for all your Flight Sim needs.'
        else:
            description = attrgetter(
                self.create_lookup_string(self.description))(instance)
            self.description = re.sub("<(.*)>", description, self.description)

        if self.keywords is None:
            self.keywords = 'Flight Simulation, MSFS2020, FSX, Prepar3D, X-Plane 11'
        else:
            self.keywords = getattr(
                instance, re.search("<(.*)>", self.keywords).group(1)
            )

        if self.og_image:
            self.og_image = attrgetter(
                self.create_lookup_string(self.og_image))(instance)

        data = {
            'title': self.title,
            'description': self.description,
            'keywords': self.description,
            'og_image': self.og_image,
            'og_url': self.og_url
        }

        return data

    def create_lookup_string(self, lookup_data):
        '''Looks for a string inside < and > signs and returns it.
        If multiple are found, they get concatenated with a dot (.).'''
        lookup_data = re.findall(r"\<([A-Za-z0-9_]+)\>", lookup_data)
        lookup_var = ''

        for count, res in enumerate(lookup_data):
            if count == 0:
                lookup_var += res + ''
            else:
                lookup_var += '.' + res

        return lookup_var
