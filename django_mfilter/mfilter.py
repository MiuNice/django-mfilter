class MFields(object):
    def __init__(self, fields):
        self.fields = fields

    def __getitem__(self, index):
        fields = list()
        for i in self.fields:
            fields.append(i.name)
            if i.__class__.__name__ == "ForeignKey":
                fields.append(i.name + "_id")
        return fields[index]


class XFilter:
    pass


class MFilter(XFilter):
    def __init__(self, request, model, params=dict()):
        self.model = model
        self.params = params
        if params:
            self.params = params
        else:
            self.params = self.request_params(request)

        self.funcs = dict()
        self.rename = dict()
        self.operate = dict()

        self.fields = MFields(self.model_field(self.model))

    @staticmethod
    def do_nothing(value):
        return value

    @staticmethod
    def model_field(model):
        return model._meta.fields

    @staticmethod
    def request_params(request):
        http_params = dict()

        method = request.method
        if method == "GET":
            # django.http.request.QueryDict
            http_params = request.GET

        return http_params

    def _rename(self):
        new_name = dict()
        if self.rename:
            for key, value in self.params.items():
                if key in self.rename:
                    key = self.rename[key]
                new_name[key] = value
            self.params = new_name

    def _get_operate(self, key):
        return self.operate.get(key, "")

    def filter_params(self):
        if not self.params:
            return dict()

        self._rename()

        _filter_params = dict()
        for key, value in self.params.items():
            if key in self.fields:
                value = self.funcs.get(key, self.do_nothing)(value)
                _filter_params[key + self._get_operate(key)] = value

        return _filter_params

    # set 函数未来可能更加饱满，现（在）不封装
    def set_funcs(self, *args, **kwargs):
        if args:
            self.funcs = args[0]
        else:
            self.funcs = kwargs
        return self

    def set_rename(self, *args, **kwargs):
        if args:
            self.rename = args[0]
        else:
            self.rename = kwargs
        return self

    def set_operate(self, *args, **kwargs):
        if args:
            self.operate = args[0]
        else:
            self.operate = kwargs
        return self
