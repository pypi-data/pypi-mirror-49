from __future__ import unicode_literals

from django.db import models


class MensagemSms(models.Model):
    id = models.AutoField(db_column='IDMensagemSMS', primary_key=True)
    numero_celular = models.IntegerField(db_column='NumeroCelular')
    mensagem = models.CharField(db_column='TextoMensagem', max_length=140)
    tipo_sms = models.IntegerField(db_column='IDTipoSMS')

    class Meta:
        managed = True
        db_table = 'mensagemsms'

