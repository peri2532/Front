//문제1
let fruitList=['사과','바나나'];
let FruitName = prompt("과일 이름을 입력하세요: ");
if(FruitName == '사과' || FruitName =='바나나'){
    console.log("이미 존재하는 과일입니다.");
}
else{
    fruitList.push(FruitName);
    console.log(fruitList);
}

//문제2
let juNUM= prompt("주민등록번호 13자리: ");
if(juNUM[6]==1 || juNUM[6]==3){
    console.log("blue");
}
else if(juNUM[6]==2 || juNUM[6]==4){
    console.log("red");
}
else{
    console.log("다시 시도하시오.")
}

//문제3
let totalPrice = Number(prompt("총 구매 금액: "));
if(totalPrice>=50000){
    console.log(`총 구매 금액은 ${(totalPrice)*0.9}입니다.`);
}
else if(totalPrice>=30000){
    console.log(`총 구매 금액은 ${(totalPrice)*0.95}입니다.`);
}
else if(totalPrice>=10000){
    console.log(`총 구매 금액은 ${(totalPrice)*0.99}입니다.`);
}
else {
    console.log(`총 주문 금액은 ${totalPrice}입니다.`);
}

//문제4
let month = prompt("1~12사이의 월을 입력하시오: ");
if(month>=3 &&month<=5 ){
    console.log("봄");
}
else if(month>=6 && month<=8){
    console.log("여름");
}
else if(month>=9 && month<=11){
    console.log("가을");
}
else if(month == 12 || month == 1 || month == 2){
    console.log("겨울");
}
else{
    console.log("잘못된 월입니다.");
}

//문제 5 
let 정수1 = Number(prompt("정수1: "));
let 정수2 = Number(prompt("정수2: "));
let 정수3 = Number(prompt("정수3: "));
if(정수1>정수2){
    if(정수1>정수3){
        console.log("정수1이 가장 큰 수");
    }
    else{
        console.log("정수3이 가장 큰 수");
    }
}
else if(정수1<정수2){
    if(정수1>정수3){
        console.log("정수2가 가장 큰 수");
    }
    else{
        console.log("정수3이 가장 큰 수");
    }
}
else if(정수1 == 정수2 && 정수2 == 정수3){
    console.log("3개의 정수가 다 똑같음")
}

//문제 6
let year = prompt("연도를 입력하시오: ");
if((year%4 == 0 && year %100 != 0) || year%400==0){
    console.log(`${year}년은 윤년입니다.`);
}
else{
    console.log(`${year}년은 평년입니다.`);
}

//문제7
let int1 = Number(prompt("정수1 입력: "));
let int2 = Number(prompt("정수2 입력: "));
let int3 = Number(prompt("정수3 입력: "));

if(int1>=int2 && int1>=int3){
    if(int2>=int3){
        console.log(`${int3},${int2},${int1}`);
    }
    else{
        console.log(`${int2},${int3},${int1}`);
    }
}
else if(int2>=int1 && int2 >=int3){
    if(int1>=int3){
        console.log(`${int3},${int1},${int2}`);
    }
    else{
        console.log(`${int1},${int3},${int2}`);
    }
}
else{
    if(int1>=int2){
        console.log(`${int2},${int1},${int3}`);
    }
    else{
        console.log(`${int1},${int2},${int3}`);
    }
}

//문제 8
let R_S_P1 = Number(prompt("0(가위),1(바위),2(보)중 하나의 숫자를 입력하시오: "));
let R_S_P2 = Number(prompt("0(가위),1(바위),2(보)중 하나의 숫자를 입력하시오: "));
if(R_S_P1 == 0 && R_S_P2 == 1){
    console.log("플레이어2 승리");
}
else if(R_S_P1 ==1 && R_S_P2 == 2){
    console.log("플레이어2 승리");
}
else if(R_S_P1 ==2 && R_S_P2 == 0){
    console.log("플레이어2 승리");
}
else if(R_S_P1 == 1 && R_S_P2 == 0){
    console.log("플레이어1 승리");
}
else if(R_S_P1 ==2 && R_S_P2 == 1){
    console.log("플레이어1 승리");
}
else if(R_S_P1 ==0 && R_S_P2 == 2){
    console.log("플레이어1 승리");
}
else if(R_S_P1==0 && R_S_P2 == 0){
    console.log("무승부");
}
else if(R_S_P1==1 && R_S_P2 == 1){
    console.log("무승부");
}
else if(R_S_P1==2 && R_S_P2 == 2){
    console.log("무승부");
}
else{
    console.log("숫자를 바르게 입력하시오.");
}

//문제9
let carArray=['250어7142','142가7415', '888호8888'];
let locationArray=['A1','B3','C2'];
let carNUM=prompt("차량번호 입력: ");
let index= carArray.indexOf(carNUM);
if(index != -1){
    console.log(`차량 이름은 ${carArray[index]}이고 차량위치는 ${locationArray[index]}이다.`)
}
else{
    console.log("차량이 존재하지 않습니다.")
}

//문제10
let courseList=['수학','영어','과학','국어'];
let delname = prompt("제외하고 싶은 과목명 입력: ");
let index1 = courseList.indexOf(delname);

if(index1 != -1){
    courseList.splice(index1,1);
    console.log(`${courseList}`);
}
else{
    console.log("해당 과목은 신청 목록에 없습니다.");
}
