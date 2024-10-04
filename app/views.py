from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import ArquivoForm
import PyPDF2
import zipfile
from docx import Document
import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        return render(request, 'index.html')

class ConversaoView(View):
    def get(self, request):
        form = ArquivoForm()
        return render(request, 'conversao.html', {'form': form})

    def post(self, request):
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['arquivo']
            base_name = uploaded_file.name.rsplit('.', 1)[0]  # Nome base do arquivo sem extensão

            if uploaded_file.name.endswith('.pdf'):
                # Converter PDF para DOCX
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                doc = Document()
                txt_content = []

                for page in pdf_reader.pages:
                    text = page.extract_text()
                    doc.add_paragraph(text)
                    txt_content.append(text)

                # Salvar como DOCX
                docx_io = io.BytesIO()
                doc.save(docx_io)
                docx_io.seek(0)

                # Salvar como TXT
                txt_io = io.BytesIO()
                txt_io.write("\n".join(txt_content).encode('utf-8'))
                txt_io.seek(0)

                # Retornar os arquivos
                response_zip = HttpResponse(content_type='application/zip')
                response_zip['Content-Disposition'] = f'attachment; filename="{base_name}.zip"'
                
                with zipfile.ZipFile(response_zip, 'w') as zf:
                    zf.writestr(f"{base_name}.docx", docx_io.getvalue())
                    zf.writestr(f"{base_name}.txt", txt_io.getvalue())

                return response_zip

            elif uploaded_file.name.endswith('.docx'):
                # Converter DOCX para PDF
                doc = Document(uploaded_file)
                pdf_io = io.BytesIO()
                c = canvas.Canvas(pdf_io, pagesize=letter)
                width, height = letter
                txt_content = []

                for paragraph in doc.paragraphs:
                    text = paragraph.text
                    c.drawString(72, height - 72, text)  # Margem de 1 polegada
                    height -= 12  # Mover para baixo
                    txt_content.append(text)

                c.save()
                pdf_io.seek(0)

                # Salvar como TXT
                txt_io = io.BytesIO()
                txt_io.write("\n".join(txt_content).encode('utf-8'))
                txt_io.seek(0)

                # Retornar os arquivos
                response_zip = HttpResponse(content_type='application/zip')
                response_zip['Content-Disposition'] = f'attachment; filename="{base_name}.zip"'

                with zipfile.ZipFile(response_zip, 'w') as zf:
                    zf.writestr(f"{base_name}.pdf", pdf_io.getvalue())
                    zf.writestr(f"{base_name}.txt", txt_io.getvalue())

                return response_zip

            else:
                messages.error(request, "Formato de arquivo não suportado.")
                return redirect('conversao')

        return render(request, 'conversao.html', {'form': form})
