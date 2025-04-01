from jet.dashboard.dashboard import Dashboard
from jet.dashboard import modules
from django.utils.translation import gettext_lazy as _

class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))

        self.children.append(modules.ModelList(
            _('Models'),
            models=('vetclinic.*',),  # Показываем все модели из твоего приложения
            column=1,
            order=1
        ))

        self.children.append(modules.AppList(
            _('Applications'),
            column=2,
            order=2
        ))
