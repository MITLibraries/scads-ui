from __future__ import absolute_import


def test_index_page_loads(testapp):
    response = testapp.get('/')
    assert response.status_code == 200


def test_form_loads(testapp):
    response = testapp.get('/handbag')
    assert 'form' in response


def test_add_and_delete_metadata_field(testapp):
    handbag_page = testapp.get('/handbag')
    form = handbag_page.form
    assert 'metadata-item' in handbag_page
    delete = form.submit('delMetadata')
    assert 'metadata-item' not in delete
    add = form.submit('addMetadata')
    assert 'metadata-item' in add


def test_submit_valid_form(app, testapp):
    form = testapp.get('/handbag').form
    form['name'] = 'test'
    form['destinationName'] = 'test'
    form['destinationUrl'] = 'file:///safadf'
    form['destinationEmail'] = 'test@test.com'
    form['bagNameGenerator'] = 'test'
    form['packageFormat'] = 'zip'
    results = form.submit()
    print(results)
    assert results.status_code == 302
