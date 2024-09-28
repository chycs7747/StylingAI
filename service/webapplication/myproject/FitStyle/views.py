import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import boto3
from botocore.client import Config
from .serializers import ImageUploadSerializer
from django.shortcuts import render


def index(request):
    return render(request, 'FitStyle/index.html')

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            user_uuid = str(uuid.uuid4())  # 사용자 식별을 위한 UUID 생성
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )
            
            def upload_images(images, category):
                for idx, img in enumerate(images, start=1):
                    _, extension = os.path.splitext(img.name)
                    file_path = f'FitStyle/{user_uuid}/{category}{idx}{extension}'
                    s3_client.upload_fileobj(img, settings.AWS_STORAGE_BUCKET_NAME, file_path)

            if 'top_photos' in serializer.validated_data:
                upload_images(serializer.validated_data['top_photos'], 'upper_body')
            if 'bottom_photos' in serializer.validated_data:
                upload_images(serializer.validated_data['bottom_photos'], 'lower_body')
            

            # AI 서버로 요청 보내기
            ai_server_url = f'{settings.SERVER_BASE_URL}/fitstyle'
            response = requests.post(ai_server_url, data={'user_id': user_uuid}, timeout=240)

            # 응답 처리
            if response.status_code == 200:
                print(response.json())
                # result_data = response.json('content')
                result_data = response.json()['content']
                img1_base64 = result_data.get('full_body')
                img2_base64 = result_data.get('recommend')

                return Response({
                    'img1_base64': img1_base64,
                    'img2_base64': img2_base64,
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)