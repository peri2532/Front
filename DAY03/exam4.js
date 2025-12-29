//1. 산술연산자 : +더하기 -빼기 *곱하기 /나누기 %나머지
console.log( 10 + 3); //13
console.log(10 -3); //7
console.log(10 * 3); //30
console.log(10/3); //3.3333
console.log(parseInt(10%3)); //3

// [지문1] prompt 함수로 국어 , 영어 , 수학 점수를 각 입력받아서 (각 변수에 저장하고) 총점 과 평균을 계산하여 console탭에 출력하시오.
let 국어 = prompt("국어 점수를 입력하세요: ");
let 영어 = prompt("영어 점수를 입력하세요: ");
let 수학 = prompt("수학 점수를 입력하세요: ");
let 총점 = Number(국어) + Number(영어) + Number(수학);
let 평균 = 총점 /3 ;
console.log(`총점은 ${총점}이고, 평균은 ${평균}이다.`);

// [지문2] prompt 함수로 반지름를 입력받아서 원넓이[반지름*반지름*3.14] 계산하여 console탭에 출력하시오.
let 반지름 = prompt("반지름을 입력해주세요: ");
let 원넓이 = 반지름 * 반지름 * 3.14;
console.log(`원넓이는 ${원넓이} 입니다. `);

// [지문3] prompt 함수로 두 실수를 입력받아서 앞 실수의 값이 뒤실수의 값의 비율% 계산하여 console탭에 출력하시오.
let 실수1 =  Number(prompt("실수1을 입력해주세요: "));
let 실수2 = Number(prompt("실수2을 입력하세요: "));
비율 = (실수1 / 실수2) *100;
console.log(`비율은 ${비율}% 입니다.`);

// 1)비교연산자 : >초과 <미만 >=이상 <=이하 ==(값)같다 !=(값)같지않다 ===(값과타입)같다 !==(값과타입)같지않다.
//비교 결과는 true 또는 false
// 2)논리연산자 : && 이면서 ||이거나 ! 부정

// [지문4] prompt 함수로 정수를 입력받아 입력받은 값이 홀수이면 true / 짝수이면 false 로 console탭에 출력하시오.
let 정수 = prompt("정수를 입력해주세요: ");
정수 % 2 === 0 ? console.log("true") : console.log("false");

// [지문5] prompt 함수로 정수를 입력받아 입력받은 값이 7의 배수이면 true / 아니면 false 로 console탭에 출력하시오.
let 정정수 = prompt("정수를 입력하세요: ");
정정수 % 7 ===0 ? console.log("true") : console.log("false");

// [지문6] prompt 함수로 아이디 와 비밀번호를 입력받아서 (입력받은)아이디가 'admin' 이고 (입력받은)비밀번호가 1234 와 일치하면 true / 아니면 false 출력하시오.
let id = prompt("id를 입력해주세요: ");
let pw = prompt("pw를 입력해주세요: ");
id === "admin" && pw === "1234" ? console.log("true") : console.log("false");

// [지문7] prompt 함수로 정수를 입력받아 입력받은 값이 홀수 이면서 7배수 이면 true / 아니면 false 로 console탭에 출력하시오.
let 정수수 = prompt("정수를 입력하시오: ");
정수수 % 2 ===0 || 정수수 % 7 ===0 ? console.log("true") : console.log("false");

// [지문8] 1차점수 와 2차점수 prompt함수로 각 입력받아서 총점이 150점이상이면 '합격' 아니면 '불합격' HTML의 <h3> 에 출력하시오.
let 점수1차 = Number(prompt("1차 점수를 입력하세요: "));
let 점수2차 = Number(prompt("2차 점수를 입력하세요: "));
let total = 점수1차 + 점수2차;
let result= total>= 150 ? console.log("'합격'") : console.log("'불합격'");
document.write(`<h3>${result}</h3>`);

// [지문9] 두 사람의 이름을 prompt함수로 각 입력받아서 만일 이름이 '유재석' 이면 뒤에 (방장) 이라고 이름 뒤에 붙이고 아니면 생략한다.  HTML의 <ol> 에 결과를 출력하시오.
let name1 = prompt("이름을 입력하세요: ");
let name2 = prompt("이름을 입력하세요: ");
let result1 = name1 =="유재석" ? `${name1}(방장)` : `${name1}`;
let result2 = name2 =="유재석" ? `${name2}(방장)` : `${name2}`;
document.write(`<ol><li>${result1}</li><ol>`);
document.write(`<ol><li>${result2}</li><ol>`);
//documetnt.write(`<h3>실습8 : ${result} </h3>`)