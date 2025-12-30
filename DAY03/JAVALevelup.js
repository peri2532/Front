let num = Number(prompt("정수를 입력해주세요: "));
let sec = num%60;
let totalmin = (num - sec)/60;
let min = totalmin %60;
let hour = (totalmin - min) / 60;
let 초= sec<10 ? `0${sec}` : `${sec}`;
let 분= min<10 ? `0${min}` : `${min}`;
let 시= hour<10 ? `0${hour}` : `${hour}`;
console.log(`${시}:${분}:${초}`);


//문제2
let hournum1 = Number(prompt('입차시각 시간(hour)을 적어주세요: '));
let minnum1= Number(prompt("입차시각 분(min)을 적어주세요: "));
let hournum2 = Number(prompt("출차시각 시간(hour)을 적어주세요: "));
let minnum2 = Number(prompt("출차시각 분(min)을 적어주세요: "));
let total1=hournum1*60+minnum1;
let total2=hournum2*60+minnum2;
let total3=total2-total1
namugi = total3-30
namugi2=namugi / 10
yogum=namugi2*1000+3000


