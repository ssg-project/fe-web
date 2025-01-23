//예약 성공시 
function handleReservationSuccess(response) {
    // success가 true이고 redirect 값이 있을 때만 이동
    if (response.success && response.redirect) {
        window.location.href = response.redirect;
    } else {
        console.error('Reservation failed or invalid response:', response);
        alert(response.message || 'Reservation failed. Please try again.');
    }
}