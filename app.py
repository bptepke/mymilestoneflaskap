from flask import Flask, render_template, request, redirect
import quandl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

sns.set(style="whitegrid")

# Authenticate quandl account so quandl will serve the data
quandl.ApiConfig.api_key = "rEUZzxLS2ZKmFWRrMG1Q"

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')
  
@app.route('/process_stock', methods=['GET', 'POST'])
def process_stock():
  co = request.form['company']
  #return render_template('about_stock.html')
  dat = get_data(co)
  df = pd.DataFrame(dat,columns=['date', 'close'])
  df['date'] = pd.to_datetime(df['date'])
  df = df.set_index(['date'])
  df.sort_index(inplace=True, ascending=True)
  plot_data = df.loc['2018-1-1':'2018-1-31']
  ax = sns.lineplot(data=plot_data, palette="tab10", linewidth=2.5)
  ax.set(ylabel='Closing Price',title=co)
  img = io.BytesIO()
  plt.savefig(img, format='png')
  img.seek(0)
  plot_url = base64.b64encode(img.getvalue()).decode()
  return '<img src="data:image/png;base64,{}">'.format(plot_url)
  #return render_template('about_stock.html')

  
  
def get_data(company):
    # Specific company must be provided to avoid excessive data volume
    data = quandl.get_table("WIKI/PRICES",ticker = company , paginate=True)
    return data
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
