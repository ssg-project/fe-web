document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('file-upload');
    const uploadForm = document.getElementById('upload-form');

    // 업로드 버튼 클릭 시 파일 선택 창 열기
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    // 파일 선택 후 처리
    fileInput.addEventListener('change', function(event) {
        const files = event.target.files;
        
        if (files.length > 0) {
            const formData = new FormData(uploadForm);

            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            fetch('/upload-endpoint', { // 서버의 업로드 엔드포인트 URL로 변경 필요
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log('성공:', data);
                // 업로드 성공 시 추가 작업
            })
            .catch((error) => {
                console.error('오류:', error);
                // 업로드 실패 시 추가 작업
            });
        }
    });
});