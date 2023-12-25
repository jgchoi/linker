# Read all files under "files" directory and print out the file name


import requests

def make_api_call(title):
    url = "https://agit501.xyz/novel/search.php"
    headers = {
        "authority": "agit501.xyz",
        "accept": "*/*",
        "accept-language": "ko,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "2a0d2363701f23f8a75028924a3af643=OTkuMjI5LjE2Mi4yMzM^%^3D; e1192aefb64683cc97abb83c71057733=ZnJlZQ^%^3D^%^3D; PHPSESSID=tdauiqtqqdrph5jvar3ua22cgk",
        "dnt": "1",
        "origin": "https://agit501.xyz",
        "referer": "https://agit501.xyz/novel/",
        "sec-ch-ua": '"Not A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        "mode": "get_data_novel_list_p_sch",
        "search_novel": title,
        "list_limit": "0"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()  

def parse_response(response_json):
    # Check if 'list' key exists in the response and it's not empty
    if 'list' in response_json and response_json['list']:
        # Extract the first item in the list
        first_item = response_json['list'][0]
        
        # Check if 'np_author' and 'wr_subject2' keys exist in the first item
        if 'np_author' in first_item and 'wr_subject2' in first_item:
            np_author = first_item['np_author']
            # remove any special characters from the author name like (\t, \n, \r, etc.)
            np_author = np_author.strip()
            wr_subject2 = first_item['wr_subject2'] 

            # Given wr_sumject "가니메데 게이트-277화", extract the number 277, int only
            if '-' in wr_subject2 and '화' in wr_subject2:
                wr_subject2 = int(wr_subject2.split('-')[1].split('화')[0])
            else:
                wr_subject2 = 000
            
            return np_author, wr_subject2

    return None, None

# function that takes title, call make_api_call, return prased_response
def get_author_and_episode(title):
    response_json = make_api_call(title)
    return parse_response(response_json)