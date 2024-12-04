from flask import Flask, jsonify, request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import requests
import re
import json
app = Flask(__name__)

@app.route('/amazon')
@app.route('/amazon/')
@app.route('/amazon/<search_query>', methods=['GET'])
def amazon(search_query = None):
  data = search_query
  headers = {"FUser":"An", 'User-Agent': 'Mozilla/4.0'}
  if data == None:
    return render_template('productos.html', data = None)
  url = "https://www.amazon.com/s?k={}".format(data)
  r = requests.get(url,headers=headers)
  if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html.parser')
    urls =soup.find('div',attrs={"class":"s-main-slot s-result-list s-search-results sg-row"}).find_all('a', attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    nombres = soup.find('div',attrs={"class":"s-main-slot s-result-list s-search-results sg-row"}).find_all('span', attrs={"class": re.compile(r"\b(a-color-base a-text-normal)\b")})
    urls = ["https://www.amazon.com/" + i.get('href') for i in urls[:5] ]
    nombres = [ i.text for i in nombres[:5] ]
    scraping = {"urls":urls, "nombres":nombres}
    combinate = list(zip(scraping["urls"], scraping["nombres"]))
    return render_template('productos.html', scraping = combinate)
  else:
    answer = "Fallo Respuesta"
    return redirect(url_for('index'))
  
@app.route('/search')
def search_amazon_redirect():
    query = request.args.get('query', '')
    if query:
        return redirect(url_for('amazon', search_query=query))
    return redirect(url_for('index'))
  
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True, port=5000,host="0.0.0.0")