boardPrint();
function boardPrint(){
    const boardTbody = document.querySelector("#boardTbody");
    let boardList = localStorage.getItem("boardList");
    if(boardList==null){boardList=[]}
    else{boardList = JSON.parse(boardList)};
    let html = ``
    for(let index=0; index<=boardList.length-1; index++){
        const obj =boardList[index];
    
    html += `<tr>
    <td>${obj.no}</td>
    <td><a href="view.html?no=${obj.no}">${obj.title}</a></td>
    </tr>`
    
    
    
    }
    boardTbody.innerHTML=html;
}