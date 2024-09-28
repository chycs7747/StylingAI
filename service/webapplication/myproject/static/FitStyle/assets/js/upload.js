function addFileInput(sectionId) {
    const section = document.getElementById(sectionId);

    // Create new file input
    const newFileInput = document.createElement('input');
    newFileInput.type = 'file';
    newFileInput.name = sectionId + '_photos';
    newFileInput.accept = '.png, .jpg, .jpeg, .webp';
    newFileInput.onchange = function() {
        addFileInput(sectionId); // Add new file input
    };

    // Create a div to hold the new file input and add it to the section
    const inputWrapper = document.createElement('div');
    inputWrapper.appendChild(newFileInput);
    section.appendChild(inputWrapper);
}

function validateForm() {
    const topSection = document.getElementById('top_photos_section');
    const bottomSection = document.getElementById('bottom_photos_section');

    const topInputs = topSection.getElementsByTagName('input');
    const bottomInputs = bottomSection.getElementsByTagName('input');

    let topValid = false;
    let bottomValid = false;

    for (let input of topInputs) {
        if (input.files.length > 0) {
            topValid = true;
            break;
        }
    }

    if (!topValid) {
        alert('상의 사진을 1개 이상 업로드해주세요');
        return false;
    }

    for (let input of bottomInputs) {
        if (input.files.length > 0) {
            bottomValid = true;
            break;
        }
    }

    if (!bottomValid) {
        alert('하의 사진을 1개 이상 업로드해주세요');
        return false;
    }

    return true;
}

function resetFileInputs(sectionId) {
    const section = document.getElementById(sectionId);
    section.innerHTML = ''; // Clear all child elements
    addFileInput(sectionId); // Add the initial file input
}

function resetAllFileInputs() {
    resetFileInputs('top_photos_section');
    resetFileInputs('bottom_photos_section');
}

window.onload = function() {
    // Initialize with one file input for each section
    addFileInput('top_photos_section');
    addFileInput('bottom_photos_section');

    // Add reset functionality to buttons
    document.getElementById('reset_top_photos').onclick = function() {
        resetFileInputs('top_photos_section');
    };
    document.getElementById('reset_bottom_photos').onclick = function() {
        resetFileInputs('bottom_photos_section');
    };
    document.getElementById('reset_all_photos').onclick = function() {
        resetAllFileInputs();
    };
};

// Form submission handler
document.querySelector('form').addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault(); // Stop form submission if validation fails
        return; // Exit the function
    }

    event.preventDefault();

    var formData = new FormData();

    // Append top photos
    var topPhotosSection = document.getElementById('top_photos_section').getElementsByTagName('input');
    for (var i = 0; i < topPhotosSection.length; i++) {
        if (topPhotosSection[i].files.length > 0) {
            for (var j = 0; j < topPhotosSection[i].files.length; j++) {
                formData.append('top_photos', topPhotosSection[i].files[j]);
            }
        }
    }

    // Append bottom photos
    var bottomPhotosSection = document.getElementById('bottom_photos_section').getElementsByTagName('input');
    for (var i = 0; i < bottomPhotosSection.length; i++) {
        if (bottomPhotosSection[i].files.length > 0) {
            for (var j = 0; j < bottomPhotosSection[i].files.length; j++) {
                formData.append('bottom_photos', bottomPhotosSection[i].files[j]);
            }
        }
    }

    alert('답변이 올때까지 기다려주세요.');

    // Hide submit button and show spinner
    var submitButton = document.getElementById('fitstyle-submit');
    var resetButton = document.getElementById('reset_all_photos');
    var spinner = document.getElementById('spinner');
    submitButton.style.display = 'none';
    resetButton.style.display = 'none';
    spinner.style.display = 'block';

    fetch('/fitstyle/upload/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide spinner and show submit button
        spinner.style.display = 'none';
        submitButton.style.display = 'inline-block';
        resetButton.style.display = 'inline-block';

        if (data.img1_base64 && data.img2_base64) {
            document.getElementById('result-image1').src = 'data:image/png;base64,' + data.img1_base64;
            document.getElementById('result-image2').src = 'data:image/png;base64,' + data.img2_base64;
            document.getElementById('result-image1').style.display = 'block';
            document.getElementById('result-image2').style.display = 'block';
        } else {
            alert('이미지를 처리하지 못했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('이미지를 업로드하는 동안 오류가 발생했습니다.');
        spinner.style.display = 'none';
        submitButton.style.display = 'inline-block';
        resetButton.style.display = 'inline-block';
    });
});
