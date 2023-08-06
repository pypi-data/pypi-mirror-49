from .models.mensagem_sms import MensagemSms

def enviar_sms(telefone, mensagem, tipo):
    sms = MensagemSms(numero_celular=telefone, tipo_sms=tipo, mensagem=mensagem)
    sms.save()
    return sms