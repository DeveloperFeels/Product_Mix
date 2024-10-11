import os
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)

# Define the folder to store uploaded files temporarily
UPLOAD_FOLDER = '/tmp/uploads'  # Use Render's temporary storage
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_files():
    # Get the uploaded files
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Save the files to the UPLOAD_FOLDER
    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    # Your processing logic goes here...
    # Read the CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Example processing: Replace NULLVALUE and "-" with 0 in specific columns
    for df in [df1, df2]:
        df[['J', 'K', 'L']] = df[['J', 'K', 'L']].replace({"NULLVALUE": 0, "-": 0})

    # Export iOS tab from Product_Mix_iOS and And tab from Product_Mix_And
    # Assuming 'iOS' and 'And' are the names of the DataFrame
    ios_df = df2  # Product_Mix_iOS
    and_df = df1.iloc[1:]  # Product_Mix_And (omit first row)

    # Append And tab to iOS tab
    result_df = pd.concat([ios_df, and_df], ignore_index=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Output the result as CSV
    result_path = os.path.join(UPLOAD_FOLDER, 'result.csv')
    result_df.to_csv(result_path, index=False)

    # Return the processed file to the user for download
    return send_file(result_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
