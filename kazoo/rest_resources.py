import re

from .request_objects import KazooRequest


METHOD_TYPES = ("detail", "list", "update", "create", "delete")


class RestResource(object):
    def __init__(self, name, path, plural_name=None, extra_views=None,
                 methods=METHOD_TYPES, exclude_methods=None,
                 method_names=None):
        extra_views = extra_views or []
        exclude_methods = exclude_methods or []
        method_names = method_names or {}

        self._param_regex = re.compile("{([a-zA-Z0-9_]+)}")
        self.name = name
        self._plural_name = plural_name
        self._check_at_least_one_argument(path)
        self.required_args = self._get_required_arguments(path)
        self.object_arg = self._get_object_argument(path)
        self.path = self._get_resource_path(path)
        self._initialize_extra_view_descriptions(extra_views)
        self._initialize_methods(methods, exclude_methods)
        self._initialize_method_names(method_names)

    def _initialize_method_names(self, given_method_names):
        self.method_names = {
            "list": "get_{0}".format(self.plural_name),
            "object": "get_{0}".format(self.name),
            "update": "update_{0}".format(self.name),
            "create": "create_{0}".format(self.name),
            "delete": "delete_{0}".format(self.name),
        }
        self.method_names.update(given_method_names)

    def _initialize_methods(self, methods, exclude_methods):
        self.methods = list(set(methods) - set(exclude_methods))

    @staticmethod
    def _get_resource_path(path):
        return path[:path.rfind("{") - 1]

    def _check_at_least_one_argument(self, path):
        if not self._get_params(path):
            raise ValueError("Rest resources need at least one argument")

    def _get_required_arguments(self, path):
        params = self._get_params(path)
        if len(params) > 1:
            return params[:-1]
        return []

    def _get_object_argument(self, path):
        return self._get_params(path)[-1]

    def _get_params(self, path):
        param_names = self._param_regex.findall(path)
        return param_names

    def _get_full_url(self, params):
        object_id = params[self.object_arg]
        return self.path.format(**params) + "/{0}".format(object_id)

    def _initialize_extra_view_descriptions(self, view_descs):
        self.extra_views = []
        for view_desc in view_descs:
            if isinstance(view_desc, dict):
                result = view_desc
            else:
                result = {"name": "get_" + view_desc, "path": view_desc}
            if "scope" not in result:
                result["scope"] = "aggregate"
            if "method" not in result:
                result["method"] = "get"
            self.extra_views.append(result)

    def get_list_request(self, **kwargs):
        relative_path = self.path.format(**kwargs)
        return KazooRequest(relative_path)

    def get_object_request(self, **kwargs):
        return KazooRequest(self._get_full_url(kwargs))

    def get_update_object_request(self, **kwargs):
        return KazooRequest(self._get_full_url(kwargs), method='post')

    def get_delete_object_request(self, **kwargs):
        return KazooRequest(self._get_full_url(kwargs), method='delete')

    def get_create_object_request(self, **kwargs):
        return KazooRequest(self.path.format(**kwargs), method='put')

    def get_extra_view_request(self, viewname, **kwargs):
        view_desc = None
        for desc in self.extra_views:
            if desc["path"] == viewname:
                view_desc = desc
        if view_desc is None:
            raise ValueError("Unknown extra view name {0}".format(viewname))
        if view_desc["scope"] == "aggregate":
            return KazooRequest(self.path.format(**kwargs) + "/" + viewname,
                                method=view_desc["method"])
        return KazooRequest(self._get_full_url(kwargs) + "/" + viewname,
                            method=view_desc["method"])

    @property
    def plural_name(self):
        if self._plural_name:
            return self._plural_name
        return self.name + "s"
