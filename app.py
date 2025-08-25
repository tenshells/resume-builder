from flask import Flask, render_template, send_file
import os
from weasyprint import HTML, CSS # Ensure WeasyPrint is installed (pip install WeasyPrint)
from shel_resume import SHEL_RESUME_DATA

app = Flask(__name__)

@app.route('/view_resume')
def view_resume():
    # You can later change this to accept dynamic data (via query or session)
    return render_template('resume_template.html', **SHEL_RESUME_DATA)

@app.route('/download_resume')
def download_resume():
    # Generate HTML content
    html_content = render_template('resume_template.html', **SHEL_RESUME_DATA)
    
    # Get the print CSS
    css_path = os.path.join(app.root_path, 'static', 'print.css')
    
    # Generate PDF with custom CSS
    pdf_filename = os.path.join(app.root_path, 'static', 'resume.pdf')
    HTML(string=html_content).write_pdf(
        pdf_filename,
        stylesheets=[CSS(filename=css_path)]
    )
    
    # Send PDF file
    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    # Ensure the static directory exists for PDF output
    if not os.path.exists(os.path.join(app.root_path, 'static')):
        os.makedirs(os.path.join(app.root_path, 'static'))
    
    app.run(debug=True)
