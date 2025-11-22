import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    output_filename = "Selected_Document.txt"
    print(f"Attempting to extract text from: {pdf_path}")

    try:
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"Error: The file '{pdf_path}' was not found in the current directory.")
            return None

        text_content = []
        
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            
            # Iterate through every page
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_content.append(text)
                else:
                    print(f"Warning: Could not extract text from page {i+1}")
        
        # Combine text
        full_raw_text = "\n".join(text_content)
        
        # Collapse extra whitespace:
        # splits the string by whitespace (spaces, tabs, newlines) and joins them back with a single space
        cleaned_text = " ".join(full_raw_text.split())

        # Write to file with UTF-8 encoding
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
            
        print(f"Success! Extracted {len(cleaned_text)} characters.")
        print(f"Saved extracted text to '{output_filename}'")
        return cleaned_text

    except Exception as e:
        print(f"Failure: An error occurred while processing the PDF: {e}")
        return None

def main():
    # Hardcoded PDF path as requested
    # Ensure the file 'Energy_Efficient_AI.pdf' is in your project root
    pdf_path = "Energy_Efficient_AI.pdf" 
    extract_text_from_pdf(pdf_path)

if __name__ == "__main__":
    main()


