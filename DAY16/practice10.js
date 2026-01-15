
// [1] 메모리 설계
// 1. 저장할 서로 더른 자료들을 하나의 객체로 구성
// { "no" : 1 , "id" : qwe , "pw" : "1234" };

// 2. 여러개 객체 들은 배열로 구성 
//let memberList = [{ "no" : 1 , "id" : "qwe" , "pw" : "1234" },{ "no" : 2 , "id" : "asd" , "pw" : "4567" },];

// [2] 함수 설계 
// 1. 등록함수 : 매:x , 리:x , 처 : 입력받은값을 객체 생성하여 배열에저장
// 2. 로그인함수 : 매:x , 리:x , 처 : 입력받은값을 배열내 존재하는지[비교]

// [3] 등록함수 구현 : 등록버튼을 클릭했을때
function signup( ) {
    const signIdDom = document.querySelector( ".signId"); // 1. 입력받은 값 가져온다.
    const id = signIdDom.value;
    const signPwDom = document.querySelector( ".signPw" );
    const pw = signPwDom.value;

    /********** localStorage 활용하여 memberList 호출  *********** */
    let memberList = localStorage.getItem( "memberList" ); // 로컬저장소 'memberList' 값 가져오기
    if( memberList == null ){  // memberList가 비어있으면 
        memberList = [ ]; // memberList 새로운 배열 선언 
    }else{ //memberList가 있으면 
        memberList = JSON.parse( memberList ); // memberList 타입변환
    }
    /********** ====================================  *********** */

    // 2. 입력받은 값들을 객체로 구성한다. 
    //  만약에 회원목록에서 1개이상이면 마지막회원번호 에 +1 , 아니면 1 
    let no = memberList.length >= 1 ? memberList[ memberList.length-1 ].no + 1 : 1 ;
    // let obj = { "no" : no , "id" : id , "pw" : pw }; // * 만약에 속성명 과 속성값변수명이 같으면 생략가능
    let obj = { no , id , pw };
    memberList.push( obj ); alert("회원가입 성공 ") ;// 3. 구성한 객체를 배열에 저장한다.

    /********** localStorage 활용하여 memberList 저장  *********** */
    localStorage.setItem( "memberList" , JSON.stringify( memberList ) );
    /********** ====================================  *********** */
    
} // f end 

// [3] 로그인함수 구현 : 로그인버튼을 클릭했을때
function login( ){
    // 1. 입력받은 값 가져온다. 
    const loginIdDom = document.querySelector( ".loginId"); // 1. 입력받은 값 가져온다.
    const id = loginIdDom.value;
    const loginPwDom = document.querySelector( ".loginPw" );
    const pw = loginPwDom.value;

    /********** localStorage 활용하여 memberList 호출  *********** */
    let memberList = localStorage.getItem( "memberList" ); // 로컬저장소 'memberList' 값 가져오기
    if( memberList == null ){  // memberList가 비어있으면 
        memberList = []; // memberList 새로운 배열 선언 
    }else{ //memberList가 있으면 
        memberList = JSON.parse( memberList ); // memberList 타입변환
    }
    /********** ====================================  *********** */

    // 2. 입력받은 값이 배열(회원목록)내 존재하면 로그인 성공 , 아니면 실패
    for( let index = 0 ; index <= memberList.length - 1 ; index++ ){
        const member = memberList[index]; // index번째 멤버(객체) 꺼내기
        if( member.id == id && member.pw == pw ){ // 만약에 index번째 객체내 id가 입력받은 id와 같으면 
            alert("로그인 성공"); return; // 안내후 함수를 강제 종료;
        }
    } // for end 
    alert("로그인 실패");
} // f end 