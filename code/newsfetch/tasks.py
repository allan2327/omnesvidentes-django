from __future__ import absolute_import
from celery import shared_task
from nltk import word_tokenize,WordNetLemmatizer,NaiveBayesClassifier,classify,MaxentClassifier,DecisionTreeClassifier
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from decimal import Decimal
import re, hashlib, datetime, parsedatetime, random
from datetime import timedelta, time
import newsfetch
from . import secrets
import gnp.gnp as gnp
from slacker import Slacker

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
    categories = newsfetch.models.Category.objects.all()
    print("Running News Rating Model: ")
    for category in categories:
        topics = newsfetch.models.Topic.objects.filter(category = category)
        stories = newsfetch.models.NewsItem.objects.filter(rating__gte = 0, topic__in = topics)
        if not stories:
            print('- Not enough training data for '+category.category_name)
            stories = newsfetch.models.NewsItem.objects.filter(topic = topic)
            for story in stories:
                story.modelrating = Decimal(-1.0)
                story.save()
        else:
            print('- Training Classifier for '+category.category_name+' ('+category.fetcher.fetcher_name + ')')
            storydata = []
            for story in stories:
                storydata.append([story.title + story.content_snippet, story.rating])

            random.shuffle(storydata)
            featuresets = [text_features(n[0]) for n in storydata]
            featuresets_y = [n[1] for n in storydata]

            vec = DictVectorizer()
            featuresets_vectorized = vec.fit_transform(featuresets)

            #size = int(len(featuresets) * 0.35)
            #train_set, test_set = featuresets[size:], featuresets[:size]
            #classifier = NaiveBayesClassifier.train(train_set)
            #classifier = DecisionTreeClassifier.train(featuresets)
            clf = RandomForestRegressor(n_estimators=10)
            clf = clf.fit(featuresets_vectorized,featuresets_y)
            print("  * score: "+str(clf.score(featuresets_vectorized,featuresets_y)))

            #print('accuracy: '+ str(classify.accuracy(classifier,test_set)))
            #classifier.show_most_informative_features(30)
            #print('labels:'+str(classifier.labels()))

            # Predict for all items!
            topics = newsfetch.models.Topic.objects.filter(category = category)
            stories = newsfetch.models.NewsItem.objects.filter(topic__in = topics)
            print("  * predicting score for all items.")

            for story in stories:
                featset = text_features(story.title + story.content_snippet)
                featset_vectorized = vec.transform(featset)
                story.modelrating = Decimal(clf.predict(featset_vectorized)[0])
                story.save()

    return(True)

@shared_task()
def displayNews(category):
    slack = Slacker(newsfetch.secrets.SLACK_TOKEN)

    categories = newsfetch.models.Category.objects.filter(category_name = category)
    topics = newsfetch.models.Topic.objects.filter(category__in = categories)
    # TODO: Filter by Date, limit to a smaller dataset...
    stories = newsfetch.models.NewsItem.objects.filter(topic__in = topics, modelrating__gte = 3.5,date__gte = datetime.datetime.now().date()-timedelta(1), date__lte=datetime.datetime.now().date(), posted=False).order_by('-modelrating')[:5]
    for story in stories:
        #print(story.title)
        slack.chat.post_message(channel = '#news', text = story.title + '\n<'+story.link +'>\n'+story.content_snippet,username=story.source)
        story.posted = True
        story.save()
    return(True)
