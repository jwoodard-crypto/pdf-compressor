from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS
import io
import fitz  # PyMuPDF
import os
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print("Index route accessed")
    return send_from_directory('.', 'index.html')

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    print("=== COMPRESS PDF ENDPOINT HIT ===")
    try:
        if 'file' not in request.files:
            print("ERROR: No file in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        print(f"Quality: {quality}, Width: {width}, Height: {height}")
        
        # Open PDF
        pdf_bytes = file.read()
        print(f"PDF bytes read: {len(pdf_bytes)}")
        
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        print(f"PDF opened, pages: {pdf_document.page_count}")
        
        output_pdf = fitz.open()
        
        for page_num in range(pdf_document.page_count):
            print(f"Processing page {page_num + 1}/{pdf_document.page_count}")
            page = pdf_document[page_num]
            
            # Calculate DPI based on quality (72-300 DPI range)
            dpi = 72 + (quality / 100) * (300 - 72)
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to image
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to JPEG bytes with quality
            img_bytes = pix.tobytes("jpeg", quality=quality)
            
            # Create new page with compressed image
            img_pdf = fitz.open(stream=img_bytes, filetype="jpeg")
            
            # Get dimensions for new page
            if width and height:
                page_width = float(width)
                page_height = float(height)
            else:
                page_width = page.rect.width
                page_height = page.rect.height
            
            new_page = output_pdf.new_page(width=page_width, height=page_height)
            new_page.show_pdf_page(new_page.rect, img_pdf, 0)
            img_pdf.close()
        
        # Save to bytes
        output = io.BytesIO()
        output_pdf.save(output)
        output.seek(0)
        
        pdf_document.close()
        output_pdf.close()
        
        print(f"Compression complete! Output size: {len(output.getvalue())}")
        
        return send_file(output, mimetype='application/pdf', as_attachment=False, download_name='compressed.pdf')
    
    except Exception as e:
        print(f"ERROR in compress_pdf: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/get-pdf-dimensions', methods=['POST'])
def get_pdf_dimensions():
    print("=== GET PDF DIMENSIONS ENDPOINT HIT ===")
    try:
        if 'file' not in request.files:
            print("ERROR: No file in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        # Open PDF and get first page dimensions
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if pdf_document.page_count == 0:
            return jsonify({'error': 'PDF has no pages'}), 400
            
        page = pdf_document[0]
        
        width = int(page.rect.width)
        height = int(page.rect.height)
        
        print(f"Dimensions: {width} x {height}")
        
        pdf_document.close()
        
        return jsonify({'width': width, 'height': height})
    
    except Exception as e:
        print(f"ERROR in get_pdf_dimensions: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
