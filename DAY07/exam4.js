//  [1] for 중첩 : for문 안에 for
// (1) 2단 구구단
for (let 곱 = 1; 곱 <= 9; 곱++) { //곱이 1부터 9까지 1씩 증가
    console.log(`2 * ${곱} = ${2 * 곱}`);
}

//(2) 2단 ~ 9단
for (let 단 = 2; 단 <= 9; 단++) {
    console.log(`${단} * 1 = ${단 * 1}`);
}

//(3) 1. 곱 마다 단을 계산하는건지[X] 2. 단 마다 곱을 계산하는거지[O]
// 2단일 때 9번 곱을 해야하고 3단일 때 9번 곱을 해야하고...

for (let 단 = 2; 단 <= 9; 단++) {
    for (let 곱 = 1; 곱 <= 9; 곱++) { //곱이 1부터 9까지 1씩 증가
        console.log(`${단}* ${곱} = ${단 * 곱}`);
    }// 곱 END
} //단 END //즉 : 곱은 단마다 9번씩 실행된다. 총 실행횟수는 72회 반복

//[2] 별 출력하기
/*             line(row)    star(colum)         
*                   1           1               첫번째줄의 별 1개 출력  line은 1부터 5까지 1씩증가하면서 줄바꿈(\n) ,
**                  2           1 2             두번째줄의 별 2개 출력  star는 1부터 현재 라인까지 1싹 증가하면서 "*"을 출력
***                 3           1 2 3           세번째줄의 별 3개 출력
****                4           1 2 3 4         네번째줄의 별 4개 출력
*****               5           1 2 3 4 5       다섯번째줄의 별 5개 출력
찾은 패턴 1: line은 1부터 5까지 1씩증가하면서 줄바꿈(\n)
찾은 패턴 2: star는 1부터 현재 라인까지 1싹 증가하면서 "*"을 출력*/

// (1)
// let output = ""; //출력할 문자열 선언

// for (let line =1 ; line<=5; line++){
//     output = output + "/n"}
//     //console.log(``)}
// 예상: "\n\n\n\n\n"

// (2)
// for(let star=1; star<= 5; star++){
//     output=output+ "*";}

// 예상: output = "\n\n\n"

//(3) 1. 줄마다 별 출력할건지?(o)[별 출력 후 줄 바꿈] 2. 별마다 줄 출력하는건지?
let output = "";//출력할 문자열 선언

for (let line = 1; line <= 5; line++) {
    for (let star = 1; star <= line; star++) {
        output = output + "*"; //총 합계와 동일하게 문자열 출력
    } output = output + "/n"; //줄바꿈처리
    console.log(output);
}
//예상하기 output,line 1일때, *\n
//line2일때 , *\n**\n
//line3일때 , *\n**\n***\n
//line4일때 , *\n**\n***\n****\n
//line5일때 , *\n**\n***\n****\n*****\n

//[3] 반복문과 자주 사용되는 키워드 
// (1) continue;
for (let i = 1; i <= 5; i++) {
    if (i == 3) {
        continue; //만약에 i(반복변수)가 3일때 반복문으로 이동<이하 코드 실행 안됨>
        console.log(i); // 1 2 4 5 , 1부터 3 제외한 5까지 출력됨 이유: 3일때 continue 만났기 때문에
    }//for end
//(2) break 
    for (let i = 1; i <= 5; i++) {
    if (i == 3) {break}//만약에 i(반복변수)가 3일때 반복문 탈출/종료<이하코드 실행안됨>
    console.log(i); // 1 2  , 1부터 5까지 출력하되 3이면 종류, 이유: 3일때 break 만났기 때문에
  }
//(3) 무한루프 :종료가 없는 계속되는 반복문
//방법1:for( ; ; ){console.log(1);}
//방법2:while(true){console.log(1);}
//활용1 : for( ; ; ){let a = prompt("무한입력:");}
//활용2 : for( ; ; ){let a = prompt("무한입력: "); if( b == "x") break;}