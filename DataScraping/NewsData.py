#Parsing another website to get each teams' relevant news data
for team in teams:
    team: str
    teamName = team.lower().replace(' ', '-')
    print(team, teamName)
    page = 1
    weekAgoReached = False
    print(weekAgoReached)
    while not weekAgoReached:
        print(page)
        link = f'https://www.football365.com/{teamName}/news' if page == 1 else f'https://www.football365.com/{teamName}/page/{page}'
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'lxml')
        articleComponents = [article for article in soup.find_all(class_='news-card') if not article.find_parent('aside')] # only want news articles in the main section of the page

        print(len(articleComponents))
        
        #Parsing each article component/card one by one
        for articleComponent in articleComponents:

            categories = []
            categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag')]
            categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag-1')]

            if team not in categories: # skipping news articles not related to the team
                continue

            timeTag = articleComponent.find('time')
            if timeTag:
                postTime = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', timeTag['datatime']), "%A %d %B %Y %I:%M %p")
                postTime = postTime.replace(tzinfo=utc) # localzing to UTC
                now = datetime.now(utc)
                weekAgo = now - timedelta(weeks=1)

                if not weekAgo <= postTime <= now: # only want news from current week
                    weekAgoReached = True
                    break

                pl_news['date'].append(postTime.date())

            linkTag = articleComponent.find('a', href=True)
            if linkTag:
                article = newspaper.article(linkTag['href'])
                title = article.title.replace('"', '')
                pl_news['title'].append(title)
                bodyLines = article.text.splitlines() # removing unnecassary lines from article body
                for i, line in enumerate(bodyLines):
                    if line.isupper():
                        for j in range(4): bodyLines.pop(i+j)
                        break
                pl_news['body'].append(''.join(bodyLines))

            pl_news['team'].append(team)
            pl_news['summary'].append('null')

        if page == 5: break # dont want to go more than 5 pages, just to avoid a infinte loop in the worst case
        page+=1 # if week ago article not found, we'll be continuing on to the next page

news_df = pd.DataFrame(pl_news)
news_df.to_csv('pl_news.csv')