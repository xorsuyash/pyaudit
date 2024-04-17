from flask import Flask, request, jsonify,render_template,send_file
from werkzeug.utils import secure_filename
from Crypto.PublicKey import RSA 
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256 
import base64 
import os

UPLOAD_FOLDER='uploads'
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify',methods=['POST'])
def verify_signature():

    file_data=request.files['file']
    uploaded_signature=request.files['signature']
    public_key=request.form['public_key']

    #savinig the files 
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file_data.filename))
    signature_path=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_signature.filename))
    file_data.save(file_path)
    uploaded_signature.save(signature_path)


    key=RSA.import_key(public_key)

    with open(file_path,'rb') as f:
        file_hash=SHA256.new(file_data.read())


    verifier=pkcs1_15.new(key)

    try:
        with open(signature_path,'rb') as f:
            signature=f.read()
        verifier.verify(file_hash,base64.b64decode(signature))
        result={'verifies':True}
    except Exception as e:
        result ={'verified':False,'error': str(e)}
    
    os.remove(file_path)
    os.remove(signature_path)
    
    return jsonify(result)
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)
