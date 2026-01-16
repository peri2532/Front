function boardWrite(){
    const titleInput = document.querySelector("#titleInput");
    const contentInput = document.querySelector("#contentInput");
    const pwdInput = document.querySelector("#pwdInput");
    const title = titleInput.value;
    const content = contentInput.value;
    const pwd = pwdInput.value;
    const obj = { title , content, pwd};
    let boardList = localStorage.getItem("boardList");
    if(boardList==null){boardList=[]}
    else{boardList = JSON.parse(boardList)};
    obj.no = boardList.length==0?1:boardList[boardList.length-1].no+1;
    boardList.push(obj);
    localStorage.setItem('boardList',JSON.stringify(boardList));
    alert("게시글 저장 완료!");
    location.href="list.html"
}