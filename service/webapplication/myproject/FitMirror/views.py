from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import boto3
import uuid
import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from botocore.client import Config
from .serializers import ImageUploadSerializer
from django.conf import settings

import os # 임시로 테스트 이미지 로컬에 저장해보기 위해 사용 (/app/myproject/FitMirror/testimages)

def index(request):
    return render(request, 'FitMirror/index.html')

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            fullbody_image = serializer.validated_data['fullbody_image']
            clothes_image = serializer.validated_data['clothes_image']
            fit_type = request.data.get('fit_type')

            _, fullbody_image_extension = os.path.splitext(fullbody_image.name)
            _, clothes_image_extension = os.path.splitext(clothes_image.name)

            # UUID 생성
            user_uuid = str(uuid.uuid4())
            
            
            # S3에 이미지 업로드
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )

            # S3 경로 설정
            fullbody_image_path = f"FitMirror/{user_uuid}/full_body{fullbody_image_extension}"
            clothes_image_path = f"FitMirror/{user_uuid}/fit_body{clothes_image_extension}"

            # 이미지 업로드
            s3.upload_fileobj(fullbody_image, settings.AWS_STORAGE_BUCKET_NAME, fullbody_image_path)
            s3.upload_fileobj(clothes_image, settings.AWS_STORAGE_BUCKET_NAME, clothes_image_path)


            # 업로드 확인 함수
            def check_upload(bucket_name, file_path):
                try:
                    s3.head_object(Bucket=bucket_name, Key=file_path)
                    return True
                except s3.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        return False
                    else:
                        raise e

            # 업로드 확인
            fullbody_uploaded = check_upload(settings.AWS_STORAGE_BUCKET_NAME, fullbody_image_path)
            clothes_uploaded = check_upload(settings.AWS_STORAGE_BUCKET_NAME, clothes_image_path)

            # 업로드 확인 결과를 반환
            if fullbody_uploaded and clothes_uploaded:
                return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Image upload failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            """
            # 인공지능 서버에 요청 보내기
            ai_server_url = f'{settings.SERVER_BASE_URL}/fitmirror'
            
            
            data = {
                'user_id': user_uuid,
                'fit_type': fit_type
            }
            response = requests.post(ai_server_url, data={'user_id': user_uuid,'fit_type':fit_type}, timeout=240)
            if response.status_code == 200:
                result = response.json()
                # 결과에서 base64 데이터를 추출
                base64_image = result.get('content')

                return Response({'base64_image': base64_image}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to get response from AI server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        """
        
        else:
            print("serializer error occured")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


