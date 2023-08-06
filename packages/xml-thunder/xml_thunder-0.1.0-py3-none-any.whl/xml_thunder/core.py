from xml.etree.ElementTree import parse


class Lightning(object):
    """
    Used for creating an XML parser
    """

    def __init__(self):
        self.__routes = {}

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__routes)

    def __contains__(self, route):
        return route in self.__routes.keys()

    def __getitem__(self, route):
        return self.__routes.get(route)

    def __setitem__(self, route, function):
        self.__routes[route] = function

    def __delitem__(self, route):
        del self.__routes[route]

    def __len__(self):
        return len(self.__routes)

    def __bool__(self):
        return self.__routes == {}

    def get_all_routes(self):
        """ Returns all registered routes """
        return self.__routes

    def route(self, path):
        """
        Creates a route for the provided 'path'

        Note that 'path' is any valid xPath
        """

        def inner(function_):
            self[path] = function_

            return function_

        return inner

    def parse(self, xml_like_document):
        """ The entrypoint for parsing xml strings/files """

        document_root = parse(xml_like_document).getroot()

        for path_as_string, function_ in self.__routes.items():
            for element in document_root.findall(path_as_string):
                if function_.__code__.co_argcount != 1:
                    raise ValueError(
                        f"{function_.__name__} may only have 1 parameter")
                function_(element)
