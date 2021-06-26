import jinja2
import pdfkit

def render_html(row):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath="app/templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "layout.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        apiname=row.apiname,
        apiurl=row.apiurl,
        apidata=row.apidata,
        apiid=row.apiid,
        )

    html_path = f'app/pdf/{row.apiname}.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    print(f"Now converting {row.apiname} ... ")
    pdf_path = f'app/pdf./{row.apiname}.pdf'
    html2pdf(html_path, pdf_path)

def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    path_wk = r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options, configuration=config)
