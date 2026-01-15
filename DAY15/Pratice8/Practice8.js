/* ====== DB (초기 샘플 데이터) ====== */
let dept = [
    { id: 1, name: '개발팀' },
    { id: 2, name: '디자인팀' },
    { id: 3, name: '기획팀' }
];

let emp = [
    { id: 1, name: '김민준', rank: '선임 개발자', dept_id: 1, profileImage: undefined },
    { id: 2, name: '이서연', rank: '수석 디자이너', dept_id: 2, profileImage: undefined },
    { id: 3, name: '박도윤', rank: '팀장', dept_id: 3, profileImage: undefined }
];

let vacation_list = [
    { id: 1, emp_id: 1, startDate: '2026-08-04', endDate: '2026-08-05', reason: '병원 진료' }
];

/* ====== INITIALIZE ====== */
window.onload = function() {
    printAll();
};

/* ====== COMMON UTIL ====== */
function searchIndex(array, key, value) {
    for(let i = 0; i < array.length; i++){
        if(value == array[i][key]) return i;
    }
    return -1;
}

/* ====== 1. DEPT MANAGEMENT ====== */
function addDept(){
    const inputDOM = document.querySelector("#dept_name-input");
    const name = inputDOM.value.trim();

    if(!name) return alert("부서명을 입력해주세요.");
    if(dept.some(d => d.name === name)) return alert("이미 존재하는 부서명입니다.");

    const newId = dept.length > 0 ? dept[dept.length - 1].id + 1 : 1;
    dept.push({ id: newId, name: name });
    
    inputDOM.value = "";
    printAll();
}

function updateDept(deptId){
    const index = searchIndex(dept, "id", deptId);
    const newName = prompt("수정할 부서명을 입력하세요", dept[index].name);
    
    if(newName && newName.trim() !== "") {
        dept[index].name = newName;
        printAll();
    }
}

function deleteDept(deptId){
    // [제약조건] 부서에 소속된 사원이 있는지 확인
    const hasEmployee = emp.some(e => e.dept_id == deptId);
    if(hasEmployee) return alert("해당 부서에 소속된 사원이 있어 삭제할 수 없습니다.");

    const index = searchIndex(dept, "id", deptId);
    if(index !== -1) {
        dept.splice(index, 1);
        printAll();
    }
}

/* ====== 2. EMP MANAGEMENT ====== */
function addEmp(){
    const name = document.querySelector("#emp_name-input").value;
    const rank = document.querySelector("#emp_rank-input").value;
    const deptId = document.querySelector("#emp_deptId-select").value;
    const file = document.querySelector("#emp_profileImage-input").files[0];

    if(!name || !rank || deptId === "disabled") return alert("모든 항목을 입력하세요.");

    const newId = emp.length > 0 ? emp[emp.length - 1].id + 1 : 1;
    emp.push({
        id: newId,
        name: name,
        rank: rank,
        dept_id: parseInt(deptId),
        profileImage: file
    });

    printAll();
}

function updateEmp(empId){
    const index = searchIndex(emp, "id", empId);
    const input = prompt("수정할 이름과 직급을 입력하세요 (예: 홍길동,과장)", `${emp[index].name},${emp[index].rank}`);
    
    if(input) {
        const [newName, newRank] = input.split(",");
        if(newName && newRank) {
            emp[index].name = newName.trim();
            emp[index].rank = newRank.trim();
            printAll();
        } else {
            alert("입력 형식이 올바르지 않습니다.");
        }
    }
}

function deleteEmp(empId){
    const index = searchIndex(emp, "id", empId);
    if(index !== -1) {
        // [제약조건] 해당 사원의 휴가 신청 기록도 함께 삭제
        vacation_list = vacation_list.filter(v => v.emp_id != empId);
        emp.splice(index, 1);
        printAll();
    }
}

/* ====== 3. VACATION MANAGEMENT ====== */
function addVacationRequest(){
    const empId = document.querySelector("#vacationList_empId-select").value;
    const start = document.querySelector("#vacationList_startDate-input").value;
    const end = document.querySelector("#vacationList_endDate-input").value;
    const reason = document.querySelector("#vacationList_reason-input").value;

    if(empId === "disabled" || !start || !end || !reason) return alert("모든 정보를 입력하세요.");

    const newId = vacation_list.length > 0 ? vacation_list[vacation_list.length - 1].id + 1 : 1;
    vacation_list.push({
        id: newId,
        emp_id: parseInt(empId),
        startDate: start,
        endDate: end,
        reason: reason
    });

    printAll();
}

function cancelVacationRequest(vId){
    const index = searchIndex(vacation_list, "id", vId);
    if(index !== -1) {
        vacation_list.splice(index, 1);
        printAll();
    }
}

/* ====== 4. PRINT FUNCTIONS ====== */
function printAll(){
    printDept();
    printEmp();
    printVacationList();
}

function printDept(){
    const tbody = document.querySelector("#dept_list");
    const select = document.querySelector("#emp_deptId-select");
    let html = "";
    let options = `<option value="disabled">부서를 선택하세요.</option>`;

    dept.forEach(d => {
        html += `<tr>
            <td>${d.name}</td>
            <td>
                <span onclick="updateDept(${d.id})" class="update">수정</span>
                <span onclick="deleteDept(${d.id})" class="delete">삭제</span>
            </td>
        </tr>`;
        options += `<option value="${d.id}">${d.name}</option>`;
    });
    tbody.innerHTML = html;
    select.innerHTML = options;
}

function printEmp(){
    const tbody = document.querySelector("#emp_list");
    const select = document.querySelector("#vacationList_empId-select");
    let html = "";
    let options = `<option value="disabled">휴가 신청 사원을 선택하세요</option>`;

    emp.forEach(e => {
        const dIdx = searchIndex(dept, "id", e.dept_id);
        const dName = dIdx !== -1 ? dept[dIdx].name : "소속없음";
        const imgUrl = e.profileImage ? URL.createObjectURL(e.profileImage) : "https://placehold.co/100";

        html += `<tr>
            <td><img src="${imgUrl}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;"></td>
            <td>${e.name}</td>
            <td>${dName}</td>
            <td>${e.rank}</td>
            <td>
                <span onclick="updateEmp(${e.id})" class="update">수정</span>
                <span onclick="deleteEmp(${e.id})" class="delete">삭제</span>
            </td>
        </tr>`;
        options += `<option value="${e.id}">${e.name}</option>`;
    });
    tbody.innerHTML = html;
    select.innerHTML = options;
}

function printVacationList(){
    const listDiv = document.querySelector("#vacation_list");
    let html = "";

    vacation_list.forEach(v => {
        const eIdx = searchIndex(emp, "id", v.emp_id);
        const eName = eIdx !== -1 ? emp[eIdx].name : "퇴사자";
        
        html += `<div class="list">
            <div class="top"><span>${eName}</span><span onclick="cancelVacationRequest(${v.id})" class="delete" style="cursor:pointer">신청취소</span></div>
            <div class="mid"><span>${v.startDate} ~ ${v.endDate}</span></div>
            <div class="bottom"><span>사유: ${v.reason}</span></div>
        </div>`;
    });
    listDiv.innerHTML = html;
}