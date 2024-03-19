import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def fetch_latest_stories():
    url = 'https://time.com'
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html5lib')
        stories = []

        story_elements = soup.find_all('div', class_='partial latest-stories')[0].find_all('li', class_='latest-stories__item')

        for story_element in story_elements[:6]:  # Extracting the latest 6 stories
            title = story_element.find('h3', class_='latest-stories__item-headline').text.strip()
            url = story_element.find('a')['href']
            stories.append({'title': title, 'link': "https://time.com"+url})

        return stories
    else:
        print(f"Failed to fetch Time.com: {r.status_code}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getTimeStories')
def get_time_stories():
    latest_stories = fetch_latest_stories()
    if latest_stories:
        return jsonify(latest_stories)
    else:
        return jsonify({'error': 'Failed to fetch latest stories from Time.com'}), 500

if __name__ == '__main__':
    app.run(debug=True)
