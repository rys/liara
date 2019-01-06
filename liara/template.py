from typing import Dict
from . import Site

class Template:
    def render(self, **kwargs):
        pass


class TemplateRepository:
    __definition = Dict[str, str]

    def __init__(self, routes: Dict[str, str]):
        self.__routes = routes

    def find_template(self, url: str) -> Template:
        pass

    def _match_template(self, url: str) -> str:
        import fnmatch
        matches = []
        for pattern, template in self.__routes.items():
            if fnmatch.fnmatch(url, pattern):
                matches.append((len(pattern), template))

        matches = list(sorted(matches, key=lambda x: x[0], reverse=True))
        return matches[0][1]


class MakoTemplate(Template):
    def __init__(self, template):
        self.__template = template

    def render(self, **kwargs) -> str:
        return self.__template.render(**kwargs)


class MakoTemplateRepository(TemplateRepository):
    def __init__(self, routes, path):
        super().__init__(routes)
        from mako.lookup import TemplateLookup
        self.__lookup = TemplateLookup(directories=[path])

    def find_template(self, url) -> Template:
        template = self._match_template(url)
        return MakoTemplate(self.__lookup.get_template(template))


class Jinja2Template(Template):
    def __init__(self, template):
        self.__template = template

    def render(self, **kwargs) -> str:
        return self.__template.render(**kwargs)


class Jinja2TemplateRepository(TemplateRepository):
    def __init__(self, routes, path):
        super().__init__(routes)
        from jinja2 import FileSystemLoader, Environment

        self.__env = Environment(loader=FileSystemLoader(path))

    def find_template(self, url) -> Template:
        template = self._match_template(url)
        return Jinja2Template(self.__env.get_template(template))

class SiteTemplateProxy:
    __site: Site

    def __init__(self, site: Site):
        self.__site = site
        self.__data = {}
        for data in self.__site.data:
            self.__data.update (data.metadata)

    @property
    def data(self):
        return self.__data