from django.db import models

class Usuario(models.Model):
    email = models.CharField(max_length=100, verbose_name="E-mail")
    senha = models.CharField(max_length=100, verbose_name="Senha")
    perfil = models.BooleanField(verbose_name="Perfil do usuário")
    def __str__(self):
            return f"'Usuário:' {self.email}"
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Formato(models.Model):
     extensao = models.CharField(max_length=10, verbose_name="Extensão")
     def __str__(self):
          return f"{self.extensao}"
     class Meta:
        verbose_name = "Formato"
        verbose_name_plural = "Formatos"

class Arquivo(models.Model):
     arquivo = models.FileField(upload_to='app/static/files')
     def __str__(self):
          return f"'Arquivo: {self.arquivo} "
     class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

class Conversao(models.Model):
     arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE, verbose_name="Arquivo", null=True)
     nome_arquivo = models.CharField(max_length=255, verbose_name="Nome do Arquivo")
     tamanho = models.FloatField(verbose_name="Tamanho")
     data_conversao = models.DateField(verbose_name="Data")
     status = models.BooleanField(verbose_name="Status")
     fconvertido = models.CharField(max_length=10, verbose_name="Formato Convertido")
     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Nome do Usuário")
     foriginal = models.ForeignKey(Formato, on_delete=models.CASCADE, verbose_name="Formato Original")
     def __str__(self):
          return f"'Arquivo: ' {self.nome_arquivo} ' Convertido de: '{self.foriginal} ' para: ' {self.fconvertido}"
     class Meta:
        verbose_name = "Conversão"
        verbose_name_plural = "Conversões"

class Feedback(models.Model):
     mensagem = models.TextField(max_length=255, verbose_name="Mensagem")
     data_feedback = models.DateField(verbose_name="Data do Feedback")
     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Nome do Usuário")
     def __str__(self):
          return f"'O usuário '{self.usuario} ' enviou a mensagem: ' {self.mensagem}"
     class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"