from flask import Flask, render_template, request

app = Flask(__name__)

# Your original dictionaries
months = {"Jan": 1,
          "Feb": 2,
          "Mar": 3,
          "Apr": 4,
          "May": 5,
          "Jun": 6,
          "Jul": 7,
          "Aug": 8,
          "Sep": 9,
          "Oct": 10,
          "Nov": 11,
          "Dec": 12}

week = {"Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6,
        "Sun": 7}

days = {"Jan": 31,
        "Feb": 28,
        "Mar": 31,
        "Apr": 30,
        "May": 31,
        "Jun": 30,
        "Jul": 31,
        "Aug": 30,
        "Sep": 31,
        "Oct": 31,
        "Nov": 30,
        "Dec": 31}

def calculate_brawl_pass(current_balance, season, month, year):
    brawl_pass_count = 0
    when_brawl_pass = []
    new_when_brawl_pass = []
    current_season = [season]
    season_details = []
    
    for x in range(0, 6):
        start_month = (list(months.keys())[list(months.values()).index(month)])
        # Month Brawl Pass starts
        month += 2
        current_balance += 90
        season += 1
        if season == [a for a in current_season]:
            current_balance -= 90
            # Don't add 90 gems for current season
            '''if current_balance >= 169:
                 current_balance = current_balance + 169'''
            # Only enable if not buying current seasons' brawl pass
        if current_balance >= 169:
            current_balance -= 169
            brawl_pass_count += 1
            when_brawl_pass.append(str(season))
            # Assuming you buy the brawl pass as soon as you get the amount of gems
        if month > 12:
            month -= 12
            year += 1
        end_month = (list(months.keys())[list(months.values()).index(month)])
        # Month Brawl Pass ends
        
        # Store season details for display
        season_details.append({
            'season': season,
            'start_month': start_month,
            'end_month': end_month,
            'year': year,
            'balance': current_balance
        })
    
    for x in when_brawl_pass:
        new_when_brawl_pass.append(f"Season {x}")
    
    return {
        'brawl_pass_count': brawl_pass_count,
        'when_brawl_pass': new_when_brawl_pass,
        'season_details': season_details
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    input_data = None
    
    if request.method == 'POST':
        try:
            current_balance = int(request.form['current_balance'])
            season = int(request.form['season'])
            month = int(request.form['month'])
            year = int(request.form['year'])
            
            # Call your original function
            results = calculate_brawl_pass(current_balance, season, month, year)
            input_data = {
                'current_balance': current_balance,
                'season': season,
                'month': list(months.keys())[month-1],
                'year': year
            }
        except (ValueError, KeyError):
            pass
    
    return render_template('index.html', 
                         months=list(months.keys()),
                         results=results,
                         input_data=input_data)

if __name__ == '__main__':
    app.run(debug=True)