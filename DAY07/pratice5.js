//문제 1
let numbers = [23, 5, 67, 12, 88, 34]
let max = number[0];
for (let i = 1; i < numbers.length; i++) {
    (numbers[i] > max){
        max = numbers[i];
    }
}
console.log(max);

//문제2
let output = "";
for (let a = 5; a <= 5; a--) {
    for (let b = 5; b <= a; b--) {
        output = output + "*";
    }
    console.log(output);
}

//문제3
let userNames = ['김하준', '이서아', '박솔민', '최도윤'];
for (let c = 0; c < userNames; c++) {
    let currentName = userNames[i];
    if (currentName.indexOf("솔") != -1) {
        console.log(currentName);
        break;
    }
}
//문제 4
let seatLayout = [['A1','A2','A3'],['B1']]