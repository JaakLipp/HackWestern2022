#imports for use in web display
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from machine import getter
from machine import bruh
from machine.bruh import Trainer


model_class = bruh.Trainer()
model_class.trainer()

#the location of the folder where user uploads go
UPLOAD_FOLDER = 'uploads' 

#only accept certain formatted files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#initialize app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    #helper function to determine if a file is of the correct format
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/result/<image>')
def result(image):
    done = getter.get_doneness(image, model_class)
    os.remove(image)
    return render_template('result.html', doneness=str(done))


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('error.html')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('empty.html')
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            try:
                file.save('uploads/' + os.path.join(filename))
                return result('uploads/' + os.path.join(filename))
            except:
                file.save('HackWestern2022/uploads/' + os.path.join(filename))
                return result('HackWestern2022/uploads/' + os.path.join(filename))
            # #redirects to the results page when a valid input is given

        elif not (allowed_file(file.filename)):
            return render_template('error.html')

    #reloads the page if the user submits nothing    
    return render_template('index.html')

if __name__ == '__main__':
    #mandatory initializations
    
    app.secret_key = 'the random string'
    server_port = os.environ.get('PORT', '8082')
    app.run(port=int(os.environ.get("PORT", 8082)),host='0.0.0.0',debug=True)
