// 1. HTML 요소들 가져오기 (DOM 선택)
const categoryInput = document.querySelector('select');
const nameInput = document.querySelectorAll('input')[0]; // 첫 번째 input
const priceInput = document.querySelectorAll('input')[1]; // 두 번째 input
const fileInput = document.querySelectorAll('input')[2]; // 파일 input
const registerBtn = document.querySelector('.btn');
const tableBody = document.querySelector('tbody'); // 데이터가 들어갈 곳

// 2. 등록 버튼 클릭 이벤트 연결
registerBtn.onclick = function() {
    // A. 입력값 가져오기
    const category = categoryInput.value;
    const name = nameInput.value;
    const price = priceInput.value;
    
    // B. 오늘 날짜 생성 (YYYY-MM-DD 형식)
    const now = new Date();
    const date = now.toISOString().split('T')[0];

    // [중요] 예외 처리: 값이 비어있으면 경고창 띄우기
    if (name === "" || price === "") {
        alert("제품명과 가격을 입력해주세요!");
        return;
    }

    // C. 새로운 행(tr) 만들기
    const newRow = document.createElement('tr');

    // D. 행 안에 들어갈 내용(td) 작성 (백틱 ` 사용)
    newRow.innerHTML = `
        <td><img src="#" class="img"></td>
        <td>${category}</td>
        <td>${name}</td>
        <td>${Number(price).toLocaleString()}</td>
        <td>${date}</td>
        <td>
            <button class="delete" onclick="deleteRow(this)">삭제</button>
            <button class="update" onclick="updateRow(this)">수정</button>
        </td>
    `;

    // E. 표(tbody)에 추가하기
    tableBody.appendChild(newRow);

    // F. 입력창 초기화하기
    nameInput.value = "";
    priceInput.value = "";
};

// 3. 삭제 기능 함수
function deleteRow(button) {
    // button(나) -> td(부모) -> tr(조부모)를 찾아서 삭제
    if (confirm("정말 삭제하시겠습니까?")) {
        button.parentElement.parentElement.remove();
    }
}

// 4. 수정 기능 함수
function updateRow(button) {
    // 수정할 행의 '상품명' 칸과 '가격' 칸 찾기
    const row = button.parentElement.parentElement;
    const nameCell = row.children[2]; // 3번째 칸
    const priceCell = row.children[3]; // 4번째 칸

    // prompt로 새 값 받기
    const newName = prompt("새로운 상품명:", nameCell.innerText);
    const newPrice = prompt("새로운 가격:", priceCell.innerText);

    // 값이 입력되었다면 화면 업데이트
    if (newName) nameCell.innerText = newName;
    if (newPrice) priceCell.innerText = Number(newPrice).toLocaleString();
}