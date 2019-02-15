# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------
from os import path

from django.core.files.uploadedfile import UploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from main.models import Session, Picture


class ManagePicturesView(View):
    """
    Endpoint for pictures upload
    """

    @staticmethod
    def handle_file_upload(file: UploadedFile, ses: Session):
        """
        Handles the upload of a picture file
        :param file: An UploadedFile coming from the form
        :param ses: The session to which Pictures will be linked
        """
        pic = Picture(session=ses, type='original', ext=path.splitext(file.name)[1])
        pic.save()

        filename = pic.pic_path
        print('Saving ' + filename)

        try:
            with open(filename, 'wb+') as pic_file:
                for chunk in file.chunks():
                    pic_file.write(chunk)
            return True
        except IOError:
            print('Error while saving ' + filename)
            pic.delete()
            return False

    def post(self, request: WSGIRequest):
        try:
            session = Session.objects.get(id=request.session.session_key)
        except Session.DoesNotExist:
            session = Session(id=request.session.session_key, status='initial status')
            session.save()
        files = request.FILES.getlist('filepond')

        results = []

        for i, file in enumerate(files):
            results.append({'id': i, 'result': self.handle_file_upload(file, session)})

        return JsonResponse({'results': results})

    def delete(self, request: WSGIRequest):
        print(request)
