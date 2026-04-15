from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS
from PIL import Image
import io
import fitz  # PyMuPDF
import os
import traceback
import sys

app = Flask(__name__)
CORS(app)

# Enable debug logging
app.config['DEBUG'] = True

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/compress-image', methods=['POST'])
def compress_image():
    print("=== COMPRESS IMAGE ENDPOINT HIT ===", flush=True)
    try:
        file = request.files['file']
        format = request.form.get('format', 'JPEG').upper()
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        print(f"Image: {file.filename}, Format: {format}, Quality: {quality}", flush=True)
        
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
        print(f"Image compressed successfully", flush=True)
        
        return send_file(output, mimetype=mime_type)
    
    except Exception as e:
        error_msg = f"ERROR in compress_image: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, flush=True)
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'type': type(e).__name__
        }), 500

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    print("=== COMPRESS PDF ENDPOINT HIT ===", flush=True)
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        print(f"PDF: {file.filename}, Quality: {quality}, Width: {width}, Height: {height}", flush=True)
        
        # Open PDF
        pdf_bytes = file.read()
        print(f"Read {len(pdf_bytes)} bytes from uploaded file", flush=True)
        
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        print(f"Opened PDF with {pdf_document.page_count} pages", flush=True)
        
        output_pdf = fitz.open()
        
        for page_num in range(pdf_document.page_count):
            print(f"Processing page {page_num + 1}/{pdf_document.page_count}", flush=True)
            page = pdf_document[page_num]
            
            # Calculate DPI based on quality
            dpi = 72 + (quality / 100) * (300 - 72)
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            print(f"Rendering page at DPI: {dpi}, zoom: {zoom}", flush=True)
            
            # Render page to image - NOTE: tobytes() doesn't accept quality parameter
            pix = page.get_pixmap(matrix=mat)
            
            # Convert pixmap to PIL Image so we can control JPEG quality
            img_data = pix.tobytes("jpeg")  # No quality parameter here!
            pil_img = Image.open(io.BytesIO(img_data))
            
            # Now compress with PIL which DOES support quality
            img_bytes_io = io.BytesIO()
            pil_img.save(img_bytes_io, format='JPEG', quality=quality, optimize=True)
            img_bytes = img_bytes_io.getvalue()
            
            print(f"Rendered and compressed page to {len(img_bytes)} bytes", flush=True)
            
            # Determine page dimensions
            if width and height:
                page_width = float(width)
                page_height = float(height)
            else:
                page_width = page.rect.width
                page_height = page.rect.height
            
            print(f"Creating new page with dimensions: {page_width}x{page_height}", flush=True)
            
            # Create new page and insert the compressed image
            new_page = output_pdf.new_page(width=page_width, height=page_height)
            
            # Insert the JPEG image directly into the page
            new_page.insert_image(new_page.rect, stream=img_bytes)
            
            print(f"Inserted image into page {page_num + 1}", flush=True)
        
        print("Saving output PDF", flush=True)
        output = io.BytesIO()
        output_pdf.save(output)
        output.seek(0)
        
        pdf_document.close()
        output_pdf.close()
        
        print(f"PDF compressed successfully, output size: {len(output.getvalue())} bytes", flush=True)
        
        return send_file(output, mimetype='application/pdf')
    
    except Exception as e:
        error_msg = f"ERROR in compress_pdf: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, flush=True)
        sys.stdout.flush()
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'type': type(e).__name__
        }), 500

@app.route('/get-pdf-dimensions', methods=['POST'])
def get_pdf_dimensions():
    print("=== GET PDF DIMENSIONS ENDPOINT HIT ===", flush=True)
    try:
        file = request.files['file']
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = pdf_document[0]
        
        width = int(page.rect.width)
        height = int(page.rect.height)
        
        print(f"PDF dimensions: {width}x{height}", flush=True)
        
        pdf_document.close()
        
        return jsonify({'width': width, 'height': height})
    
    except Exception as e:
        error_msg = f"ERROR in get_pdf_dimensions: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, flush=True)
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'type': type(e).__name__
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}", flush=True)
    app.run(host='0.0.0.0', port=port)
