/*예제 1: 요소 내용 변경하기, id가 'title'인 <h1> 요소의 내용을 'DOM 조작 성공!'으로 변경하시오.*/
// <h1 id="title"></h1>
let titleDom = document.querySelector("#title"); // 1. 특정한 마크업 가져오기
titleDom.innerHTML = "DOM 조작 성공!";// 2. 특정한 마크업내 텍스트 .innerHTML,  <마크업> 여기가INNER </마크업>

/*예제 2: 사용자 입력값 가져와서 표시하기, id가 'usernameInput'인 <input>에 이름을 입력하고 '확인' 버튼(id: 'submitBtn')을 클릭하면, id가 'greeting'인 <p> 태그에 "안녕하세요, [입력된이름]님!"이라고 표시하시오.*/
//<input id="usernameInput" />,<button id="submitBtn">확인</button>,<p id="greeting"></p>
// 버튼 클릭하면 :  <button id="submitBtn" onclick=" 함수명() ">
function func2( ){ // 클릭이벤트 사용시에는 함수로 묶어주기.
    let usernameDom = document.querySelector("#usernameInput"); // 1. 특정한 마크업 가져오기
    let username = usernameDom.value; // 2. 입력받은 값 가져오기
    let greetingDom = document.querySelector("#greeting"); // 3. 특정한 마크업2 가져오기 
    greetingDom.innerHTML = `안녕하세요, ${ username } 님!` // 4. 특정 마크업2 텍스트 대입 
} // func end 

/*예제 3: 요소 스타일 동적으로 변경하기, '스타일 변경' 버튼(id: 'styleBtn')을 클릭하면, id가 'colorBox'인 <div>의 배경색을 'skyblue'로, 글자색을 'white'로 변경하시오.*/
function func3( ){
    let colorBoxDom = document.querySelector("#colorBox");
    // DOM객체.style.CSS속성명 = CSS속성값  // CSS는 -하이픈가능 , JS -하이픈 불가능
    // 속성명은 카멜표기법 사용하기 : background-color ---> backgroundColor
    colorBoxDom.style.backgroundColor = "skyblue"; 
    colorBoxDom.style.color = "white";
}

/*예제 4: CSS 클래스 토글하기 (다크 모드 예시), '테마 변경' 버튼(id: 'themeBtn')을 클릭할 때마다 <body> 태그에 'dark-mode' 클래스를 추가하거나 제거(토글)하시오. */
// <style> .dark-mode{background-color: black;} </style>
function func4(){
    const bodyDom = document.querySelector("body");
    // DOM객체.classList.toggle( 클래스명 ) : 만약에 클래스가 존재하면 삭제 없으면 추가
    bodyDom.classList.toggle("dark-mode");
}
/*예제 5: 특정 HTML 요소 제거하기, '박스 삭제' 버튼(id: 'removeBtn')을 클릭하면, id가 'targetBox'인 <div> 요소를 문서에서 제거하시오. */
function func5(){
    const targetBoxDom = document.querySelector("#targetBox");
    targetBoxDom.remove();  // DOM객체.remove() : 해당 마크업 삭제/지우기
}
/*예제 6: 여러 요소에 동일한 작업 반복하기 , 클래스가 'item'인 모든 <p> 요소의 글자색을 'green'으로, 글자 두께를 'bold'로 변경하시오. */
// querySelector(): 1개(객체반환)   vs querySelectorAll() : 여러개(배열반환) 
let itemDoms = document.querySelectorAll(".item");
for( let index = 0 ; index <= itemDoms.length -1 ; index++ ){
    const item = itemDoms[index]; // index번째 dom(객체) 꺼내기
    //item.style.color = "green";
    //item.style.fontWeight = "bold";
    // vs 
    item.style = " color : green; font-weight : bold ";
}
/*예제 7: 이미지 소스(src) 변경하기 , https://placehold.co/ , '이미지 변경' 버튼(id: 'changeImgBtn')을 클릭하면, id가 'mainImage'인 <img> 요소의 src 속성을 'https://placehold.co/600x400/red/white'로 변경하시오. */
function func7( ){
    const mainImageDom = document.querySelector("#mainImage");
    // DOM객체명.src = "이미지경로";
    mainImageDom.src="https://placehold.co/600x400/red/white";
}
/* 예제 8 : select 에서 선택한 option값 console 출력하기. */
// <마크업 onclick = "함수명()" />  : 클릭했을떄 
// <마크업 onchange = "함수명()" /> : 값 변경 되었을때 
function func8( ){
    const foodSelectDom = document.querySelector("#foodSelect");
    const food = foodSelectDom.value; // 선택된 option 값 가져오기
    console.log( food );
}
/* 예제 9 : input 에서 입력받은 값을 전역 배열에 저장하고 배열 상태를 출력하기. */
const products = [ ]; // 전역배열 , 
// 지역변수 대신에 전역변수 선언한이유 : 등록할때 마다 함수는 재실행/초기화/영구저장안됨
function func9(){
    // 입력 
    const productInputDom = document.querySelector("#productInput");
    const product = productInputDom.value;
    // 저장
    products.push( product ); // 배열에 입력받은값 저장 
    // 출력
    const productPrintDom = document.querySelector("#productPrint");
    productPrintDom.innerHTML = products;
}