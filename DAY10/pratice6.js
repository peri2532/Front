//문제1
let name1=prompt("제품명 입력: ");
let name2=prompt("가격 입력: ");
let name3=prompt("제조사 입력: ");
let product={"제품명" : name1 ,"가격" : name2, "제조사":name3 };
console.log(product);

//문제2

let admin1=prompt("아이디 입력: ");
let admin2=prompt("비밀번호 입력: ");
let admin3=prompt("이름 입력: ");
let member ={"아이디" : admin1 , "비밀번호" : admin2 , "아이디" : admin3};
console.log(member);

//문제3
const scores = [
    {name: "A" , math : 80 , science:92},
    {name: "B" , math : 95 , science:88},
    {name: "C" , math : 76 , science:78},
]
let math = scores.math(keys);
let  score = math/3;

//문제4
const products = [
    {id:1, name : '사과'},
    {id : 2, name : '바나나'},
    {id : 3, name : '포도'},
    {id : 4, name : '딸기'}
]
console.log(`${products[2]}`);
