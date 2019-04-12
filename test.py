import urllib.request, json 


def main():
    try:
        with urllib.request.urlopen("https://www.reddit.com/r/programmerhumor/.json?sort=top&t=week&limit=10") as url:
            posts = json.loads(url.read().decode())["data"]["children"]
        
            for index, post in enumerate(posts):
                if(index > 1):
                    print(post["data"]["url"])
                
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()