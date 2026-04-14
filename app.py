from flask import Flask, request, send_file, send_from_directory
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
    file = request.files['file']
    quality = int(request.form.get('quality', 85))
    width = request.form.get('width')
    height = request.form.get('height')
    
    # Open PDF
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    output_pdf = fitz.open()
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        
        # Calculate DPI based on quality (72-300 DPI range)
        dpi = 72 + (quality / 100) * (300 - 72)
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page to image
        pix = page.get_pixmap(matrix=mat)
        
        # Resize if dimensions provided
        if width and height:
            # PyMuPDF can resize pixmaps directly
            target_width = int(width)
            target_height = int(height)
            
            # Create new pixmap with target dimensions
            # Convert to PIL-compatible format for resizing
            img_data = pix.tobytes("png")
            
            # Use PyMuPDF to create resized image
            temp_pdf = fitz.open("pdf", img_data)
            temp_page = temp_pdf[0]
            
            # Calculate scale to fit target dimensions
            scale_x = target_width / pix.width
            scale_y = target_height / pix.height
            resize_mat = fitz.Matrix(scale_x, scale_y)
            
            pix = temp_page.get_pixmap(matrix=resize_mat)
            temp_pdf.close()
        
        # Convert to JPEG bytes with quality
        img_bytes = pix.tobytes("jpeg", quality=quality)
        
        # Create new page with compressed image
        img_pdf = fitz.open(stream=img_bytes, filetype="jpeg")
        
        # Get dimensions for new page
        if width and height:
            page_width = int(width)
            page_height = int(height)
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
    
    return send_file(output, mimetype='application/pdf')

@app.route('/pdf-preview', methods=['POST'])
def pdf_preview():
    file = request.files['file']
    
    # Open PDF and get first page
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    page = pdf_document[0]
    
    # Render first page as image for preview
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_data = pix.tobytes("png")
    
    pdf_document.close()
    
    return send_file(io.BytesIO(img_data), mimetype='image/png')

@app.route('/get-pdf-dimensions', methods=['POST'])
def get_pdf_dimensions():
    file = request.files['file']
    
    # Open PDF and get first page dimensions
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    page = pdf_document[0]
    
    width = int(page.rect.width)
    height = int(page.rect.height)
    
    pdf_document.close()
    
    return {'width': width, 'height': height}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
