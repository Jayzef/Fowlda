from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from .forms import *
import PyPDF2
from docx import Document
import io
from django.http import HttpResponse

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    def post(self, request):
        return render(request, 'index.html')
    
class ConversaoView(View):
    def get(self, request):
        form = ArquivoForm(request.POST, request.FILES)
        return render(request, 'conversao.html', {'form':form})

    def post(self, request):
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['arquivo']
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            doc = Document()
            for page in pdf_reader.pages:
                doc.add_paragraph(page.extract_text())

            docx_io = io.BytesIO()
            doc.save(docx_io)
            docx_io.seek(0)

            response = HttpResponse(
                docx_io,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename="arquivo.docx"'
            form.save()
            return response
        else:
            form = ArquivoForm()
        return render(request, 'conversao.html', {'form':form})