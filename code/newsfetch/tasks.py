from __future__ import absolute_import
from celery import shared_task
from nltk import word_tokenize,WordNetLemmatizer,NaiveBayesClassifier,classify,MaxentClassifier,DecisionTreeClassifier
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
import re, hashlib, datetime, parsedatetime, random
import newsfetch
import gnp.gnp as gnp

commonwords = stopwords.words('english')
wordlemmatizer = WordNetLemmatizer()

def getNews(q):
    news = gnp.get_google_news_query(q=q)
    stories = news['stories']
    formattedStories = []
    for story in stories:
        story['link'] = story['link'].decode('utf-8')
        story['content_snippet'] = story['content_snippet'].decode('utf-8')
        story['title'] = story['title'].decode('utf-8')
        story['source'] = story['source'].decode('utf-8')
        story['date'] = story['date'].decode('utf-8')
        formattedStories.append(story)
    return formattedStories

@shared_task()
def getAllNews():
    topics = newsfetch.models.Topic.objects.all()
    for topic in topics:
        stories = getNews(q = topic.query_text)
        for story in stories:
            cal = parsedatetime.Calendar()
            temp, status = cal.parse(re.sub('[^A-Za-z0-9 ]+', '', story['date']))
            temp = datetime.datetime(*temp[:6])
            obj = newsfetch.models.NewsItem(topic = topic,newscategory = story['category'],content_snippet = story['content_snippet'],link = story['link'],source = story['source'],title = story['title'], date = temp,rating = -1)
            obj.md5hash = hashlib.md5(obj.link.encode()).hexdigest()
            # Check if hash exists in db before saving (avoid duplicates)!
            if newsfetch.models.NewsItem.objects.filter(md5hash = obj.md5hash, topic = topic).__len__() == 0:
                obj.save()
    return True


def text_features(txt):
    features = {}
    wordtokens = [wordlemmatizer.lemmatize(word.lower()) for word in word_tokenize(txt)]
    for word in wordtokens:
        if word not in commonwords:
            features[word] =  True
    return features

@shared_task()
def buildClassifier():
    # TODO build one classifier for each topic; requires more training data though!
    stories = newsfetch.models.NewsItem.objects.filter(rating__gte = 0)
    storydata = []
    for story in stories:
        #print(story.title)
        storydata.append([story.title + story.content_snippet, story.rating])

    random.shuffle(storydata)
    featuresets = [(text_features(n),rat) for (n,rat) in storydata]

    size = int(len(featuresets) * 0.35)
    train_set, test_set = featuresets[size:], featuresets[:size]
    #classifier = NaiveBayesClassifier.train(train_set)
    #classifier = DecisionTreeClassifier.train(featuresets)
    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(featuresets)

    print('accuracy: '+ str(classify.accuracy(classifier,test_set)))
    #classifier.show_most_informative_features(30)
    #print('labels:'+str(classifier.labels()))

    # Predict for all items!
    stories = newsfetch.models.NewsItem.objects.all()
    for story in stories:
        featset = text_features(story.title + story.content_snippet)
        story.modelrating = classifier.classify(featset)
        story.save()

    return(True)
