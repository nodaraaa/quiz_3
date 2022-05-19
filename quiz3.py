import requests
import sqlite3
import json
serialis_saxeli= input("shemoitane serialis saxeli:")
response = requests.get(f"https://api.tvmaze.com/search/shows?q={serialis_saxeli}")
information = json.loads(response.text)
while True:
    if len(information) == 0:
        print("informacia ar moidzebna , tavidan scade")
        seriali = input("shemoitane serialis saxeli:")
        response = requests.get(f"https://api.tvmaze.com/search/shows?q={seriali}")
        information = json.loads(response.text)
        for element in information:
            print(json.dumps(element, indent=4))
        break
    else:
        for element in information:
            print(element)
        break

connection = sqlite3.connect("shows_api.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS   api_shows(name VARCHAR(70)  ,
                                                                  language VARCHAR (25),
                                                                  genres VARCHAR (50),
                                                                  officialsite VARCHAR (100))''')
for each in information:
    cursor.execute('''INSERT INTO api_shows (name,language,genres,officialsite) VALUES ( ?, ?, ?, ?)''',
                       (each['show'].get('name'), each['show'].get('language'), str(each['show'].get('genres')), str(each['show'].get('officialSite'))))
    connection.commit()
print("informacia chaiwera")
print("--------------------------------------------")
print("amjamad bazashi chawerili informacia")
new_info = cursor.execute("SELECT * FROM api_shows")
for i in new_info:
    print(i)
cursor.close()
connection.close()