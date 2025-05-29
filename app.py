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
    
    # Ensure print.css exists
    css_path = os.path.join(app.root_path, 'static', 'print.css')
    if not os.path.exists(css_path):
        with open(css_path, 'w') as f:
            f.write("""
@page {
    size: A4;
    margin: 0;
}

body {
    margin: 20px;
    font-family: Arial, sans-serif;
    color: #222;
}

h1, h2, h3 {
    margin-bottom: 5px;
}

h1 {
    font-size: 28px;
}

h2 {
    font-size: 20px;
    margin-top: 20px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
}

.section {
    margin-bottom: 20px;
}

.info {
    margin-bottom: 10px;
    font-size: 14px;
}

ul {
    padding-left: 20px;
}

li {
    margin-bottom: 6px;
}

.job-title {
    font-weight: bold;
}

.date-range {
    font-style: italic;
    font-size: 14px;
}

.inline-list span {
    margin-right: 20px;
}
            """)
    app.run(debug=True)
