from flask import Flask, request, url_for, redirect, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/players',methods=['POST'])
def players():
    Country = request.form['element_2']
    batting_ranks = []
    batting_names = []
    batting_countries = []
    URL = f'http://www.relianceiccrankings.com/ranking/odi/batting/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='top100battest')
    rank_elems = results.find_all('td', class_ = 'top100id')
    name_elems = results.find_all('td', class_ = 'top100name')
    country_elems = results.find_all('td', class_ = 'top100nation')
    for rank_elem in rank_elems:
        batting_ranks.append(rank_elem.text)
    for name_elem in name_elems:
        batting_names.append(name_elem.text.strip())
    for country_elem in country_elems:
        batting_countries.append(country_elem.get('title'))
    batting_country_df = pd.DataFrame(list(zip(batting_ranks, batting_names, batting_countries)), columns =['Batting Rank', 'Player Name', 'Country'])
    batting_country_df['Batting Rank'] = pd.to_numeric(batting_country_df['Batting Rank'])
    batting_country_ranks = batting_country_df[batting_country_df['Country'] == Country].reset_index(drop = True)
    #return render_template("home.html", column_names=country_ranks.columns.values, row_data=list(country_ranks.values.tolist()), zip=zip)
    
    bowling_ranks = []
    bowling_names = []
    bowling_countries = []
    URL = f'http://www.relianceiccrankings.com/ranking/odi/bowling/'
    page = requests.get(URL)
    bowling_soup = BeautifulSoup(page.content, 'html.parser')
    bowling_results = bowling_soup.find(id='top100battest')
    bowling_rank_elems = bowling_results.find_all('td', class_ = 'top100id')
    bowling_name_elems = bowling_results.find_all('td', class_ = 'top100name')
    bowling_country_elems = bowling_results.find_all('td', class_ = 'top100nation')
    for bowling_rank_elem in bowling_rank_elems:
        bowling_ranks.append(bowling_rank_elem.text)
    for bowling_name_elem in bowling_name_elems:
        bowling_names.append(bowling_name_elem.text.strip())
    for bowling_country_elem in bowling_country_elems:
        bowling_countries.append(bowling_country_elem.get('title'))
    bowling_country_df = pd.DataFrame(list(zip(bowling_ranks, bowling_names, bowling_countries)), columns =['Bowling Rank', 'Player Name', 'Country'])
    bowling_country_df['Bowling Rank'] = pd.to_numeric(bowling_country_df['Bowling Rank'])
    bowling_country_ranks = bowling_country_df[bowling_country_df['Country'] == Country].reset_index(drop = True)
    #return render_template("home.html", tables=[country_ranks.to_html(index = False, justify = 'center'), bowling_country_ranks.to_html(index = False, justify = 'center')])
    return render_template("home.html", bowling_column_names=bowling_country_ranks.columns.values, batting_column_names=batting_country_ranks.columns.values, bowling_row_data=list(bowling_country_ranks.values.tolist()), batting_row_data=list(batting_country_ranks.values.tolist()), zip=zip)
  
if __name__ == '__main__':
    app.run(debug=True)