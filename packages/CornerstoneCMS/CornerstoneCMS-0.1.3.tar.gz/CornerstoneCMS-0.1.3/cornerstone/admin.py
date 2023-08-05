import inspect
import re
from pathlib import Path

from unidecode import unidecode
from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from wtforms import TextAreaField, PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets import TextArea

from cornerstone.models import User, Page, Sermon, Topic, Preacher, session
from cornerstone.settings import get_all_settings, has_setting, save_setting


def _create_slug(title):
    """
    Convert the title to a slug
    """
    return re.sub(r'\W+', '-', unidecode(title).lower()).strip('-')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthorizedMixin(object):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('/'))
        else:
            return redirect(url_for('user.login', next=request.url))


class AuthorizedAdminIndexView(AuthorizedMixin, AdminIndexView):
    pass


class AuthorizedModelView(AuthorizedMixin, ModelView):
    extra_js = ['//cdn.ckeditor.com/4.11.4/full/ckeditor.js']
    column_exclude_list = ('password',)
    column_descriptions = {
        'weight': 'Use this to order items in the menu'
    }
    form_excluded_columns = ('slug',)
    form_overrides = {
        'password': PasswordField,
        'weight': IntegerField
    }

    def on_model_change(self, form, model, is_create):
        if isinstance(model, Page):
            model.slug = _create_slug(model.title)


class SettingsView(AuthorizedMixin, BaseView):
    @expose('/', methods=['GET'])
    def index(self):
        settings = get_all_settings()
        return self.render('admin/settings.html', settings=settings)

    @expose('/', methods=['POST'])
    def index_post(self):
        for key, value in request.form.items():
            if has_setting(key):
                save_setting(key, value)
        return redirect(self.get_url('settings.index'))


def _get_template_mode():
    """
    Detect template mode. This allows us to use the bootstrap4 theme if it exists, and fall back to bootstrap3.

    NB: This is a temporary workaround until the Bootstrap 4 branch merges into Flask-Admin master
    """
    templates_path = Path(inspect.getfile(Admin)).resolve().parent / 'templates'
    if 'bootstrap4' in list(templates_path.iterdir()):
        return 'bootstrap4'
    else:
        return 'bootstrap3'


# Set up the admin
admin = Admin(name='CornerstoneCMS', template_mode=_get_template_mode(), index_view=AuthorizedAdminIndexView())
admin.add_view(AuthorizedModelView(Page, session, name='Pages'))
admin.add_view(AuthorizedModelView(Sermon, session, name='Sermons'))
admin.add_view(AuthorizedModelView(Preacher, session, name='Preachers'))
admin.add_view(AuthorizedModelView(Topic, session, name='Topics'))
admin.add_view(AuthorizedModelView(User, session, name='Users'))
admin.add_view(SettingsView(name='Settings', endpoint='settings'))
