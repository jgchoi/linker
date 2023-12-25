/**
* ---------------------------------------------------------------------------------
* | 팝업 |
* ---------------------------------------------------------------------------------
**/

// changeColor ID element 를 취득
let changeColor = document.getElementById("changeColor");

// 스토리지에 저장되어 있는 컬러가 있다면 표시
chrome.storage.sync.get("color", ({ color }) => {
  changeColor.style.backgroundColor = color;
});

// 배경색 버튼을 클릭하였을 경우 이벤트 등록
changeColor.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: convertJSLinkToButtons,
  });
});

/**
 * @description 현재 웹 페이지의 Body 요소의 배경색을 변경해주는 함수
 **/
function convertJSLinkToButtons() {
  let elements = document.querySelectorAll("a[href^='javascript:']");
  for (let element of elements) {
    // Given href ="javascript:$("#id_page_loading%22).show();%20location.href=%22/novel/list/211041%22;"
    let href = element.href;
    // Remove "javascript:$("#id_page_loading%22).show();%20location.href=%22" string from href
    let toRemove = 'javascript:$("#id_page_loading%22).show();%20location.href=%22';
    let result = href.replace(toRemove, '');
    result = result.replace('%22;', '');
    let url = result;
    
    // Create <A href> element
    let button = document.createElement("a");
    button.innerText = "Open";
    button.href = url;
    button.target = "_blank";
    button.style = "display: block;";

    // Insert new Link Button beside the original link
    element.parentNode.insertBefore(button, element.nextSibling);

  }

}
