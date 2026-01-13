/*[ JS 함수 실습 ]*/

/*실습 1: 성인 인증 함수 : 나이(age)를 매개변수로 받아, 20세 이상이면 true를, 미만이면 false를 반환하는 isAdult 함수를 만드세요. isAdult(25)와 isAdult(17)의 결과를 각각 콘솔에 출력해 보세요.*/
// 함수 (구성) 설계 : 
// 1.매개변수 :age 
// 2.리턴값 : true/false 
// 3.처리 : age 가 20세 이상이면 true를, 미만이면 false
function isAdult( age ){
    if( age >= 20 ){ return true; }
    else{ return false; }
    // vs return age >=20;
} // f end 
let result1 = isAdult( 25 );  // 1. 함수실행 -> 2. 함수반환 -> 3. 반환값 변수저장 -> 4.변수출력
console.log( result1 );
console.log( isAdult(17) );  // 1. 함수실행 -> 2. 함수반환 -> 3. 출력  *안쪽 소괄호 부터 실행 처리 우선!

/*실습 2: 배열의 총합 구하기:숫자로 이루어진 배열을 매개변수로 받아, for 반복문을 사용해 모든 요소의 합계를 구하여 반환하는 sumArray 함수를 만드세요. 아래 numbers 배열로 테스트해 보세요. */
// 매개변수:   배열  ,  리턴값    :  합계를 구하여 반환     ,   처리  :   for 반복문을 사용해 모든 요소의 합계
const numbers = [10, 20, 30, 40, 50];
function sumArray( array ){ // 매개변수란? 함수호출시 전달되는 인자값 연결되는 변수 
  // 주의할점 : 매개변수도 지역변수 특징으로 함수밖 numbers를 인자 로 전달 하더라도 매개변수랑은 다르다.
  let sum = 0; // 지역변수 
  for( let i = 0 ; i <= array.length - 1 ; i++ ){ sum += sum+array[i]; } // 모든 합계를 구하는 반복문 끝나고
  return sum; // 함수가 종료되면서 해당 함수 호출했던 곳으로 반환 
}
console.log(  sumArray( numbers ) ) ;

/*실습 3: 가장 긴 단어 찾기 : 문자열로 이루어진 배열을 매개변수로 받아, for 반복문을 사용해 가장 긴 단어를 찾아 반환하는 findLongestWord 함수를 만드세요. 아래 words 배열로 테스트해 보세요.*/
const words = ['apple', 'banana', 'kiwi', 'strawberry'];
function findLongestWord( array ){
  let longWord = words[0]; // 첫번째 인덱스 값을 가장 긴 단어로 가정 하고 시작
  for( let index = 1 ; index <= array.length - 1 ; index++ ){
    // 만약에 가장 긴 단어가 저장된 변수보다 index번째 단어가 더 길면 
    if( longWord.length < array[index].length ){longWord = array[index];} // 가장 긴 단어를 저장하는 변수에 대입 
  } // for end 
  return longWord; // 반환값이란? 함수내 선언된 변수들은 함수가 종료되면 사라진다.
} // f end 
console.log(  findLongestWord( words ) ) ;

/*실습 4: 게임 점수 관리하기 : let userScore = 0; 전역 변수를 만드세요. gainScore() 함수는 userScore를 10 증가시키고, loseScore() 함수는 5 감소시킵니다. gainScore()를 세 번, loseScore()를 한 번 호출한 뒤, 최종 점수를 콘솔에 출력하세요.*/
let userScore = 0; // 전역변수란? JS파일내 어떠한 { } 안에서 선언되지 않은 변수 
function gainScore( ){ userScore += 10; } // 전역변수는 아무런 조건 없이 함수 안에서 사용가능 vs 전역변수를 인수로 매개변수에게 전달
function loseScore( ){ userScore -= 5; }
gainScore(); gainScore(); gainScore(); loseScore();
console.log( userScore );

