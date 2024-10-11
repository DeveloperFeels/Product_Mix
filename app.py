from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'Templates'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for the upload page
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Handle file upload and processing
@app.route('/', methods=['POST'])
def upload_files():
    # Get the uploaded files
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Save the files to the upload folder
    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
    file1.save(file1_path)
    file2.save(file2_path)

    # Process the CSV files
    and_csv = pd.read_csv(file1_path)
    ios_csv = pd.read_csv(file2_path)

    # Replace 'NULLVALUE' and '-' with 0 in columns J, K, L
    columns_to_replace = ['J', 'K', 'L']
    and_csv[columns_to_replace] = and_csv[columns_to_replace].replace(['NULLVALUE', '-'], 0)
    ios_csv[columns_to_replace] = ios_csv[columns_to_replace].replace(['NULLVALUE', '-'], 0)

    # Merge the two CSVs: Append 'And' tab (file1) to 'iOS' tab (file2), skipping the first row of 'And'
    and_tab_no_header = and_csv.iloc[1:]  # Skip the first row (header)
    merged_df = pd.concat([ios_csv, and_tab_no_header], ignore_index=True)

    # Trim whitespace from all columns
    merged_df = merged_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Save the result as a CSV file
    output_file = os.path.join(UPLOAD_FOLDER, 'merged_product_mix.csv')
    merged_df.to_csv(output_file, index=False)

    # Send the resulting file for download
    return send_file(output_file, as_attachment=True, download_name='merged_product_mix.csv')

if __name__ == '__main__':
    app.run(debug=True)
