from urllib import parse

with open('./abnormal_urls.txt', 'r') as file:
    with open('./encoded_urls.txt', 'w') as f:
        urls = file.read().split()
        print(urls)
        for url in urls:
            print(url)
            parsed_url = parse.urlparse(url)
            encoded_url = parse.quote(parsed_url.path)


            result = 'https://nas-web-01.bluewhale.kr' + encoded_url + '\n'
            print(result)
            f.write(result)
        

