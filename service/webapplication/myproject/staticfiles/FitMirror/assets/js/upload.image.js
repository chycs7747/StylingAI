document.getElementById('fullbody_image').addEventListener('change', function(event) {
    var output = document.getElementById('fullbody_preview');
    output.style.display = 'block'; // 미리보기 이미지 표시
    var reader = new FileReader();
    reader.onload = function(){
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});

document.getElementById('clothes_image').addEventListener('change', function(event) {
    var output = document.getElementById('clothes_preview');
    output.style.display = 'block'; // 미리보기 이미지 표시
    var reader = new FileReader();
    reader.onload = function(){
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});