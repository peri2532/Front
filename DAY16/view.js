getBoard();
function getBoard(){
    const url= new URLSearchParams(location.search);
    const selectNo = url.get(`no`);
    let boardList = localStorage.getItem('boardList');
    if(boardList == null){boardList=[]}
    else{boardList =JSON.parse(boardList);}

    for(let index = 0; index<=boardList.length-1; index++){
        const obj = boardList[index];
        if(obj.no == selectNo){
            document.querySelector("#title").innerHTML = obj.title
            document.querySelector("#content").innerHTML= obj.content;
            return;
        }
    }
}