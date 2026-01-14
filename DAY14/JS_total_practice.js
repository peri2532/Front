/*
3. 핵심 기능
초기 데이터 표시:
    사용자가 페이지에 처음 방문했을 때, 카테고리 선택 메뉴에는 두 개의 예시 카테고리('음료', '과자')가 기본적으로 표시되어 있어야 합니다.
    제품 목록 표에는 사용법을 쉽게 이해할 수 있도록 네 개의 예시 제품이 기본적으로 표시되어 있어야 합니다.
제품 등록 기능:
    사용자가 '등록 영역'에 카테고리, 제품명, 가격을 모두 입력하고 "등록" 버튼을 클릭하면, 해당 제품이 '목록 영역' 표에 새로운 행으로 즉시 추가되어야 합니다.
    제품 등록 시, 등록 날짜는 현재 날짜로 자동 기록되어야 합니다.
    첨부된 이미지는 목록의 '이미지' 열에 표시되어야 하며, 이미지를 첨부하지 않은 경우 기본 이미지가 대신 표시되어야 합니다.
제품 관리 기능:
    삭제: 각 제품의 "삭제" 버튼을 클릭하면 해당 제품이 목록에서 즉시 제거되어야 합니다.
    수정: "수정" 버튼을 클릭하면, prompt 창을 통해 새로운 제품명과 가격을 입력받아 해당 제품의 정보를 수정하고 목록을 즉시 갱신해야 합니다.
*/

/* [1] 메모리 설계 , 표/테이블 = 배열 , 표제목 = 속성명 , 행/가로 1개 = 객체 1개  , 기능(삭제/수정) 은 메모리가 아니다. */
// 1. 저장할 데이터 들을 객체 구성 
// { "image" : "https://placehold.co/100x100" , "category" : 1 , "name" : "코카콜라" , "price" : 1000 , "date" : "2026-01-14" }

// 2. 각 객체들 간의 식별(구분=주민등록번호/사번/학번 등등) 1개 이상 필요 , 단] 중복이 없는 속성으로 선택!
// pcode : productCode 제품코드 로써 삭제 와 수정시 식별 용도 사용 
// { pcode : 1 , "image" : "https://placehold.co/100x100" , "category" : 1 , "name" : "코카콜라" , "price" : 1000 , "date" : "2026-01-14" }

// 3. 테이들 간의 연관관계 구성 
// 카테고리테이블(상위) --> 제품테이블(하위) , 제품테이블의 ccode는 카테고리테이블의 ccode 를 참조(교집합)한다.
// { "ccode" : 1 , "category" : "음료" }
// { "pcode" : 1 , "image" : "https://placehold.co/100x100" , "ccode" : 1 , "name" : "코카콜라" , "price" : 1000 , "date" : "2026-01-14" }

// 4. 객체가 다수 일때는 배열 사용한다.
const categoryAry = [ { "ccode" : 1 , "category" : "음료" } , { "ccode" : 2 , "category" : "과자" }  ];
const productAry = [
    { "pcode" : 1 , "image" : "https://placehold.co/100x100" , "ccode" : 1 , "name" : "코카콜라" , "price" : 1000 , "date" : "2026-01-14" },
    { "pcode" : 2 , "image" : "https://placehold.co/100x100" , "ccode" : 2 , "name" : "사이다" , "price" : 1500 , "date" : "2026-01-15" }
];
// [2] 기능/함수 설계 
// 1. 함수/기능 개수  , 등록[C]기능 , 출력[R]기능 , 수정[U]기능 , 삭제[D]기능 
// 등록함수 , 매개변수 : X , 리턴값 : X , 처리 : 입력받은 4개와 현재시스템날짜 를 객체 만들어서 배열 저장 , 
//      실행조건 : <등록> 클릭하면
// 출력함수 , 매개변수 : X , 리턴값 : X , 처리 : 배열내 모든 객체들을 tr 구성하여 출력 , 
//      실행조건 : 1.페이지열렸을때 2.등록성공 3.삭제성공 4.수정성공
// 수정함수 , 매개변수 : pcode(수정할대상) , 리턴값 : X , 처리 : 수정할 값 PROMPT 받아서 매개변수의 제품 수정
//      실행조건 : <수정> 클릭하면 
// 삭제함수 , 매개변수 : pcode(삭제할대상) , 리턴값 : X , 처리 : 매개변수의 제품 삭제
//      실행조건 : <삭제> 클릭하면 

// [3] 구현 
// 1. 출력함수 : 어디에 무엇을 출력하는지?
productPrint(); // JS가 열렸을때 최초 1번 함수 실행 
function productPrint( ){ // 함수만들기 , 함수명은 아무거나 , ( ) 매개변수 없는상태 , { } 함수 실행될때 처리할 코드
    const tbody = document.querySelector("tbody"); // 1. 어디에 
    let html = "";// 2. 무엇을 + 배열내 모든 객체들을 TR 구성하여 HTML 만들기 + 반복문 
        for( let index = 0 ; index <= productAry.length-1 ; index++ ){
            const product = productAry[index]; // index번째 제품(객체) 1개 호출
            // ccode --> category 변경 : ccode의 category 배열에서 찾기  
            let category = "";
            for( let index = 0 ; index <= categoryAry.length-1 ; index++ ){
                if( product.ccode == categoryAry[index].ccode ){ // 만약에 제품의 카테고리코드가 index번째 카테고리코드 와 같으면 
                    category = categoryAry[index].category;// 찾은 카테고리명 
                    break; // 목표성공 : (가까운)반복문 종료
                }
            } // for end 
            html  += `<tr>
                        <td> <img src="${ product.image }"/> </td>
                        <td> ${ category } </td> <td> ${ product.name } </td> 
                        <td> ${ product.price } </td> <td> ${ product.date } </td> 
                        <td> 
                            <button onclick="productDelete( ${ product.pcode } )" class="deleteBtn">삭제</button> 
                            <button onclick="productUpdate( ${ product.pcode } )" class="updateBtn">수정</button> 
                        </td>
                    </tr>` // 반복(객체 개수) 횟수 만큼 tr(행) 생성
        } // for end 
    tbody.innerHTML = html;  // 3. 출력 
} // f end 

