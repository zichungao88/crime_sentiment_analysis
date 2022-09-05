import pandas, os
from flask import Flask, render_template

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

data_file_crime = pandas.read_csv('howard-daily-crime-bulletin.csv')
publish_date = data_file_crime['publish_date']
category = data_file_crime['category']
city = data_file_crime['city']
zip_code = data_file_crime['zip_code']
street = data_file_crime['street']
crime_date = data_file_crime['crime_date']
crime_time = data_file_crime['crime_time']
add_notes = data_file_crime['add_notes']
data_array = []

for i in range(len(data_file_crime)):
    record = []
    record.append(publish_date[i])
    record.append(category[i])
    record.append(city[i])
    record.append(zip_code[i])
    record.append(street[i])
    # if crime_date[i] is None:
    #     crime_date[i] = ''
    record.append(crime_date[i])
    # if crime_time[i] is None:
    #     crime_time[i] = ''
    record.append(crime_time[i])
    # if add_notes[i] is None:
    #     add_notes[i] = ''
    record.append(add_notes[i])
    data_array.append(record)

headings = ('Dated Published', 'Crime Category', 'City', 'Zip Code', 'Address', 'Date Committed', 'Time Committed', 'Additional Notes and References')

graph_crime_type = []
graph_crime_type_list = []
simplified_graph_crime_type = []
# robbery = []
# residential_burglary = []
# commercial_burglary = []
# vehicle_theft = []
# vehicle_break_in = []
# home_invasion_robbery = []
# weapon_violation = []

for i in data_array:
    graph_crime_type.append(i[1])
graph_crime_type = set(graph_crime_type)

for i in graph_crime_type:
    graph_crime_type_list.append(i)
graph_crime_type_list.sort()
print(graph_crime_type_list)

for i in range(len(graph_crime_type)):
    crime_count = 0
    for j in range(len(data_array)):
        if graph_crime_type_list[i] == data_array[j][1]:
            crime_count += 1
    simplified_graph_crime_type.append((graph_crime_type_list[i], crime_count))


@app.route('/')
def table():
    return render_template('main.html', headings=headings, data=data_array)


@app.route('/graph/')
def graph():
    labels = [row[0] for row in simplified_graph_crime_type]
    values = [row[1] for row in simplified_graph_crime_type]
    return render_template('graph.html', labels=labels, values=values)


@app.route('/graph_month/')
def graph_month():
    return None


@app.route('/graph_crime_type')
def graph_crime_type():
    return None


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/index/')
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."


if __name__ == '__main__':
    app.run(debug=True)
