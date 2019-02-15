# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Website Index, handles the pictures upload form
# ----------------------------

from os import makedirs, path
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest
from django.views.generic import FormView
from django.shortcuts import redirect

from main.models import Session, Picture

from main.forms import UploadPicsForm



class IndexView(FormView):
    """
    Index View, shows a form for original pictures upload
    """
    template_name = 'pages/index.html'
    form_class = UploadPicsForm
    success_url = '/'

    # Called when the form is submitted
    def post(self, request: HttpRequest, *args, **kwargs):
        form = UploadPicsForm(request.POST, request.FILES)
        files = request.FILES.getlist('pics')

        if form.is_valid():
            # Requires at least 10 pictures to be uploaded
            if len(files) < 10:
                form.add_error('pics', 'Sono necessarie almeno 10 immagini')
                return self.form_invalid(form)

            if len(files) > 30:
                form.add_error('pics', 'Sono consentite al massimo 30 immagini')
                return self.form_invalid(form)

            if request.session.session_key:
                request.session.flush()

            request.session.create()
            key = request.session.session_key
            print('Session created, key: ' + key)

            ses = Session(id=key, status='initial status')
            ses.save()

            originals_dir = '{}/original'.format(ses.session_dir)
            makedirs(originals_dir)
            makedirs(originals_dir + '/preps')
            makedirs(originals_dir + '/noises')

            # Processes the uploaded pictures
            # TODO: add security checks for file type
            # TODO: add checks on client (js)
            for pic_file in files:
                handle_file_upload(pic_file, ses)

            return redirect('socials/')

        return self.form_invalid(form)
