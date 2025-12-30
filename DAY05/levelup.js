//문제1
let accountNumberList=['111-222','333-444','555-6666'];
let balanceList=[50000,120000,30000];

let account = (prompt("계좌번호를 입력하세요 "));
let price = Number(prompt("출금 금액을 입력하세요 "));
let accountNUM=accountNumberList.indexOf(account)
let sum= price+1200;
if(accountNUM == -1){
    console.log("존재하지 않는 계좌입니다.")
}
else{
    if(price<10000){
        console.log("출금 금액이 너무 적습니다.");
    }
    else if(price%10000 != 0){
        console.log("출금 단위 오류입니다.");
    }
    else if(sum>balanceList[accountNUM]){
        console.log("잔액이 부족합니다.");
    }
    else{
        console.log("출금 완료")
    }
}



//문제 2
let carNumberList=['12가3456','34나7890','56다1234'];
let useTimeList=[45,130,320];
let carNUM= prompt("차량 번호를 입력하세요.");
let carme=carNumberList.indexOf(carNUM);
if(carme==-1){
    console.log("존재하지 않는 차량입니다.");
}
else{
    let time=useTimeList[carme];
    let price = 0;
    if(time<=0){
        console.log("잘못된 사용 시간입니다.")
    }
else{
    if (time <= 60){
        price = 1000;
    }
    else{
        let overtime = time-60;
        let unit = parseInt((overtime -1 ) / 30)+1;
        price = 1000 + (unit * 500);
    }
    if(price>10000){
        price = 10000;
    }
    console.log(`주차 요금은 ${price}원 입니다.`);
}
}