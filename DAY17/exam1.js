/*
    [인터벌 : interval] : 간격/주기 뜻 
        1. 시간적인 간격에 따라 특정 코드/함수 실행
        2. 사용법
            (1) 생성 
                setInterval( 함수명 , 밀리초 );
                - 함수명 : 실행할 함수명 만 작성한 , ( ) 생략한다.
                - 밀리초 : 1/1000초
                예시] let 변수명 = setInterval( 함수명 , 밀리초 );
            (2) 종료
            clearInterval( 종료할Interval객체  );

*/
// [1] 
let value = 0;
function 증가함수( ){
    value = value + 1 ; // 전역변수 1증가 
    const box1 = document.querySelector("#box1");
    box1.innerHTML = value;
} // f end 
setInterval( 증가함수 , 1000 ); //특정한 시간/ 간격 마다 함수 실행 1초( 1/1000 ) 마다 '증가함수' 자동 실행 
// 주의할점 : 증가함수 : 함수그자체  vs 증가함수() : 함수실행 

// [2] 
function 시계함수(){
    let today = new Date(); // new Date() : 현재 시스템(컴퓨터/핸드폰)의 날짜/시간 반환 함수 
    let hour = today.getHours(); // '시'  new Date().getHours()
    let minute = today.getMinutes(); //'분' new Date().getMinutes()
    let second = today.getSeconds(); //'초' new Date().getSeconds()
    let time = `${ hour } : ${ minute } : ${ second < 10 ? '0'+second : second }`;
    const box2 = document.querySelector("#box2");
    box2.innerHTML = time;
} // f end 
setInterval( 시계함수 , 1000 ); // 자동으로 1초 마다 시계함수 가 자동 실행된다.
// [3] 
let time = 0 ;  // 현재 타이머의 시간(초) ????? 
let timerId;    // inerval 객체를 저장하는 전역변수? 서로다른 함수간의 *공유* 
function 타이머시작(){
    // ! interval 실행후 반환된 객체를 timmerId에 대입 , 왜? 추후에 제어(종료)하기 위해서
    timerId = setInterval( 시간함수 , 1000 );
}
function 타이머중지(){
    clearInterval( timerId ); // clearInterval( 종료할interval객체 )
}
function 시간함수(){
    time++; // 1증가
    document.querySelector("#box3").innerHTML = time;
}