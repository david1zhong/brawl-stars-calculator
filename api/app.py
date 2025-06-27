from flask import Flask, render_template, request
import sys
import os

sys.path.append(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

week = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7}

days = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31, "Jun": 30,
        "Jul": 31, "Aug": 30, "Sep": 31, "Oct": 31, "Nov": 30, "Dec": 31}

def calc_passes(gems, season, month, year):
    passes = 0
    when = []
    seasons = []
    start_season = season
    
    for i in range(6):
        start_month = list(months.keys())[list(months.values()).index(month)]
        
        month += 2
        gems += 90
        season += 1
        
        if season == start_season:
            gems -= 90
        
        if gems >= 169:
            gems -= 169
            passes += 1
            when.append(f"Season {season}")
        
        if month > 12:
            month -= 12
            year += 1
            
        end_month = list(months.keys())[list(months.values()).index(month)]
        
        seasons.append({
            'season': season,
            'start': start_month,
            'end': end_month,
            'year': year,
            'gems': gems
        })
    
    return {'passes': passes, 'when': when, 'seasons': seasons}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    data = None
    
    if request.method == 'POST':
        try:
            gems = int(request.form['current_balance'])
            season = int(request.form['season'])
            month = int(request.form['month'])
            year = int(request.form['year'])
            
            results = calc_passes(gems, season, month, year)
            data = {
                'gems': gems,
                'season': season,
                'month': list(months.keys())[month-1],
                'year': year
            }
        except:
            pass
    
    return render_template('index.html', months=list(months.keys()), 
                         results=results, data=data)

if __name__ == '__main__':
    app.run(debug=True)