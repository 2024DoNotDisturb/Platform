const closemodal = document.querySelector(".close_modal");
const submitmodal = document.querySelector(".submit_modal");
const openModal = document.querySelector(".btn-open-modal");
const signInBtn = document.getElementById("signIn");
const container = document.querySelector(".container");
const modal = document.querySelector('.modal');
const termsOfUseModal = document.getElementById('termsOfUseModal');

// 이용약관 텍스트 불러오기
function fetchContent(url, elementId) {
  fetch(url)
    .then(response => response.text())
    .then(data => {
      document.getElementById(elementId).textContent = data;
    });
}

openModal.addEventListener("click", () => {
  fetchContent('/get_terms_of_use', 'termsOfUseContent');
  fetchContent('/get_personal_information', 'personalInformationContent');
  termsOfUseModal.style.display = "flex";
});
closemodal.addEventListener("click", () => {
  modal.style.display = "none";
});
submitmodal.addEventListener("click", () => {
  modal.style.display = "none";
  container.classList.add("right-panel-active");
});
signInBtn.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});
openModal.addEventListener("click", () => {
  modal.style.display = "flex";
});

// 전화번호 하이픈
const hypenTel = (target) => {
  target.value = target.value
    .replace(/[^0-9]/g, '')
    .replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);
}

// 우편번호 주소 핸들러
function sample6_execDaumPostcode() {
  new daum.Postcode({
      oncomplete: function(data) {
          // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

          // 각 주소의 노출 규칙에 따라 주소를 조합한다.
          // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
          var addr = ''; // 주소 변수
          var extraAddr = ''; // 참고항목 변수

          //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
          if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
              addr = data.roadAddress;
          } else { // 사용자가 지번 주소를 선택했을 경우(J)
              addr = data.jibunAddress;
          }

          // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
          if(data.userSelectedType === 'R'){
              // 법정동명이 있을 경우 추가한다. (법정리는 제외)
              // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
              if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                  extraAddr += data.bname;
              }
              // 건물명이 있고, 공동주택일 경우 추가한다.
              if(data.buildingName !== '' && data.apartment === 'Y'){
                  extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
              }
              // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
              if(extraAddr !== ''){
                  extraAddr = ' (' + extraAddr + ')';
              }
              // 조합된 참고항목을 해당 필드에 넣는다.
              document.getElementById("sample6_extraAddress").value = extraAddr;
          
          } else {
              document.getElementById("sample6_extraAddress").value = '';
          }

          // 우편번호와 주소 정보를 해당 필드에 넣는다.
          document.getElementById('sample6_postcode').value = data.zonecode;
          document.getElementById("sample6_address").value = addr;
          // 커서를 상세주소 필드로 이동한다.
          document.getElementById("sample6_detailAddress").focus();
      }
  }).open();
}

// 생일 날짜 확인
document.addEventListener("DOMContentLoaded", () => {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById("birthDate").setAttribute('max', today);
});

// 회원가입 버튼 이벤트
document.querySelector('.sign-up-container form').addEventListener('submit', function(event) {
  const id = document.querySelector('input[name="join_id"]').value;
  const password = document.querySelector('input[name="join_pwd"]').value;
  const email = document.querySelector('input[name="email"]').value;
  
  const idPattern = /^[A-Za-z0-9]{6,}$/; // 특수문자 제외, 6자 이상
  const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/; // 8-20자, 문자, 숫자, 특수문자 포함
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;

  if (!idPattern.test(id)) {
    alert('아이디는 특수문자를 제외하고 6자 이상이어야 합니다.');
    event.preventDefault();
  } else if (!passwordPattern.test(password)) {
    alert('비밀번호는 8-20자 이내의 문자, 숫자, 특수문자를 포함해야 합니다.');
    event.preventDefault();
  }else if (!emailPattern.test(email)) {
    alert('비밀번호는 8-20자 이내의 문자, 숫자, 특수문자를 포함해야 합니다.');
    event.preventDefault();
  }

});

// 아이디 중복 버튼 및 규칙 확인
document.getElementById('checkIdBtn').addEventListener('click', function() {
  const joinId = document.getElementById('join_id').value;
  const idCheckIcon = document.getElementById('idCheckIcon');
  const idFeedback = document.getElementById('idFeedback');

  fetch(`/check_id?join_id=${joinId}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        idCheckIcon.textContent = 'cancel';
        idCheckIcon.style.color = 'red';
        idFeedback.style.color = 'red';
      } else {
        const idPattern = /^[a-zA-Z0-9]{6,}$/;
        if (!idPattern.test(joinId)) {
          idFeedback.textContent = '아이디는 특수문자 제외, 6자 이상이어야 합니다.';
          idFeedback.style.color = 'red';
          idCheckIcon.textContent = 'cancel';
          idCheckIcon.style.color = 'red';
        } else {
          idFeedback.textContent = '';
          idCheckIcon.textContent = 'check_circle';
          idCheckIcon.style.color = 'green';
        }
      }
      idCheckIcon.style.display = 'inline';
    })
    .catch(error => {
      console.error('Error checking ID:', error);
    });
});
document.getElementById('join_id').addEventListener('input', function() {
  const joinId = document.getElementById('join_id').value;
  const idFeedback = document.getElementById('idFeedback');
  const idCheckIcon = document.getElementById('idCheckIcon');

  const idPattern = /^[a-zA-Z0-9]{6,}$/;

  if (!idPattern.test(joinId)) {
    idFeedback.textContent = '아이디는 특수문자 제외, 6자 이상이어야 합니다.';
    idFeedback.style.color = 'red';
    idCheckIcon.style.display = 'none';
  } else {
    idFeedback.textContent = '';
  }
});
document.getElementById('join_pwd').addEventListener('input', function() {
  const joinPwd = document.getElementById('join_pwd').value;
  const pwdFeedback = document.getElementById('pwdFeedback');

  const pwdPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$/;

  if (!pwdPattern.test(joinPwd)) {
    pwdFeedback.textContent = '비밀번호는 8-20자 이내, 문자, 숫자, 특수문자를 포함해야 합니다.';
    pwdFeedback.style.color = 'red';
  } else {
    pwdFeedback.textContent = '';
  }
});
