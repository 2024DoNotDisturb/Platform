document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button-grid button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const url = button.getAttribute('data-url');
            if (url) {
                window.location.href = url; // 각 페이지 url로 이동
            }
        });
    });
});