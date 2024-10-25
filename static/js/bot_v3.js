document.addEventListener('DOMContentLoaded', function() {
    const stenography_list = [...document.querySelector(".stenography-wrap").children];
    const stenography_active_list = [...document.querySelector(".stenography-active").children];
    const ai_guide_btn = document.querySelector(".ai-guide");
    const ai_guide_open_btn = document.querySelector(".ai-guide-accordian-button");
    const ai_guide_content = document.querySelector(".ai-guide-content");
    const black_modal = document.querySelector(".black-modal");
    const error_black_modal = document.querySelector(".error-black-modal");
    const date_list = document.querySelector(".date-list");
    const date_dropDown_btn = document.querySelector(".date-dropDown-menu");
    const stenography_desc = {};
    const stenography_active = {};
    const stenography_code = {};
    const today = new Date();
    const original_location = window.location.href;

    const year = today.getFullYear();
    const month = today.getMonth() + 1; // getMonth()는 0부터 시작하므로 +1
    const day = today.getDate();
    const formattedDate = `${month}월 ${day}일`;

    const URLDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    // 전날
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    const yesterdayYear = yesterday.getFullYear();
    const yesterdayMonth = yesterday.getMonth() + 1;
    const yesterdayDay = yesterday.getDate();
    const yesterdayURLDate = `${yesterdayYear}-${String(yesterdayMonth).padStart(2, '0')}-${String(yesterdayDay).padStart(2, '0')}`;

    // 전전날
    const dayBeforeYesterday = new Date(today);
    dayBeforeYesterday.setDate(today.getDate() - 2);
    const dayBeforeYesterdayYear = dayBeforeYesterday.getFullYear();
    const dayBeforeYesterdayMonth = dayBeforeYesterday.getMonth() + 1;
    const dayBeforeYesterdayDay = dayBeforeYesterday.getDate();
    const dayBeforeYesterdayURLDate = `${dayBeforeYesterdayYear}-${String(dayBeforeYesterdayMonth).padStart(2, '0')}-${String(dayBeforeYesterdayDay).padStart(2, '0')}`;

    const DateList = [String(day).padStart(2, '0'), String(yesterdayDay).padStart(2, '0'), String(dayBeforeYesterdayDay).padStart(2, '0')]
    const URLDateList = [URLDate, yesterdayURLDate, dayBeforeYesterdayURLDate];

    const dateReform = document.querySelector(".today-menu-title").innerText.split('\n')[0].trim();

    if (dateReform !== formattedDate) {
        const menuTitleElement = document.querySelector(".today-menu-title");
        menuTitleElement.childNodes[0] = dateReform;
        menuTitleElement.childNodes[4].textContent = "지나간 생중계";
    }
    
    setTimeout(() => {
        error_black_modal.style.opacity = 0;
        setTimeout(() => {
            error_black_modal.style.display = "none";
        }, 1000)
    },2000)

    date_dropDown_btn.addEventListener("click", () => {
        date_list.classList.toggle("open");
        date_dropDown_btn.classList.toggle("open");
    })

    date_list.childNodes.forEach((v, index) => {
        if(index%2){
            v.innerHTML = `<a class="date-link ${original_location.slice(-2) === DateList[(index-1)/2] ? "now" : ""}" href="/donga/gookhwe/${URLDateList[(index-1)/2]}">${DateList[(index-1)/2]}일</a>`
        }
    })

    ai_guide_btn.addEventListener("click", () => {
        ai_guide_content.classList.toggle("close");
        black_modal.classList.toggle("on");
        if(ai_guide_content.classList.contains("open")){
            ai_guide_content.classList.remove("open");
            ai_guide_open_btn.children[0].classList.remove("open");
        }
    })
    
    black_modal.addEventListener("click", () => {
        ai_guide_content.classList.toggle("close");
        setTimeout(() => {
            black_modal.classList.toggle("on");
        }, 500)
        if(ai_guide_content.classList.contains("open")){
            ai_guide_content.classList.remove("open");
            ai_guide_open_btn.children[0].classList.remove("open");
        }
    })
    
    ai_guide_open_btn.addEventListener("click", () => {
        ai_guide_content.classList.toggle("open");
        ai_guide_open_btn.children[0].classList.toggle("open");
        ai_guide_content.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    })

    const toggle_btn = document.querySelector(".toggle-btn");
    const today_menu = document.querySelector(".today-menu");
    toggle_btn.addEventListener("click", () => {
        toggle_btn.classList.toggle("close");
        today_menu.classList.toggle("close");
    })

    function updateStenographyState() {
        return new Promise((resolve, reject) => {
            fetch(`${original_location}/list`)
                .then(response => response.json())
                .then(data => {
                    data.forEach((v, index) => {
                        stenography_active[index] = v.active;
                        stenography_desc[index] = v.xdesc;
                        stenography_code[index] = v.xcode;
                    });
                    resolve();
                })
                .catch(reject);
        })
    }

    setInterval(() => {
        updateStenographyState().then(() => {
            stenography_list.forEach((v, index) => {
                if(index > 2 && index%3 === 1){
                    if(v.textContent !== stenography_desc[Math.floor(index/3) - 1]){
                        v.textContent = stenography_desc[Math.floor(index/3) - 1];
                    }
                }
            })

            stenography_active_list.forEach((v, index) => {
                if(index> 0){
                    if (stenography_active[index - 1] !== v.children[0].getAttribute('data-url')) {
                        v.innerHTML = `<a data-url="TRUE" class="stenography-link" href="/donga/gookhwe/${original_location.slice(-10)}/${stenography_code[index - 1]}">속기록 확인</a>`;
                    }
                }
            })
        });
    }, 30000)
    //     if (event.target.classList.contains('button')) {
    //         const ind = event.target.id;
    //         const url = event.target.name;
    //         const press = event.target.value;
    //         const title = event.target.title;

    //         document.getElementById(ind).classList.add('writen');

    //         // if(clicked != 'avoid'){
    //         // document.querySelectorAll('tr').forEach(function(sibling) {
    //         //     sibling.classList.remove('onclick');
    //         // });
    //         // event.target.classList.add('onclick');
    //         // }

    //         // AJAX 요청 처리
    //         const xhr = new XMLHttpRequest();
    //         xhr.open('POST', '/donga/dangbun/naver/write', true);
    //         xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    //         xhr.onreadystatechange = function() {
    //             if (xhr.readyState === 4 && xhr.status === 200) {
    //                 const data = xhr.responseText;

    //                 const brRegex = /<br\s*[\/]?>/gi;
    //                 const textArea = document.createElement('textarea');
    //                 textArea.value = data.replace(brRegex, "\r\n");
    //                 document.body.appendChild(textArea);
    //                 textArea.select();
    //                 document.execCommand('copy');
    //                 document.body.removeChild(textArea);

    //                 alert(data + "\n\n\n클립보드에 복사됐습니다");
    //                 // console.log(data)
    //                 // document.getElementById('content').innerHTML = data;
    //             }
    //         };

    //         // 데이터를 URL 인코딩하여 전송
    //         const params = 'ind=' + encodeURIComponent(ind) +
    //                        '&url=' + encodeURIComponent(url) +
    //                        '&press=' + encodeURIComponent(press) +
    //                        '&title=' + encodeURIComponent(title) +
    //                        '&cmd=readall';
    //         xhr.send(params);

    //         // 아직 on click
    //         // event.preventDefault();
    //     }
    // });
});