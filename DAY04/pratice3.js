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
//참조: [1] a b c 비교: a>b , a>c , b>c 총 3번 , [2] 두 변수간의 값 교체/스왑
//스왑: (1) 변수는 하나의 자료(값)만 저장한다. (2)연산은 하나씩 처리된다.
//방법: 임시저장소 인 temp변수를 활용한다. a 와 b 의 값 스왑, temp= a; b=a; a=temp;
//오름차순: 작은것->큰 것 / 과거 ->최근날짜 / abc/ 123/ ㄱㄴㄷ
let a = Number(prompt(" a input : "));
let b = Number(prompt(" b input : "));
let c = Number(prompt(" c input : "));
if(a>b){let temp= a; a=b; b=temp;}//비교1: 만약에 앞에 있는 값이 더 크면 스왑
if(a>c){let temp= a; a=c; c=temp;}//비교2
if(b>c){let temp= b; b=c; c=temp;}//비교3 : 반복문 이용하면 충분히 코드 줄일 수 있음.
console.log(`오름차순: ${a} ${b} ${c}`);

//내가 한 풀이
// let int1 = Number(prompt("정수1 입력: "));
// let int2 = Number(prompt("정수2 입력: "));
// let int3 = Number(prompt("정수3 입력: "));

// if(int1>=int2 && int1>=int3){
//     if(int2>=int3){
//         console.log(`${int3},${int2},${int1}`);
//     }
//     else{
//         console.log(`${int2},${int3},${int1}`);
//     }
// }
// else if(int2>=int1 && int2 >=int3){
//     if(int1>=int3){
//         console.log(`${int3},${int1},${int2}`);
//     }
//     else{
//         console.log(`${int1},${int3},${int2}`);
//     }
// }
// else{
//     if(int1>=int2){
//         console.log(`${int2},${int1},${int3}`);
//     }
//     else{
//         console.log(`${int1},${int2},${int3}`);
//     }
// }

//문제 8
//플레이어 1 경우의수 : 승리(0==2 이거나 1==0 이거나 2==1) 무승부(0==0 1==1 2==2 ) 패배(그외)
//플레이어 1 경우의 수 2: 공식: 플레이어1 ==(플레이어2 +1)%3 / 3(2+1)%3 ==0, 1(0+1)%3==1, 2(1+1)%3 ==2
let player1 = Number(prompt("플레이어1:가위[0] 바위[1] 보[2] : "));
let player2 = Number(prompt("플레이어1:가위[0] 바위[1] 보[2] : "));
//방법1: if(player1 ==0&&player2 ==2 ||player1 == 1 && player2 ==0 || player1 == 2 && player2 ==1){
if(player1 ==(player2 + 1) % 3) {// 나머지 연산
    console.log("플레이어1 승리");
}else if (player== player2){
    console.log("무승부");
}else{
    confirm("플레이어2 승리");
}
// let R_S_P1 = Number(prompt("0(가위),1(바위),2(보)중 하나의 숫자를 입력하시오: "));
// let R_S_P2 = Number(prompt("0(가위),1(바위),2(보)중 하나의 숫자를 입력하시오: "));
// if(R_S_P1 == 0 && R_S_P2 == 1){
//     console.log("플레이어2 승리");
// }
// else if(R_S_P1 ==1 && R_S_P2 == 2){
//     console.log("플레이어2 승리");
// }
// else if(R_S_P1 ==2 && R_S_P2 == 0){
//     console.log("플레이어2 승리");
// }
// else if(R_S_P1 == 1 && R_S_P2 == 0){
//     console.log("플레이어1 승리");
// }
// else if(R_S_P1 ==2 && R_S_P2 == 1){
//     console.log("플레이어1 승리");
// }
// else if(R_S_P1 ==0 && R_S_P2 == 2){
//     console.log("플레이어1 승리");
// }
// else if(R_S_P1==0 && R_S_P2 == 0){
//     console.log("무승부");
// }
// else if(R_S_P1==1 && R_S_P2 == 1){
//     console.log("무승부");
// }
// else if(R_S_P1==2 && R_S_P2 == 2){
//     console.log("무승부");
// }
// else{
//     console.log("숫자를 바르게 입력하시오.");
// }

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
