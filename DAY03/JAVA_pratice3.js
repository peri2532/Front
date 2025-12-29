//문제 1
let 밑변 = prompt("밑변을 입력하세요: ");
let 높이 = prompt("높이를 입력하세요: ");
let 넓이 = (밑변 * 높이) / 2;
console.log(`삼각형의 넓이: ${넓이}`);

//문제 2
let 섭씨 =prompt("섭씨 온도를 입력하세요: ");
let 화씨 = (섭씨 * 9 / 5)+ 32;
console.log(`화씨 온도 : ${화씨}`);

//문제3
let year = prompt("연도를 입력하세요: ");
let 나이 = 2025 - year;
console.log(`2025년 기준 현재 나이: ${나이}`);

//문제 4
let cm = prompt("키를 cm단위로 입력하세요: ");
let kg = prompt("몸무게를 kg단위로 입력하세요: ");
let m = cm / 100;
let BMI = kg /(m*m);
console.log(`BMI 지수: ${BMI}`);

//문제 5
let id = prompt("아이디를 입력하세요: ");
let email = prompt("이메일을 입력하세요: ");
let 결과= (id ==="admin" || email === "admin@test.com" ? "관리자" : "일반 사용자");
console.log(`${결과}`);

//문제 6
let score = prompt("점수를 입력하세요: ");
let result = (score>=90 ? "A" : score>=80 ? "B" : "C");
console.log(`점수: ${result}`);
//document.write(`<h3>${result}</h3>`);
document.querySelector("h2").innerHTML = result;

//문제 7
let age = prompt("나이를 입력하세요: ");
resultage=(age>=20 && age<30 ? "이벤트 대상입니다." : "이벤트 대상이 아닙니다. ");
console.log(`${resultage}`);

//문제 8
 let likeCount = 3;
    console.log(`좋아요 수 : ${++likeCount}`);

//문제 9
let todoList = ['장보기','과제하기'];
let a = prompt("새로 할 일을 입력하세요: ");
todoList.push(a);
console.log(`할 일 목록: ${todoList}`);

//문제 10
let waitingList =['김민준','이서연','박도윤','최지우'];
console.log(`마지막 대기자는 ${waitingList[3]}입니다`);