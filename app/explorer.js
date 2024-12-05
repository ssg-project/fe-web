function confirmDelete() {
    if (confirm("정말로 삭제하시겠습니까?")) {
        alert("삭제되었습니다.");
        // 실제 삭제 로직 추가
    } else {
        alert("취소되었습니다.");
    }
}

function editRow(button) {
    const row = button.parentElement.parentElement; 
    const nameCell = row.querySelector('.file-name');
    const originalName = nameCell.textContent;

    nameCell.innerHTML = `<input type='text' value='${originalName}'>`;

    Array.from(button.parentElement.children).forEach(btn => btn.style.display = 'none');

    const applyButton = document.createElement('button');
    applyButton.textContent = '적용';
    applyButton.className = 'action-button';
    applyButton.onclick = function() { confirmEdit(applyButton); };

    const cancelButton = document.createElement('button');
    cancelButton.textContent = '취소';
    cancelButton.className = 'action-button';
    cancelButton.onclick = function() { cancelEdit(applyButton, originalName); };

   button.parentElement.appendChild(applyButton);
   button.parentElement.appendChild(cancelButton);
}

function confirmEdit(button) {
   const row = button.parentElement.parentElement; 
   const nameCell = row.querySelector('.file-name');
   const inputField = nameCell.querySelector('input');
   
   nameCell.textContent = inputField.value;

   resetButtons(button);
}

function cancelEdit(button, originalName) {
   const row = button.parentElement.parentElement; 
   const nameCell = row.querySelector('.file-name');
   
   nameCell.textContent = originalName;

   resetButtons(button);
}

function resetButtons(button) {
   const actionCell = button.parentElement;

   actionCell.innerHTML = `
       <button class='action-button' onclick='editRow(this)'>수정</button>
       <button class='action-button' onclick='confirmDelete()'>삭제</button>`;
}