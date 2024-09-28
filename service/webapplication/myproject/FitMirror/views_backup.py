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
        print("접근1")
        serializer = ImageUploadSerializer(data=request.data)
        print("접근2")
        if serializer.is_valid():
            print("접근3")
            fullbody_image = serializer.validated_data['fullbody_image']
            clothes_image = serializer.validated_data['clothes_image']
            fit_type = request.data.get('fit_type')

            # 디버깅용
            print(fullbody_image.name)  # 업로드된 파일의 이름
            print(fullbody_image.size)  # 파일의 크기
            _, fullbody_image_extension = os.path.splitext(fullbody_image.name)
            print(fullbody_image_extension)
            
            #print(fullbody_image.read())  # 파일의 내용을 바이트로 읽기
            print(clothes_image.name)  # 업로드된 파일의 이름
            print(clothes_image.size)  # 파일의 크기
            _, clothes_image_extension = os.path.splitext(clothes_image.name)
            print(clothes_image_extension)
            #print(clothes_image.read())  # 파일의 내용을 바이트로 읽기
            print(fit_type)

            # # 로컬에 파일 저장
            # local_dir = "/app/myproject/FitMirror/testimages"
            # os.makedirs(local_dir, exist_ok=True)

            # fullbody_image_path = os.path.join(local_dir, fullbody_image.name)
            # clothes_image_path = os.path.join(local_dir, clothes_image.name)

            # with open(fullbody_image_path, 'wb') as f:
            #     for chunk in fullbody_image.chunks():
            #         f.write(chunk)

            # with open(clothes_image_path, 'wb') as f:
            #     for chunk in clothes_image.chunks():
            #         f.write(chunk)

            # print(f"Fullbody image saved at: {fullbody_image_path}")
            # print(f"Clothes image saved at: {clothes_image_path}")

            # UUID 생성
            user_uuid = str(uuid.uuid4())

            print("시리얼라이징 uuid:", user_uuid)
            print(f"AWS_ACCESS_KEY_ID: {settings.AWS_ACCESS_KEY_ID}")
            print(f"AWS_SECRET_ACCESS_KEY: {settings.AWS_SECRET_ACCESS_KEY}")
            print(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
            
            
            # S3에 이미지 업로드
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )

            print("s3 클라이언트 생성완료")

            # S3 경로 설정
            fullbody_image_path = f"FitMirror/{user_uuid}/full_body{fullbody_image_extension}"
            clothes_image_path = f"FitMirror/{user_uuid}/fit_body{clothes_image_extension}"

            print(f'경로1: {fullbody_image_path}')
            print(f'경로2: {clothes_image_path}')

            print("경로 설정 완료")

            # 이미지 업로드
            s3.upload_fileobj(fullbody_image, settings.AWS_STORAGE_BUCKET_NAME, fullbody_image_path)
            s3.upload_fileobj(clothes_image, settings.AWS_STORAGE_BUCKET_NAME, clothes_image_path)

            print("이미지 업로드")

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

            print("업로드 확인 완료")
            
            # 인공지능 서버에 요청 보내기
            ai_server_url = f'{settings.SERVER_BASE_URL}/fitmirror'
            
            
            data = {
                'user_id': user_uuid,
                'fit_type': fit_type
            }
            print(f'보낸 api주소: {ai_server_url}\n 보낸 데이타: {data}')
            response = requests.post(ai_server_url, data={'user_id': user_uuid,'fit_type':fit_type})
            if response.status_code == 200:
                result = response.json()
                # 결과에서 base64 데이터를 추출
                base64_image = result.get('content')
                print(f'ai서버에서 응답: {base64_image}')
                return Response({'base64_image': base64_image}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to get response from AI server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        else:
            print("serializer error occured")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
