/* 메뉴 펼치기*/
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
          navbar = document.getElementById(navbarId),
          bodypadding = document.getElementById(bodyId);

    if (toggle && navbar) {
        toggle.addEventListener('click', () => {
            navbar.classList.toggle('expander');
            bodypadding.classList.toggle('body-pd');
        });
    }
};

showMenu('nav-toggle', 'navbar', 'body-pd');

const navbar = document.getElementById('navbar');
const bodypadding = document.getElementById('body-pd');

navbar.addEventListener('mouseenter', () => {
    navbar.classList.add('expander');
    bodypadding.classList.add('body-pd');
});

navbar.addEventListener('mouseleave', () => {
    navbar.classList.remove('expander');
    bodypadding.classList.remove('body-pd');
});

/* 활성 링크 */
const linkColor = document.querySelectorAll('.nav__link');
function colorLink() {
    linkColor.forEach(l => l.classList.remove('active'));
    this.classList.add('active');
}
linkColor.forEach(l => l.addEventListener('click', colorLink));

/* 메뉴 축소 */
const linkCollapse = document.getElementsByClassName('collapse__link');
for (let i = 0; i < linkCollapse.length; i++) {
    linkCollapse[i].addEventListener('click', function() {
        const collapseMenu = this.nextElementSibling;
        collapseMenu.classList.toggle('showCollapse');

        const rotate = collapseMenu.previousElementSibling;
        rotate.classList.toggle('rotate');
    });
}

// 로그아웃 핸들러
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logout-btn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(event) {
            event.preventDefault();

            fetch('/logout', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (response.ok) {

                    window.location.replace('/login');
                } else {
                    console.error('로그아웃 실패');
                }
            })
            .catch(error => {
                console.error('로그아웃 오류:', error);
            });
        });
    }
});