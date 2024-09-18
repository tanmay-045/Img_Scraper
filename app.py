from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename="scraper.log" , level=logging.INFO)
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:

                    # query to search for images
                    query = request.form['content'].replace(" ","")

                            # directory to store downloaded images
                    save_directory = "images/"

                            # create the directory if it doesn't exist
                    if not os.path.exists(save_directory):
                        os.makedirs(save_directory)



                            # fake user agent to avoid getting blocked by Google
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

                            # fetch the search results page
                    response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=e9ea40622f6d2cac&sca_upv=1&sxsrf=ADLYWIJvxGBAawjZDqNkBcXT27Bkkna7FA:1726659811020&source=hp&biw=1366&bih=641&ei=4rzqZrabO-i9vr0P2aHH2Qg&iflsig=AL9hbdgAAAAAZurK88tvd2dl6YRoPu695TYUKtZCzuii&ved=0ahUKEwi2lLmFtcyIAxXonq8BHdnQMYsQ4dUDCBA&uact=5&oq=spider+man&gs_lp=EgNpbWciCnNwaWRlciBtYW4yCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMgUQABiABDIIEAAYgAQYsQMyCBAAGIAEGLEDMgsQABiABBixAxiDATIIEAAYgAQYsQMyCBAAGIAEGLEDSP4yUOURWPUvcAJ4AJABAZgBjgSgAeoQqgELMC45LjAuMS4wLjG4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ5gCDKAC5w-oAgrCAgcQIxgnGOoCwgIEECMYJ5gDH5IHCTIuOC4xLjAuMaAH0T0&sclient=img&udm=2")


                            # parse the HTML using BeautifulSoup
                    soup = BeautifulSoup(response.content, "html.parser")

                            # find all img tags
                    image_tags = soup.find_all("img")

                            # download each image and save it to the specified directory
                    del image_tags[0]
                    img_data=[]
                    for index,image_tag in enumerate(image_tags):
                                # get the image source URL
                                image_url = image_tag['src']
                                #print(image_url)
                                
                                # send a request to the image URL and save the image
                                image_data = requests.get(image_url).content
                                mydict={"Index":index,"Image":image_data}
                                img_data.append(mydict)
                                with open(os.path.join(save_directory, f"{query}_{image_tags.index(image_tag)}.jpg"), "wb") as f:
                                    f.write(image_data)
                    client = pymongo.MongoClient("mongodb+srv://tanmaysharma123:tanmay123@cluster0.czeutbt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
                    db = client['scraping']
                    review_col = db['scrapping_data']
                    review_col.insert_many(img_data)          

                    return "image laoded"
                except Exception as e:
                    logging.info(e)
                    return 'something is wrong'
            # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 