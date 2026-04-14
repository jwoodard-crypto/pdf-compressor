from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS
from PIL import Image
import io
import fitz  # PyMuPDF
import os
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/compress-image', methods=['POST'])
def compress_image():
    print("=== COMPRESS IMAGE ENDPOINT HIT ===")
    try:
        file = request.files['file']
        format = request.form.get('format', 'JPEG').upper()
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        print(f"Image: {file.filename}, Format: {format}, Quality: {quality}")
        
        img = Image.open(file.stream)
        
        if width and height:
            img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        
        if format == 'PNG':
            img.save(output, format='PNG', optimize=True)
        elif format == 'WEBP':
            img.save(output, format='WEBP', quality=quality)
        else:  # JPEG
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            img.save(output, format='JPEG', quality=quality, optimize=True)
        
        output.seek(0)
        
        mime_type = f'image/{format.lower()}'
        print(f"Image compressed successfully")
        
        return send_file(output, mimetype=mime_type)
    
    except Exception as e:
        print(f"ERROR in compress_image: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    print("=== COMPRESS PDF ENDPOINT HIT ===")
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        print(f"PDF: {file.filename}, Quality: {quality}, Width: {width}, Height: {height}")
        
        # Open PDF
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        output_pdf = fitz.open()
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # Calculate DPI based on quality
            dpi = 72 + (quality / 100) * (300 - 72)
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to image
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("jpeg", quality=quality)
            
            # Create new page
            img_pdf = fitz.open(stream=img_bytes, filetype="jpeg")
            
            if width and height:
                page_width = float(width)
                page_height = float(height)
            else:
                page_width = page.rect.width
                page_height = page.rect.height
            
            new_page = output_pdf.new_page(width=page_width, height=page_height)
            new_page.show_pdf_page(new_page.rect, img_pdf, 0)
            img_pdf.close()
        
        output = io.BytesIO()
        output_pdf.save(output)
        output.seek(0)
        
        pdf_document.close()
        output_pdf.close()
        
        print(f"PDF compressed successfully")
        
        return send_file(output, mimetype='application/pdf')
    
    except Exception as e:
        print(f"ERROR in compress_pdf: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/get-pdf-dimensions', methods=['POST'])
def get_pdf_dimensions():
    try:
        file = request.files['file']
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = pdf_document[0]
        
        width = int(page.rect.width)
        height = int(page.rect.height)
        
        pdf_document.close()
        
        return jsonify({'width': width, 'height': height})
    
    except Exception as e:
        print(f"ERROR in get_pdf_dimensions: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
