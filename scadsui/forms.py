from flask.ext.wtf import Form
from wtforms import (BooleanField, FieldList, FormField, IntegerField,
                     SelectField, StringField, SubmitField, validators)


class HandbagMetadataForm(Form):
    """ Sub form class for characterizing metadata fields.
    """
    name = StringField('Field name', [validators.InputRequired()],
                       default='Bag-Creator')
    presetValue = StringField('Preset value', description='smithkr@mit.edu',
                              default=None)
    optional = BooleanField('Optional')
    sticky = BooleanField('Sticky')


class HandbagWorkflowForm(Form):
    """ Form class defining metadata fields requiring user input to generate a
        workflow for the Handbag tool.
    """
    name = StringField('Profile name', [validators.InputRequired()],
                       description='Ex: IASC Accession')
    # version = ndb.IntegerProperty(default=1)
    destinationName = StringField('Destination name',
                                  [validators.InputRequired()],
                                  description='Archives/Submission')
    destinationUrl = StringField('Destination URL',
                                 [validators.InputRequired(),
                                  validators.Regexp('file:///.*')],
                                 default=('Mac ex: file:///Volumes/Archives/'
                                          'Submission     Windows ex: file:///'
                                          'Z:\Submission'))
    destinationEmail = StringField('Notification email recipient',
                                   [validators.InputRequired(),
                                    validators.Email()],
                                   description='smithkr@mit.edu')
    bagNameGenerator = StringField('Bag naming convention',
                                   [validators.InputRequired()],
                                   description='IASC-Accession')
    packageFormat = SelectField('Compression format',
                                [validators.InputRequired()],
                                choices=[('zip', 'Zip'), ('tar', 'Tar'),
                                         ('uncompressed', 'Uncompressed')])
    checksumType = SelectField('Checksum type', choices=[('md5', 'md5'),
                               ('sha', 'sha')])
    maxBagSize = IntegerField('Maximum bag size (in GB)', default=10)
    metadata = FieldList(FormField(HandbagMetadataForm), min_entries=1)
    addMetadata = SubmitField(description='Add metadata field')
    delMetadata = SubmitField(description='Delete metadata field')
