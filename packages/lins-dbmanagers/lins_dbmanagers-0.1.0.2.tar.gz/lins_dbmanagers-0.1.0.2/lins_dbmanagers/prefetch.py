from django.db import models


class PrefetchManager(models.Manager):
    """
    Manager para carregar por default os relacionamentos, como se fossem chamados os métodos
     select_related ou prefetch_related
    """
    def __init__(self, *args, **kwargs):
        self._select_related = kwargs.pop('select_related', None)
        self._prefetch_related = kwargs.pop('prefetch_related', None)

        super(PrefetchManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(PrefetchManager, self).get_queryset(*args, **kwargs)

        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)

        return qs
