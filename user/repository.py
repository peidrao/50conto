from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin


class ProcessFormView(View):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class CreateView(ProcessFormView, ModelFormMixin):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
