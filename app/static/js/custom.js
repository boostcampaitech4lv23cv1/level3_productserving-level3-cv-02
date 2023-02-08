const images = new DataTransfer();
const chooseFile = document.getElementById('chooseFile');

function uploadBoxOnclick(){
    chooseFile.click();
}

function getImageFiles(e) {//파일 추가 업로드 시 리셋되지 않고 뒤에 추가되도록
    const files = e.currentTarget.files;

    if(files != null && files.length>0){
        for(var i=0;i<files.length;i++){
            images.items.add(files[i])
        }
    }
    chooseFile.files = images.files;
    console.log("input FIles =>", chooseFile.files)
    addImages(files);
    e.target.value = ''; //같은 파일 추가 가능하도록 reset
}

chooseFile.addEventListener('change', getImageFiles);//파일 업로드 후 이벤트

/* 이미지 슬라이드 코드 */
const slides = document.querySelector('.slides'); //슬라이드 ul
let slideImg = document.querySelectorAll('.slides li'); //슬라이드 list
const uploadPage = slideImg[0]; //파일 업로드 페이지
let curIdx = 0; //현재 슬라이드 index
let slideCnt = slideImg.length; // 슬라이드 개수
const prev_btn = document.getElementById('prev_btn'); //이전 버튼
const next_btn = document.getElementById('next_btn'); //다음 버튼
const del_btn = document.getElementById('del_btn');

function moveImages(cur, next) {
    
    if(cur > -1) slideImg[cur].hidden=true;
    slideImg[next].hidden=false;
    curIdx = next;
    buttonDisable()
}

function buttonDisable(){
    if(curIdx == 0) prev_btn.disabled = true;
    else prev_btn.disabled = false;

    if(curIdx==slideCnt-1){
        next_btn.disabled = true;
        del_btn.disabled = true;
    } else{
        next_btn.disabled = false;
        del_btn.disabled = false;
    }
}

function prevButton() {
  /*첫 번째 슬라이드로 표시 됐을때는 
  이전 버튼 눌러도 아무런 반응 없게 하기 위해 
  curIdx !==0일때만 moveImages 함수 불러옴 */
    if (curIdx !== 0) moveImages(curIdx, curIdx-1);
};

function nextButton() {
  /* 마지막 슬라이드로 표시 됐을때는 
  다음 버튼 눌러도 아무런 반응 없게 하기 위해
  curIdx !==slideCnt - 1 일때만 
  moveImages 함수 불러옴 */
    if (curIdx !== slideCnt - 1) {
        moveImages(curIdx, curIdx + 1);
    }
};

function delButton() {
    var result = confirm("현재 이미지를 삭제하시겠습니까?")
    if(result){
        slideImg[curIdx].remove();
        slideImg = document.querySelectorAll('.slides li'); //변경된 리스트
        slideCnt = slideImg.length;
        moveImages(-1, curIdx);
        location.replace("/index")
    }
}

/* 이미지 li에 추가하는 함수 */
async function addImages(files){
    slideImg[slideCnt-1].remove();
    
    await Promise.all([...files].map(file => new Promise(resolve =>{
        const reader = new FileReader();
        reader.onload = (e) => {
            const li = createElement(e, file)
            slides.appendChild(li);
            resolve();
        }
        reader.readAsDataURL(file);
    })))

    /* 이미지 추가 후처리 */
    debugger;
    console.log("이미지 추가 후처리")
    slides.appendChild(uploadPage);
    slideImg = document.querySelectorAll('.slides li'); //변경된 리스트
    slideCnt = slideImg.length;
    curIdx = slideCnt - files.length - 1;
    if(curIdx+1==slideCnt) curIdx=0;
    for(var i=0;i<slideCnt;i++){
        slideImg[i].hidden = true;
    }
    slideImg[curIdx].hidden = false;
    buttonDisable();
}

function createElement(e, file) {
    console.log("createElemete:: ", file);
    const li = document.createElement('li');
    const img = document.createElement('img');
    img.setAttribute('src', e.target.result);
    img.setAttribute('data-file', file.name);
    img.setAttribute('width', '100%');
    img.setAttribute('height', '100%');
    img.setAttribute('class', 'image-files');
    li.appendChild(img);

    return li;
  }

  /* 파일 제출 시 확인 코드 */
  function submitConfirm(e){
    let fileCnt = images.files.length;
    if(fileCnt==0){
        alert('한 개 이상의 파일을 업로드 해주세요.');
        return false;
    }
    if(confirm(`이미지를 변환하시겠습니까?`)){
        document.submitFrm.submit();
    }
    // if(confirm(`${fileCnt}개의 이미지를 변환하시겠습니까?`)){
    //     document.submitFrm.submit();
    // }
  }