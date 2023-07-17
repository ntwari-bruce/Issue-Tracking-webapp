window.addEventListener('DOMContentLoaded', (event) => {
    const dismissAll = document.getElementById('dismiss-all');
    const notificationCards = document.querySelectorAll('.notification-card');
    const today = document.querySelector('.today');
    const older = document.querySelector('.older');

    dismissAll.addEventListener('click', function(e){
        e.preventDefault();
        notificationCards.forEach(card => {
            card.classList.add('display-none');
        });
        today.style.display = 'none';
        older.style.display = 'none';
        dismissAll.style.display = 'none';
        const row = document.querySelector('.notification-container');
        const message = document.createElement('h4');
        message.classList.add('text-center');
        message.innerHTML = 'All caught up!';
        row.appendChild(message);
    });
});