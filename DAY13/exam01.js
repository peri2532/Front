// [1] 함수 : 함(상자/공간) 수(숫자/코드)
//누군가가 상자에 미리 넣어둔 상자
//왜? 한번 넣어둔 숫자/코드를 재사용 예] 수학(공식), 라이브러리/API

//[2]함수 정의/만들기
function 내가만든함수명(){ //fun s
    console.log(); //중괄호 안에 미리 정의할 코드/명령어
} //fun e
//[3]] 함수 호출 / 사용하기
내가만든함수명();

//[4] 함수 종류: 1.내가만든함수 function 2.남이만든함수 console.log( ) alert() prompt()

//[5] 함수 예
function 믹서기함수(과일){
    let 주스 = 과일 + "주스"; // 믹서기 함수가 처리하는 코드 정의/만들기
    return 주스; //처리된 결과를 반환 선택
} //func end
믹서기함수("사과") //믹서기 함수에 사과라는 문자열을 전달했다. 인자값/인수 --- 중매/연결 --> 매개변수
//참고: "사과" 이면 자료이고 사과이면 변수/함수명(키워드)
//믹서기 함수가 처리한 결과를 컵 이라는 변수에 담았다.
let data = "딸기";
let 컵2 = 믹서기함수(data);

//[6] 매개변수 x, 반환 x
function func1() {console.log("func1 exe");}
func1();

//매개변수 o , 반환 x , 대표적으로 console.log()
function func2 (x, y){console.log("func2 exe");}

//매개변수 o , 반환 o , 대표적으로 prompt();
function func3 (x,y) {console.log("func3 exe"); return x+y; }
let result1 = func(3,5);

//매개변수 x, 반환 o 
function func( ){console.log("func4 exe"); return 10;}
let result2 = funsc();

//[7] 지역변수란? 특정한 if/for/함수 {} 안에서 선언된 (매개)변수는 { } 밖에서 호출/사용 안된다.
let 전역변수 = "대한민국";
if( true){
    let 지역변수1= "경기도";
    console.log(지역변수1);
for(let i =1; i<1; i++){
    let 지역변수2 = "안양시";
    console.log(지역변수1);
    console.log(지역변수2);
    console.log(전역변수);
}
}

function func5(지역변수3){
    let 지역변수3 = "수원시"
}//func end
func5("안산시");

//[8] 함수 호출/사용 하는 방법
//(1) JS에서 호출: 함수명();
alert("JS에서 실행");
//(2) HTML에서 호출:  <마크업명 이벤트속성명="함수명 ()"/>
//onclick : 해당 마크업을 클릭했을때 (이벤트/JS)발생
 //<button onclick="alert('HTML에서 실행')">버튼</button>