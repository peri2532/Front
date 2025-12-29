//문제 1
let 점수1 = Number(prompt("점수1: "));
let 점수2 = Number(prompt("점수2: "));

let 총점 = 점수1 + 점수2 ;
if(총점>=90){
    console.log("성공");
}
else{
    console.log("실패");
}

//문제2
let 정수1 = Number(prompt("정수1: "));
let 정수2 = Number(prompt("정수2: "));
if(정수1>정수2){
    console.log("정수1이 더 큽니다.");
}
else if(정수1<정수2){
    console.log("정수2가 더 큽니다.");
}
else{
    console.log("두 정수는 같다.")
}

//문제3
let id = (prompt("id: "));
let pwd = (prompt("pwd") );
if(id=='admin'&&pwd=="1234"){
    console.log("로그인 성공");
}
else{
    console.log("로그인 실패")
}

//문제4
let password =(prompt("비밀번호 입력: "));
let pwdLEN= password.length;
if(pwdLEN>=12){
    console.log("보안 등급 강함");
}
else if(pwdLEN>=8){
    console.log("보안 등급: 보통")
}
else{
    console.log("보안등급: 약함(8자 이상으로 설정해주세요.)")
}

//문제5
let seat=['O','X','O'];
let num=prompt("좌석번호(0~2)입력: ");
if(seat[num]=='O'){
    console.log("예약 불가");
}
else{
    console.log("예약 성공");
    seat[num]='O';
}

//문제6
let 점수 = Number(prompt("게임 점수를 입력하세요: "));
if(점수>=900){
    console.log("A급 경품");
}
else if(점수>=700){
    console.log("B급 경품");
}
else if(점수>=500){
    console.log("C급 경품");
}
else{
    console.log("참가상");
}

//문제7
let role = prompt("사용자 역할: ");
if(role=="admin"){
    console.log("모든 기능에 접근할 수 있습니다.");
}
else if(role == "editor"){
    console.log("콘텐츠 수정 및 생성 기능에 접근할 수 있습니다.");
}
else if(role == "viewer"){
    console.log("콘텐츠 조회만 가능합니다.");
}
else{
    console.log("정의디지 않은 역할입니다.");
}

//문제8
let age = Number(prompt("사용자 나이: "));
if(age>=65){
    console.log("3000원")
}
else if(age>=20){
    console.log("10000원");
}
else if(age>=8){
    console.log("5000원");
}
else{
    console.log("무료");
}

//문제 9
let Oscore = Number(prompt("점수 입력: "));
if(Oscore>=90){
    console.log("A등급");
}
else if(Oscore>=80){
    console.log("B등급");
}
else if(Oscore>=70){
    console.log("C등급");
}
else {
    console.log("재시험")
}

//문제10
let DrinkName=['콜라','사이다','커피'];
let DrinkPrice=[1000,1000,1500];
let WantNum=Number(prompt("원하는 음료(0~2): "));
if(WantNum>=0 && WantNum<=2){
    console.log(`선택하신 음료는 ${DrinkName[WantNum]}입니다. 가격은 ${DrinkPrice[WantNum]}원입니다.`);
}
else{
    console.log("없는 상품입니다.")
}