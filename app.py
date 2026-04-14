from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS
import io
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 85))
        width = request.form.get('width')
        height = request.form.get('height')
        
        # Open PDF
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        output_pdf = fitz.open()
        
        for page_num in range(pdf_document.page_count):
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
        
        return send_file(output, mimetype='application/pdf', as_attachment=False, download_name='compressed.pdf')
    
    except Exception as e:
        print(f"Error in compress_pdf: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/pdf-preview', methods=['POST'])
def pdf_preview():
    try:
        file = request.files['file']
        
        # Open PDF and get first page
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if pdf_document.page_count == 0:
            return jsonify({'error': 'PDF has no pages'}), 400
            
        page = pdf_document[0]
        
        # Render first page as image for preview (higher quality for preview)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        
        pdf_document.close()
        
        return send_file(io.BytesIO(img_data), mimetype='image/png')
    
    except Exception as e:
        print(f"Error in pdf_preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-pdf-dimensions', methods=['POST'])
def get_pdf_dimensions():
    try:
        file = request.files['file']
        
        # Open PDF and get first page dimensions
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if pdf_document.page_count == 0:
            return jsonify({'error': 'PDF has no pages'}), 400
            
        page = pdf_document[0]
        
        width = int(page.rect.width)
        height = int(page.rect.height)
        
        pdf_document.close()
        
        return jsonify({'width': width, 'height': height})
    
    except Exception as e:
        print(f"Error in get_pdf_dimensions: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
