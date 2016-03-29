from flask import flash, redirect, render_template, request
from flask_bootstrap import Bootstrap
from scadsui import app
from scadsui.forms import HandbagWorkflowForm

import json
import requests


bootstrap = Bootstrap(app)
scads_url = app.config['SCADS_URL']


@app.route('/')
def index():
    workflows = []
    i = 0
    wf_list = requests.get(scads_url + 'workflows').json()
    for wf_url in wf_list['workflows']:
        wf = requests.get(wf_url).json()
        workflows.append(wf)
        workflows[i]['id'] = wf_url[44:]
        i += 1
    return render_template('index.html', url=scads_url, workflows=workflows)


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
        post_to_scads(profile, scads_url + 'workflows?agent=anon')
        flash('Profile "%s" created' % (form.name.data))
        return redirect('/')
    return render_template('handbag.html', form=form, status="New")


@app.route('/handbag/<wf_id>', methods=['GET', 'POST'])
def handbag_edit_workflow(wf_id):
    url = scads_url + 'workflow?id=' + wf_id
    wf = requests.get(url).json()
    wf['maxBagSize'] = int(wf['maxBagSize'] / 1000000000)
    form = HandbagWorkflowForm(**wf)
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
        post_to_scads(profile, scads_url + 'workflows')
        flash('Profile "%s" updated' % (form.name.data))
        return redirect('/')
    return render_template('handbag.html', form=form, status="Edit")


def process_results(results, md):
    r = results
    r['maxBagSize'] = r['maxBagSize'] * 1000000000
    r.pop('addMetadata')
    r.pop('delMetadata')
    r['metadata'] = md
    return r


def post_to_scads(profile, url):
    r = requests.post(url, data=json.dumps(profile))
    return r
