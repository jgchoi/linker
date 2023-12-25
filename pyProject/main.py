import requests as rq
from bs4 import BeautifulSoup
import time
import asyncio

def parse_webpage(url, progress_callback=None):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = rq.get(url, headers=headers)

    soup = BeautifulSoup(result.text, "html.parser")

    divClasses = soup.find_all('div', class_='col-12')
    divWithTitle = [divClass for divClass in divClasses if divClass.find('p', string='TXT viewer control')]
    subTitle = divWithTitle[0].find('h2').text if divWithTitle else "Problem"
    progress_callback(subTitle, None)

    titleElements = soup.find_all('h5', class_='mb-0 pt-1')
    title = (titleElements[0].text if titleElements else "Problem")

    #remove special char from title
    title = title.replace('?', '')
    title = title + ".txt"

    # parse content from <div class="viewer_container dotum" id="id_wr_content">
    contentElements = soup.find_all('div', class_='viewer_container dotum')\
    
    # if number of contentElements is 0, then return -1
    if len(contentElements) == 0:
        return -1

    for br in contentElements[0].find_all("br"):
        br.replace_with("\n")

    # Add space between paragraphs
    for p in contentElements[0].find_all("p"):
        p.insert_after("\n")
    
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

async def download_novel(fullUrl, progress_callback=None):
    pageNumber = fullUrl.split('/')[-2]
    url = fullUrl

    while True:
        pageNumber = parse_webpage(url, progress_callback=progress_callback)

        if pageNumber == 0:
            progress_callback('Done', None)
            break
        
        # if -1 is returned, try again with same url
        if pageNumber != -1:
            # Replace pageNumber with the new pageNumber
            # Given url https://agit620.xyz/novel/view/222891/2
            # Replace 222891 to value of pageNumber
            url = url.replace(url.split('/')[-2], str(pageNumber))
            progress_callback(None, url)

            # url = "https://agit620.xyz/novel/view/" + str(pageNumber) + "/2"
   

    # return completion message to async function
    return "Task completed"