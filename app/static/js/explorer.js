//storage-web/app/static/js/explorer.js
document.addEventListener("DOMContentLoaded", () => {
    const uploadButton = document.getElementById("upload-button");
    const fileInput = document.getElementById("file-upload");
    const uploadForm = document.getElementById("upload-form");

    // 업로드 버튼 클릭 시 파일 선택창 열기
    uploadButton.addEventListener("click", () => {
        fileInput.click();
    });

    // 파일 선택 후 폼 자동 제출
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            uploadForm.submit();
        }
    });
});