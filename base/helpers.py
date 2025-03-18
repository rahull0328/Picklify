from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.conf import settings  

def save_pdf(params: dict):
    try:
        template = get_template('receipt/invoice.html')
        html = template.render(params)

        # Create a BytesIO buffer to store the PDF
        result = BytesIO()

        # Generate PDF
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

        if pdf.err:
            return '', False

        # Generating a unique file name
        file_name = f"{uuid.uuid4()}.pdf"
        file_path = str(settings.BASE_DIR) + f"/public/static/{file_name}.pdf"

        # Save the PDF file
        with open(file_path, 'wb+') as output:
            output.write(result.getvalue())

        return file_name, True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return '', False