// 2. 삭제함수 : 해당 하는 행의 <삭제> 버튼을 클릭하면 삭제(배열내 제거 = .splice() )처리
function productDelete( pcode ){ // 매개변수로 삭제할 pcode 받았다. [삭제할 대상자]
    for( let index = 0 ; index <= productAry.length-1 ; index++ ){// 1. pcode 의 배열내 인덱스 찾기.
        if( pcode == productAry[index].pcode ){ // 2. 만약에 삭제할pcode 와 index번째 pcode 와 같으면 
            productAry.splice( index , 1 ); // 3. 배열명.splice( 삭제할인덱스 , 개수 );
            productPrint(); // * 삭제 성공시 화면 새로고침/렌더링 한다. 즉] 출력함수 재호출 *
            break;// 4. 1개만 삭제할 예정이므로 목표(삭제) 이뤘으면 반복문 종료 또는 함수 종료
            // vs return 
        } // if end 
    } // for end 
} // f end 

// 3. 수정함수 : 해당 하는 행의 <수정> 버튼을 클릭하면 수정( 배열변수명[인덱스].속성명= 새로운값 )
function productUpdate( pcode ){
    for( let index = 0 ; index <= productAry.length-1 ; index++ ){// 1. 수정할 pcode의 인덱스를 배열에서 찾는다. <순회>
        if( pcode == productAry[index].pcode ){ //2. 수정할코드 와 index번째 제품(객체) 와 같으면 
            const newName = prompt("수정할 상품명 : "); // 입력 // *추후:수정페이지/모달 사용
            const newPrice = prompt("수정할 가격 : ");
            productAry[index].name = newName;   // 수정 
            productAry[index].price = newPrice;
            productPrint(); // **** 수정 성공시 [즉시] 화면 새로고침/렌더링 ****
            return // vs break; // 수정 성공시 반복문 또는 함수 종료 
        }
    }// for end 
} // f end 
// 4. 등록함수 : 입력받은 값들을 객체(묶어서) 구성하여 배열에 저장( .push )
let pcode = 3; // [전역변수] 처음에는 1로 가정 하고 시작 하되 샘플 데이터가 존재하면 마지막 코드+1
function productAdd( ){  
    // 1. 입력받은 값들을 가져온다.
    const categoryDom = document.querySelector(".category");
    const category = categoryDom.value;                     console.log( category );
    const nameDom = document.querySelector(".name");
    const name = nameDom.value;
    const priceDom = document.querySelector(".price");
    const price = priceDom.value;
    const imageDom = document.querySelector(".image");
    const image = imageDom.files[0]; console.log( image ); // 업로드 한 파일중에서 첫번째 파일 호출
        // 유효성검사1. = 필요  없거나 잘못된 데이터 검증
        if( category == "disabled"){ alert("카테고리를 선택하세요.!"); return; } // 함수종료[ 저장실패 ]
        // 유효성검사2. , return 함수종료 : 아래 코드가 실행안됨.
        if( name == "" || price == "" ){ alert("제품명과 가격은 필수입력 입니다."); return; }
    // ********* new Date() 현재 시스템 날짜/시간 반환 ******
    const year = new Date().getFullYear(); // 현재 연도
    const month = new Date().getMonth()+1; // 현재 월 // + 1월 -> 0 취급 , 2월 -> 1 , 12월 -> 11 , +1한다.
    const day = new Date().getDate(); // getDay 현재 요일 vs getDate 현재 일
    const date = `${ year }-${ month < 10 ? "0"+month : month }-${ day < 10 ? "0"+day : day }`;  // [날짜 두자릿수(문자) 만들기] 만약에 3월 --> 03월 
    // ********* pcode 는 자동으로 마지막 객체의 pcode + 1 *******
    pcode += 1; // 다음 객체는 1증가 한 식별코드를 갖는다.
    // 2. 입력받은 값 과 식별코드+1, 현재날짜( new Date() ) 로 객체를 구성한다.
    const obj = { 
        "pcode" : pcode , 
        // 만약에 업로드된 이미지가 존재하지 않으면 샘플이미지 존재하면 이미지출력 < 미리보기 기능 >
        // URL.createObjectURL( 이미지객체 ) : 이미지객체를 http 주소로 변경
        "image" : image == undefined ? "https://placehold.co/100x100" : URL.createObjectURL( image ) ,
        "ccode" : category , 
        "name" : name ,  "price" : price ,  "date" : date 
    };
    productAry.push( obj );  // 3. 구성한 객체를 배열에 저장한다.
    productPrint(); // 4. 화면 새로고침/렌더링 한다.

} // f end 