import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
                        #Question 1: Use yfinance to Extract Stock Data
#1)Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object.The stock is Tesla and its ticker symbol is TSLA.
tesla = yf.Ticker("TSLA")
#2)Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data.
#Set the period parameter to max so we get information for the maximum amount of time.
tesla_data = tesla.history(period="max")
#3)Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the
#head function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
tesla_data.reset_index(inplace=True)
tesla_data.head()
                            #Question 2: Use Webscraping to Extract Tesla Revenue Data
#1)Use the requests library to download the webpage. Save the text of the response as a variable named html_data.
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data  = requests.get(url).text
#2)Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data,"html5lib")
#3)Using beautiful soup extract the table with Tesla Quarterly Revenue and store it into a dataframe named tesla_revenue.
#The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column.
#If you parsed the HTML table by row and column you can use the replace function on the string
#    revenue = col[1].text.replace("$", "").replace(",", "")
#If you use the read_html function you can use the replace function on the string representation of the column
#    tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "").str.replace(",", "")
tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        date = col[0].text
        revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
print(tesla_revenue)
#4)Remove the rows in the dataframe that are empty strings or are NaN in the Revenue column. Print the entire tesla_revenue DataFrame to see if you have any.
#If you have NaN in the Revenue column
#    tesla_revenue.dropna(inplace=True)
#If you have emtpty string in the Revenue column
#    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.drop([44,47], axis = 0, inplace=True)
tesla_revenue.reset_index(drop=True, inplace=True)
print(tesla_revenue)
#5)Display the last 5 row of the tesla_revenue dataframe using the tail function. Take a screenshot of the results.
print(tesla_revenue.tail())
                            #Question 3: Use yfinance to Extract Stock Data
#1)Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object.
#The stock is GameStop and its ticker symbol is GME.
gme = yf.Ticker("GME")
#2)Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data.
#Set the period parameter to max so we get information for the maximum amount of time.
gme_data = gme.history(period="max")
#3)Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe
#using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
gme_data.reset_index(inplace=True)
gme_data.head()
                            #Question 4: Use Webscraping to Extract GME Revenue Data
#1)Use the requests library to download the webpage https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue. Save the text of the response as a
#variable named html_data.
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data  = requests.get(url).text
#2)Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data,"html5lib")
#3)Using beautiful soup extract the table with GameStop Quarterly Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns
#Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column using a method similar to what you did in Question 2.
tables = soup.find_all('table')
#print(len(tables))
for index,table in enumerate(tables):
    if ("GameStop Quarterly Revenue" in str(table)):
        table_index = index
#print(table_index)
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        date = col[0].text
        revenue = col[1].text.replace("$", "").replace(",", "")
        gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
print(gme_revenue)
#4)Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.
print(gme_revenue.tail())
                            #Question 5: Plot Tesla Stock Graph
#1)Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the make_graph function
#is make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(tesla_data, tesla_revenue, 'Tesla Stock Data')
                            #Question 6: Plot GameStop Stock Graph
#1)Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph function is
make_graph(gme_data, gme_revenue, "GameStop")
