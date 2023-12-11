import requests as rq
from bs4 import BeautifulSoup
import time

def parse_webpage(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = rq.get(url, headers=headers)

    soup = BeautifulSoup(result.text, "html.parser")

    """
    Given
    <div class="col-12">
      <p style="text-align: right;font-size: 14px;color: #a3580d;">TXT viewer control</p>
      <h2 style="font-size: 12pt;width:100%;margin-top: 10px;color: #ccc;">환생한 암살자는 검술 천재-731화</h2>
   </div>
   Find div class with "TXT viewer control" and get the h2 element
    """
    divClasses = soup.find_all('div', class_='col-12')
    # filter divClasses if p element contains "TXT viewer control"
    divWithTitle = [divClass for divClass in divClasses if divClass.find('p', string='TXT viewer control')]
    # get the h2 element
    subTitle = divWithTitle[0].find('h2').text if divWithTitle else "Problem"
    print(subTitle)

    titleElements = soup.find_all('h5', class_='mb-0 pt-1')
    title = (titleElements[0].text if titleElements else "Problem") + ".txt"

    # parse content from <div class="viewer_container dotum" id="id_wr_content">
    contentElements = soup.find_all('div', class_='viewer_container dotum')

    for br in contentElements[0].find_all("br"):
        br.replace_with("\n")
    
    content = contentElements[0].text if contentElements else "Problem"

    # Given html element <a href="javascript:fn_goto_page('next', 3112851);" style="width:100%;font-size: 30px;" class="btn btn-primary ">다음화</a>
    # Get the next page number
    try:
        nextPageNumber = soup.find('a', class_='btn btn-primary')['href'].split("'")[2]
        # convert ", 3112851);" into number
        nextPageNumber = int(nextPageNumber.split(',')[1].split(')')[0])
    except TypeError:
        print(result.text)
        nextPageNumber = 0

    # Read the existing content
    try:
        with open(title, 'r', encoding='utf-8') as file:
            old_content = file.read()
    except FileNotFoundError:
        old_content = ''

    # Write the new content followed by the old content
    with open(title, 'w', encoding='utf-8') as file:
        file.write(old_content + '\n' + content)

    return nextPageNumber

pageNumber = 456401
url = "https://agit620.xyz/novel/view/" + str(pageNumber) + "/2"

while True:
    # Give 5 sec delay
    time.sleep(1)
    pageNumber = parse_webpage(url)
    url = "https://agit620.xyz/novel/view/" + str(pageNumber) + "/2"
    print(url)
    if pageNumber == 0:
        break