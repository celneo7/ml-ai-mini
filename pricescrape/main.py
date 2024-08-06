from bs4 import BeautifulSoup
import requests

# code referenced from https://www.geeksforgeeks.org/scraping-amazon-product-information-using-beautiful-soup/

def main(urls):
    file = open("output.csv", "w")

    # write headers for csv file
    file.write('title,price,rating,number,avail\n')

    headers = ({
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })


    for url in urls:
        
        web = requests.get(url, headers=headers)

        soup = BeautifulSoup(web.content, "lxml")


        # get the required details if have
        try:
            title = soup.find("span", attrs={
                "id":"productTitle"
            }).string.strip().replace(",","")

        except AttributeError:
            title = "NA"


        try:
            price = soup.find("span", attrs={
                "class":"a-offscreen"
            }).string.strip()

        except AttributeError:
            price = "NA"


        try:
            rating = soup.find("span", attrs={
                "class":"a-size-base a-color-base"
            }).string.strip()

        except AttributeError:
            rating = "NA"    


        try:
            number = soup.find("span", attrs={
                "id":"acrCustomerReviewText"
            }).string.strip().replace("ratings", "")

        except AttributeError:
            number = "NA"    

        try:
            avail = soup.find("div", attrs={
                "id":"availability"
            }).string.strip()

        except AttributeError:
            avail = "NA"    

        # write in the output file
        file.write(f'{title},{price},{rating},{number},{avail}\n')

    file.close()

if __name__ == "__main__":
    file = open("url.txt", "r")
    main(file)