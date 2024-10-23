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
import pandas as pd
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
import os
import tempfile

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
    
class ConversaoPLAView(View):
    def get(self, request):
        form = ArquivoForm()
        return render(request, 'conversaoPLA.html', {'form': form})

    def post(self, request):
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['arquivo']
            base_name = uploaded_file.name.rsplit('.', 1)[0]

            if uploaded_file.name.endswith('.ods'):
                # Converter ODS para XLSX
                df = pd.read_excel(uploaded_file, engine='odf')
                xlsx_io = io.BytesIO()
                df.to_excel(xlsx_io, index=False, engine='openpyxl')
                xlsx_io.seek(0)

                response = HttpResponse(xlsx_io, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{base_name}.xlsx"'
                return response

            elif uploaded_file.name.endswith('.xlsx'):
                # Converter XLSX para ODS
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                ods_io = io.BytesIO()

                # Criar um novo documento ODS
                doc = OpenDocumentSpreadsheet()
                table = Table(name="Sheet1")
                doc.spreadsheet.addElement(table)

                for row in df.itertuples(index=False):
                    table_row = TableRow()
                    for value in row:
                        cell = TableCell()
                        # Adicionar texto como elemento ODF
                        text_element = P(text=str(value))
                        cell.addElement(text_element)
                        table_row.addElement(cell)
                    table.addElement(table_row)

                doc.save(ods_io)
                ods_io.seek(0)

                response = HttpResponse(ods_io, content_type='application/vnd.oasis.opendocument.spreadsheet')
                response['Content-Disposition'] = f'attachment; filename="{base_name}.ods"'
                return response

            else:
                messages.error(request, "Formato de arquivo não suportado.")
                return redirect('conversaoPLA')

        return render(request, 'conversaoPLA.html', {'form': form})
    
class ConversaoVIDView(View):
    def get(self, request):
        form = ArquivoForm()
        return render(request, 'conversaoVID.html', {'form': form})

    def post(self, request):
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['arquivo']
            base_name = uploaded_file.name.rsplit('.', 1)[0]

            if uploaded_file.name.endswith('.mp4'):
                # Converter MP4 para MP3
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video_file:
                    for chunk in uploaded_file.chunks():
                        temp_video_file.write(chunk)
                    temp_video_file_name = temp_video_file.name

                # Cria o arquivo de áudio temporário
                audio_io = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                
                # Usa um contexto `with` para garantir que o vídeo esteja fechado antes de usar
                with VideoFileClip(temp_video_file_name) as video_clip:
                    audio_clip = video_clip.audio
                    audio_clip.write_audiofile(audio_io.name)
                    audio_clip.close()  # Fecha o clip de áudio

                # Garantindo que o arquivo de áudio seja fechado antes de abrir
                audio_io.close()

                response = HttpResponse(open(audio_io.name, 'rb'), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{base_name}.mp3"'
                
                # Limpeza de arquivos temporários
                os.remove(temp_video_file_name)
                os.remove(audio_io.name)
                return response

            else:
                messages.error(request, "Formato de arquivo não suportado.")
                return redirect('conversaoVID')

        return render(request, 'conversaoVID.html', {'form': form})
    
class ConversaoIMGView(View):
    def get(self, request):
        return render(request, 'conversaoIMG.html')
    
    def post(self, request):
        return render(request, 'conversaoIMG.html')
    
class HistoricoView(View):
    def get(self, request):
        return render(request, 'historico.html')
    
    def post(self, request):
        return render(request, 'historico.html')