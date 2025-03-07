document.addEventListener("DOMContentLoaded", function() {
    const objDiv = document.getElementById("content_box");
    const summary_box = document.getElementById("summary_box");
    const summaryList = document.getElementById("summary-list");
    const today = new Date();
    const location = window.location.href;

    const month = today.getMonth() + 1; // getMonth()는 0부터 시작하므로 +1
    const day = today.getDate();
    const formattedDate = `${month}월 ${day}일`;

    const dateReform = document.querySelector(".today-menu-title").innerText.split('\n')[0].trim();

    const currentMonth = month;
    const pageMonth = parseInt(dateReform.match(/(\d+)월/)[1]);
    const pageDay = parseInt(dateReform.match(/(\d+)일/)[1]);
    if (currentMonth !== pageMonth || day !== pageDay) {
        const menuTitleElement = document.querySelector(".today-menu-title");
        menuTitleElement.innerHTML = `${dateReform}<br>지나간 생중계`;
    }
    // if (dateReform !== formattedDate) {
    //     const menuTitleElement = document.querySelector(".today-menu-title");
    //     menuTitleElement.innerHTML = `${dateReform}<br>지나간 생중계`;
    // }

    const articles = {};
    const summaries = {};
    const times = {};
    let articles_state = "";
    let last_index = -1;
    let lastArticleIndex = 0;

    const toggle_btn = document.querySelector(".toggle-btn");
    const today_menu = document.querySelector(".today-menu");
    toggle_btn.addEventListener("click", () => {
        toggle_btn.classList.toggle("close");
        today_menu.classList.toggle("close");
    })

    // 모바일 속기록 AI 요약 버튼 구동
    const stenography_header = document.querySelector(".stenography-content-header");
    const stenography_summary_box = document.querySelector(".stenography-summary");
    const clipboard_copy_btn = document.querySelector(".button.copy");
    stenography_header.children[0].addEventListener("click", () => {
        objDiv.classList.toggle("on");
        clipboard_copy_btn.classList.toggle("on");
        stenography_summary_box.classList.toggle("on");
        stenography_header.children[0].classList.toggle("on");
        stenography_header.children[2].classList.toggle("on");
    })
    stenography_header.children[2].addEventListener("click", () => {
        objDiv.classList.toggle("on");
        clipboard_copy_btn.classList.toggle("on");
        stenography_summary_box.classList.toggle("on");
        stenography_header.children[0].classList.toggle("on");
        stenography_header.children[2].classList.toggle("on");
    })

    const nav_bar_btn = document.querySelector(".nav-icon");
    const black_modal = document.querySelector(".black-modal");
    nav_bar_btn.addEventListener("click", () => {
        today_menu.classList.toggle("on");
        if(black_modal.classList.contains("on")){
            setTimeout(() => {
                black_modal.classList.toggle("on");
            }, 1000)
        } else {
            black_modal.classList.toggle("on");
        }
    })

    black_modal.addEventListener("click", () => {
        today_menu.classList.toggle("on");
        if(black_modal.classList.contains("on")){
            setTimeout(() => {
                black_modal.classList.toggle("on");
            }, 1000)
        } else {
            black_modal.classList.toggle("on");
        }
    })
    
    const stenography_state = document.querySelector(".stenography-state");
    switch(stenography_state.textContent.slice(-2)){
        case "예정":
            if(stenography_state.textContent.slice(-4) === "중계예정"){
                stenography_state.style.background = "#EDAB15"
            } else {
                stenography_state.style.background = "#32824D"
            }
            break;
        case "개시":
        case "중계":
        case "계속":
            stenography_state.style.background = "#EA3A33"
            break;
        case "없음":
            stenography_state.style.background = "#F6F6F6"
            break;
        case "산회":
            stenography_state.style.background = "#37A1ED"
            break;
    }
    stenography_state.style.background = stenography_state.textContent

    // 스크롤을 맨 아래로 이동시키는 함수
    function scrollToBottom() {
        objDiv.scrollTop = objDiv.scrollHeight;
        summary_box.scrollTop = summary_box.scrollHeight;
    }

    function updateArticle() {
        return new Promise((resolve, reject) => {
            fetch(`${location}/article`)
                .then(response => response.json())
                .then(data => {
                    let updateArticle = false;
                    articles_state = data['xdesc'];
                    data['article'].split("- (").forEach((article, index) => {
                        if(index === 0){
                            articles[index] = article
                        } else {
                            let cleanArticle = article.replace(/======================.*?======================/gs, '').trim();
                            cleanArticle = cleanArticle.replace(/(<BR>\s*){2,}/g, '<BR>');
                            let match = cleanArticle.match(/\d{2}:\d{2}/);
                            let time = match[0];
                            let [hour, minute] = time.split(':');
                            let formattedTime = `<span>${hour}시 ${minute}분</span>`;
                            
                            cleanArticle = cleanArticle.replace(/\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)/, '').trim();
                            articles[index] = `${formattedTime}${cleanArticle}`;
                        }
                    });
                    resolve(updateArticle);
                })
                .catch(reject);
        })
    }

    // 서버에서 전달된 JSON 파일 경로를 사용하여 JSON 파일 불러오기
    function updateSummary(live_key) {
        return new Promise((resolve, reject) => {
            fetch(`http://52.79.156.227:8000/list?live_key=${encodeURIComponent(live_key)}`)
                .then(response => response.json())
                .then(data => {
                    let updatedSummaries = false;
                    data.forEach(function(item) {
                        if (!summaries[item.block_index] || summaries[item.block_index] !== item.summary) {
                            summaries[item.block_index] = item.summary;
                            times[item.block_index*1 + 1] = item.time; // 시간도 추가
                            updatedSummaries = true;
                        }
                        last_index = Math.max(last_index, item.block_index);
                    });
                    resolve(updatedSummaries);
                })
                .catch(reject);
        });
    }
    
    // 초기 로딩 시 article 채워넣기
    updateArticle().then(() => {
        let start_time = articles['0'].match(/(\d{1,2}시 \d{1,2}분)/)[0].split(" ");
        let hour = start_time[0].split("시")[0].padStart(2, '0');
        let minute = start_time[1].split("분")[0].padStart(2, '0');

        times[0] = `${hour}:${minute}`;
        let articleHtml = '';

        Object.keys(articles).forEach((index) => {
            if(index !== '0'){
                articleHtml += `<p class="article-content" id="article-${index}">${articles[index]}</p>`;
            }
        })
        objDiv.innerHTML = articleHtml;
        lastArticleIndex = Math.max(...Object.keys(articles).map(Number));
        
        // 초기 로딩 시 summary 추가
        updateSummary(live_key).then(() => {
            console.log('Last index:', last_index);
            let summaryHtml = '';

            Object.keys(summaries).forEach((index) => {
                const formattedSummary = summaries[index].replace(/\n/g, '<br>');
                const time = `${times[index]} ~ ${times[index * 1 + 1]}`;
                summaryHtml += `<li class="summary-content ${index * 1 === last_index ? '' : 'close'}" id="summary-${index}">
                                    <span>${time} 요약</span>
                                    <button class="summary-button">
                                        <img src="/static/images/down_arrow_green.svg" alt="">
                                    </button>
                                    <div class="for-accordian"><p>${formattedSummary}</p></div>
                                </li>`;
            });
            summaryList.innerHTML = summaryHtml;

            // Summary에 이벤트 리스너 추가
            document.querySelectorAll('.summary-content').forEach((summary) => {
                summary.addEventListener("click", () => {
                    summary.classList.toggle("close");
                });
            });

            // 초기 로딩 시 스크롤을 맨 아래로 이동
            scrollToBottom();

            let timer = 30; // 30초부터 시작
            const timerElement = document.querySelector('.spare-time');
            timerElement.innerText = `${timer}초`;
    
            const countdown = setInterval(() => {
                if (timer > 0) {
                    timer--; // 1초 감소
                    timerElement.innerText = `${timer}초`;
                } else {
                    // 타이머가 0이 되면 새로 업데이트하고 다시 30초로 리셋
                    timer = 30;
                    timerElement.innerText = `${timer}초`;
    
                    // 주기적으로 업데이트 및 화면 갱신
                    updateArticle().then(() => {
                        let articleHtml = '';

                        // 기존 article을 유지하고, 새로운 article만 추가
                        Object.keys(articles).forEach((index) => {
                            if (index !== '0' && index >= lastArticleIndex && articles[index].toLowerCase() !== document.querySelector(`#article-${lastArticleIndex}`).innerHTML.toLowerCase()) { // 새로운 index만 추가
                                articleHtml += `<p class="article-content" id="article-${index}">${articles[index]}</p>`;
                            }
                        });
                        if (articleHtml !== '') {  // 새로운 내용이 있을 때만 추가
                            if (document.querySelector(`#article-${lastArticleIndex}`)) {
                                document.querySelector(`#article-${lastArticleIndex}`).remove();
                            }
                            objDiv.insertAdjacentHTML('beforeend', articleHtml);  // 새 기사만 추가
                        }

                        lastArticleIndex = Math.max(...Object.keys(articles).map(Number));
                    });
    
                    updateSummary(live_key).then((updated) => {
                        if (updated) {
                            console.log('New summary found, appending to display');
                            if (summaries[last_index]) {
                                const formattedSummary = summaries[last_index].replace(/\n/g, '<br>'); // 줄바꿈을 <br>로 변환
                                const time = `${times[last_index]} ~ ${times[last_index + 1]}`;
                                const newSummaryHtml = `<li class="summary-content" id="summary-${last_index}">
                                    <span>${time} 요약</span>
                                    <button class="summary-button"><img src="/static/images/down_arrow_green.svg" alt=""></button>
                                    <div class="for-accordian"><p>${formattedSummary}</p></div></li>`;
                                summaryList.insertAdjacentHTML('beforeend', newSummaryHtml);
    
                                document.querySelector(`#summary-${last_index}`).addEventListener("click", () => {
                                    document.querySelector(`#summary-${last_index}`).classList.toggle("close");
                                })
                            }
                        }
                    });

                    stenography_state.textContent = articles_state;
                    switch(articles_state.slice(-2)){
                        case "예정":
                            if(stenography_state.textContent.slice(-4) === "중계예정"){
                                stenography_state.style.background = "#EDAB15"
                            } else {
                                stenography_state.style.background = "#32824D"
                            }
                            break;
                        case "개시":
                        case "중계":
                        case "계속":
                            stenography_state.style.background = "#EA3A33"
                            break;
                        case "없음":
                            stenography_state.style.background = "#F6F6F6"
                            break;
                        case "산회":
                            stenography_state.style.background = "#37A1ED"
                            break;
                    }
                    stenography_state.style.background = stenography_state.textContent
                }
            }, 1000);  // 1초마다 타이머 업데이트
        });
    });

    // 클립보드 복사 기능
    clipboard_copy_btn.addEventListener('click', function() {
        if (!objDiv) {
            console.error('content_box를 찾을 수 없습니다.');
            return;
        }

        // HTML 태그를 제거하고 순수한 텍스트만 추출
        const textToCopy = objDiv.innerText || objDiv.textContent;

        // 임시 텍스트 영역 생성
        const tempTextArea = document.createElement('textarea');
        tempTextArea.value = textToCopy;
        document.body.appendChild(tempTextArea);

        // 텍스트 선택 및 복사
        tempTextArea.select();
        try {
            const successful = document.execCommand('copy');
            const msg = successful ? '클립보드에 복사됐습니다' : '복사 실패';
            alert(msg);
        } catch (err) {
            console.error('클립보드 복사 실패:', err);
        }

        // 임시 텍스트 영역 제거
        document.body.removeChild(tempTextArea);
    });
});