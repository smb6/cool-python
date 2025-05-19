import PyPDF2


def remove_pdf_password(input_pdf, output_pdf, password):
    # Open the input PDF file in binary read mode
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Check if the PDF is encrypted and attempt decryption
        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 0:
                print("Incorrect password provided!")
                return
        else:
            print("The PDF file is not encrypted.")
            return

        writer = PyPDF2.PdfWriter()
        # Loop through each page and add it to the writer
        for page in reader.pages:
            writer.add_page(page)

    # Write out the new PDF file without encryption
    with open(output_pdf, 'wb') as new_file:
        writer.write(new_file)

    print(f"PDF saved without password as '{output_pdf}'.")


if __name__ == '__main__':
    # Replace these with your file paths and password
    input_file = ""  # Path to your encrypted PDF
    output_file = ""  # Path for the output unencrypted PDF
    pdf_password = ""  # The password to decrypt the PDF

    remove_pdf_password(input_file, output_file, pdf_password)
