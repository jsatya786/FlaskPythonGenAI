"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, send_file
from FlaskWebProject_appConfig import app
from FlaskWebProject_appConfig.items_view import items_bp
from flask import Flask
from FlaskWebProject_appConfig.external_data_view import external_data_bp
from FlaskWebProject_appConfig.text_generation_view import text_generation_bp
from FlaskWebProject_appConfig.text_to_image import text_to_image_bp
import io
import base64

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# Register the blueprint
app.register_blueprint(items_bp)

if __name__ == '__main__':
    app.run(debug=True)

# Register the blueprints

app.register_blueprint(external_data_bp)

if __name__ == '__main__':
    app.run(debug=True)

app.register_blueprint(text_generation_bp, url_prefix='/text-generation')

if __name__ == '__main__':
    app.run(debug=True)

app.register_blueprint(text_to_image_bp, url_prefix='/text_to_image')

if __name__ == '__main__':
    app.run(debug=True)
    
app = Flask(__name__)