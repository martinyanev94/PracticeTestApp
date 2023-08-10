
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text()
            print(text)
            return render_template('result.html', text=text)

    return render_template('upload.html')