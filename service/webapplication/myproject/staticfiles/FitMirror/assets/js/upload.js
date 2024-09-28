document.getElementById('fullbody_image').addEventListener('change', function(event) {
    var output = document.getElementById('fullbody_preview');
    output.style.display = 'block'; // 미리보기 이미지 표시
    var reader = new FileReader();
    reader.onload = function() {
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});

document.getElementById('clothes_image').addEventListener('change', function(event) {
    var output = document.getElementById('clothes_preview');
    output.style.display = 'block'; // 미리보기 이미지 표시
    var reader = new FileReader();
    reader.onload = function() {
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // 스피너 및 버튼 요소 찾기
    var spinner = document.getElementById('spinner');
    var submitButton = document.getElementById('fitmirror-submit');
    // 버튼 숨기고 스피너 표시
    submitButton.style.display = 'none';
    spinner.style.display = 'inline-block';


    alert('답변이 올때까지 기다려주세요.');
    console.log('Form submitted. Waiting for response...');

    var formData = new FormData();
    var fullbodyImage = document.getElementById('fullbody_image').files[0];
    var clothesImage = document.getElementById('clothes_image').files[0];
    var imageType = document.querySelector('input[name="fit_type"]:checked').value;
    formData.append('fullbody_image', fullbodyImage);
    formData.append('clothes_image', clothesImage);
    formData.append('fit_type', imageType);

    fetch('/fitmirror/upload/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Received response from server.');
        return response.json();
    })
    .then(data => {
        console.log('Processing response data:', data);
        if (data.base64_image) {
            document.getElementById('result-image').style.display = 'block';
            document.getElementById('result-image').src = 'data:image/png;base64,' + data.base64_image;
            console.log('Image displayed successfully.');
        } else {
            alert('Failed to process images (파일 업로드는 성공!!)');
            console.error('No base64_image in response data');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the images');
    })
    .finally(() => {
        // 스피너 숨기고 버튼 다시 표시
        spinner.style.display = 'none';
        submitButton.style.display = 'inline-block';
    });
});

document.getElementById('fullbody_image').addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
        var fileName = this.files[0].name;
        console.log("Fullbody Image Selected: " + fileName);
        document.getElementById('fullbody_filename').textContent = fileName;
    } else {
        console.log("No file selected for fullbody image.");
    }
});

document.getElementById('clothes_image').addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
        var fileName = this.files[0].name;
        console.log("Clothes Image Selected: " + fileName);
        document.getElementById('clothes_filename').textContent = fileName;
    } else {
        console.log("No file selected for clothes image.");
    }
});