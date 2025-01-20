document.addEventListener('DOMContentLoaded', function() {
    // 초기 변수 설정
    let currentWaitingTime = 15;
    let progress = 0;
    const progressBar = document.getElementById('progressBar');
    const timeValue = document.getElementById('timeValue');
    const currentNumber = document.getElementById('currentNumber');
    
    // 대기 시간 업데이트 함수
    function updateWaitingTime() {
        if (currentWaitingTime > 0) {
            currentWaitingTime--;
            timeValue.textContent = currentWaitingTime;
            
            // 프로그레스 바 업데이트
            progress = ((15 - currentWaitingTime) / 15) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }

    // 대기 번호 랜덤 업데이트 함수
    function updateQueueNumber() {
        const randomChange = Math.floor(Math.random() * 10) + 1;
        const currentNum = parseInt(currentNumber.textContent);
        if (currentNum > randomChange) {
            currentNumber.textContent = (currentNum - randomChange).toString();
        }
    }

    // 1초마다 시간 업데이트
    const timeInterval = setInterval(() => {
        updateWaitingTime();
        if (currentWaitingTime <= 0) {
            clearInterval(timeInterval);
            window.location.href = '/ticketing'; // 대기 완료 후 이동할 페이지
        }
    }, 1000);

    // 3초마다 대기 번호 업데이트
    setInterval(updateQueueNumber, 3000);

    // 페이지 새로고침 방지
    window.onbeforeunload = function() {
        return "대기실을 나가시면 대기순서가 초기화됩니다.";
    };
});