/*실습 5: 최고 점수 학생 찾기 : 전역변수 students 배열 데이터를 이용하여 , 가장 높은 점수(score)를 가진 학생의 이름을 찾아 반환하는 findTopStudent 함수를 만드세요.*/
const students = [{ name: '김철수', score: 85 },{ name: '이영희', score: 92 },{ name: '박민준', score: 78 }];
function findTopStudent() {
  let top = students[0]; // 첫번째 학생(객체) 을 최고 점수 가정 시작 
  for( let index = 1 ; index <= students.length-1 ; index++ ){
      if ( top.score < students[index].score ){ // 만약에 최고 점수의 점수보다 index번째 객체의 점수가 더 크면 < 객체내 속성 값 비교 >
        top = students[index]; // index번째 객체를 top 저장                                               < 객체 대입 > 
      }
  } // for end 
  return top.name; // 최고점수를 가진 객체내 점수가 아닌 이름 속성값 반환 
} // f end 
console.log( findTopStudent() );


/*실습 6: 상품 목록 페이지 만들기 : 전역변수 products 배열 데이터를 이용하여, 각 상품을 소개하는 HTML 요소를 동적으로 만들어 페이지에 표시하는 renderProducts 함수를 만드세요.
각 상품은 이름(<h4>), 가격(<p>), 재고(<p>)를 포함한 div로 묶여야 합니다.*/
const products = [ { name: '노트북', price: 1200000, stock: 5 }, { name: '모니터', price: 350000, stock: 12 },{ name: '키보드', price: 80000, stock: 25 }];
function renderProducts(){
  let html = ``; // 구성한 html 문자열 저장하는 변수
  for( let index = 0 ; index <= products.length-1 ; index++ ){
    let prod = products[index]; // index 번째 제품(객체) 호출 
    html += `<div>
              <h4> ${ prod.name } </h4>
              <p> ${ prod.price } </p>
              <p> ${ prod.stock } </p>
            </div>`; // 객체 하나씩 div 를 구성하여 html에 추가 +=   vs 대입 = 
  } // for end 
  document.write( html );
} // f end 
renderProducts();

/*실습 7: 간단한 계산기 : num1, num2, operator ( '+', '-') 세 개의 매개변수를 받는 calculator 함수를 만드시오. operator가 '+'이면 두 수의 합을, '-'이면 두 수의 차를 콘솔에 출력하시오. */
function calculator( num1 , num2 , operator ){
  if( operator == "+" ) { console.log( num1 + num2); }
  else if( operator == "-"){ console.log( num1 - num2 ); }
} // f end 
calculator( 5 , 3 , "+" );  calculator( 3 , 2 , "-" );

/*실습 8: HTML 리스트(ul, li) 동적 생성*/
let todoList = ['장보기', '운동하기']
function renderList(){
  let html = `<ul>`;  // ul 시작 
  for( let index = 0 ; index <= todoList.length-1 ; index++ ){
    let todo = todoList[index]; // index 번째의 문자열 1개 호출해서 변수 담았다.
    html += `<li> ${ todo } </li>`; // 각 항목 
  } // for end 
  html += `</ul>`;    // ul 끝
  document.write( html ); 
} // f end 
renderList();

/*실습 9: 입장료 계산 함수 : 임의의 나이(age)를 매개변수로 받아 입장료를 반환하는 getTicketPrice 함수를 만드시오.
8세 미만: "무료"  8세 이상 19세 이하: "5,000원"  20세 이상: "10,000원"  계산된 가격 문자열을 반환(return)하시오.*/

function getTicketPrice(  age  ){
  if( age >= 20 ){  return "10,000원"; }
  else if( age >= 8 ){ return "5,000원"; }
  else{ return "무료"; }
} // f end 
console.log( getTicketPrice( 21 ) );   
/*
      변수의 종류 분류 시점 : 선언
        - 선언 : let / const / function 키워드가 작성된 위치

      변수 = 하나의 값/자료 저장 
        - 전역변수 : { } 에서 선언 안된.
        - 지역변수 : { } 에서 선언 된.
        - 매개변수 : 인자값을 저장된.
*/