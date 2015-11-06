from flask import flash, redirect, render_template, request
from scadsui import app
from scadsui.forms import HandbagWorkflowForm
import json
import requests
import config as cfg
from flask_bootstrap import Bootstrap


app.config.from_object('config')
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'temp_key'
bootstrap = Bootstrap(app)
if app.config['TESTING'] == False:
    SCADS_URL = cfg.PROD_SCADS_URL


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handbag', methods=['GET', 'POST'])
def handbag():
    form = HandbagWorkflowForm()

    if form.addMetadata.data:
        form.metadata.append_entry()
    elif form.delMetadata.data:
        if form.metadata.data:
            form.metadata.pop_entry()
        else:
            flash('No metadata fields to delete')
    elif request.form and form.validate():
        metadata = []
        while form.metadata.data:
            m = form.metadata.pop_entry().data
            if m['presetValue'] == '':
                m.pop('presetValue')
            metadata.insert(0, m)
        results = form.data
        profile = process_results(results, metadata)
        post_to_scads(profile, SCADS_URL)
        flash('Profile "%s" created' % (form.name.data))
        return redirect('/')
    return render_template('handbag.html', form=form)


def process_results(results, md):
    r = results
    r.pop('addMetadata')
    r.pop('delMetadata')
    r['metadata'] = md
    return r


def post_to_scads(profile, url):
    r = requests.post(url, data=json.dumps(profile))
    return r
