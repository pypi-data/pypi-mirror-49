O que há neste pacote?
============

Managers com funcionalidades extras para os models Django.

Prefetch:
------------

Manager para carregar por default os relacionamentos, como se fossem chamados os métodos select_related ou prefetch_related

~~~python
from lins_dbmanagers.prefetch import PrefetchManager

class Modulo(models.Model):
    class Meta:
        managed = False
        db_table = 'transferenciasmodulos'
        ordering = ['-id']

    transferencia = models.ForeignKey(Transferencia,
                                      db_column='IDTransferencia',
                                      on_delete=models.DO_NOTHING,
                                      related_name='modulo')
    
    objects = PrefetchManager(select_related=('transferencia',))
~~~~