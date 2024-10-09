# this project can be done in 2 methods 1st is by using lexion method and the other one is machine learning method
# I am using lexicon method
from googleapiclient.discovery import build
# to get comments from YouTube we are sing this module, googleapiclient. discovery module is used for interacting with google cloud services, and build function helps us to interact with particular service api.
import re
#re is function from regular expressions which is used for searching patterns in given text , replacing a part of strings, extracting information from text , in this project we used this function to filter certain comments from all comments
import emoji
# this module used for finding emojis, in this project we used this module for converting emojis into text , in reality vice versa can also be done.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# this module is used for giving the emotional tone of the text provided Vader( Valence Aware Dictionary and sentiment Analyzer), which is mostly used for any social media sentiment analysis
#SentimentIntensityAnalyzer is a class in module Vadersentiment.vaderSentiment which provides us a sentiment score like positive, negative, neutral or mixed for the text provided
import matplotlib.pyplot as plt
# this module is used to show provided score in the project as a graph , in matplotlib there are many kinds of plots like bar, pie, scatter and histogram

#till now we imported the modules required for the project
# fetching comments
# for my project I am taking a YouTube video from a telugu channel named Raw Talks

# storing my api key
api_key = 'AIzaSyCrnhQC0AKjNJE95OhgASdUpfJE-mxULPc'
# for the interaction between Api and my code I am creating a service object with name youtube_service_object
# when we want to create a service object we will use google api client module and build function
# syntax for build function is build('api_name', 'version', developerKey = 'our api key')
youtube_service_object = build('youtube', 'v3', developerKey=api_key)
# I am taking YouTube url from console and slicing it because YouTube Api requires only the last 11 digits of url which is called video id
input_url = input("enter your You Tube Url to be taken:")[17:28]
# after extracting the video id , I am printing it
print(f"video id: {input_url}")
# I will send an Api request to google cloud console to give me the details of the video like title, description, channel id , thumbnails, posted date etc
#.videos() is used because we want details of video, and we want to store details in a list so .list() is used
#part is a parameter which is tells us which part of video is required and snippet gives the basic details of video
# id takes the youtube video's id and execute is a method which sends api request and gives the response
video_api_response = youtube_service_object.videos().list(part = 'snippet', id=input_url).execute()
#video_snippet is a dictionary that collects the details of video, video_api_response is the upper one which connects with api
# ['items'] is the key in dictionary video_snippet, snippet is nothing but the data of video which is obtained from the api request
video_snippet = video_api_response['items'][0]['snippet']

title = video_snippet['title']
description = video_snippet['description']
channel_title = video_snippet['channelTitle']
publish_date = video_snippet['publishedAt']
thumbnails = video_snippet['thumbnails']
uploader_channel_id = video_snippet['channelId']

print(f"Title: {title}")
print(f"Description: {description}")
print(f"Channel Title: {channel_title}")
print(f"Published Date: {publish_date}")
print(f"Thumbnails: {thumbnails}")
print(f"Uploader Channel ID: {uploader_channel_id}")

#till now we have just fetched details of video , now I am going to fetch the comments from the video and storing it in a list
#list helps in storing the comments in order and also helps in adding new comments easily rather than other data types
# generally youtube api just allows us to collect only 100 comments , but in this project to get good results I am collecting all the comments from the video

print("Fetching comments......")# it is used to just print fetching comments to look nice in console
comments = [] # created an empty list to store comments
#nextPageToken is given by youtube Api, when we ask youtube api for large data like comments
#youtube api stores youtube comments in a page, each page can store upto 100 comments, is user wants to take more than them then api gives a nextPageToken request to user
#that means the user can get next page comments using nextPageToken , the api sends this till it comes to end of the pages
# we have taken None, because we are at starting page
nextPageToken = None
# now I want to collect all the comments , so i need to start an infinite loop
# if we want limited number of commenst we can use, while len(comments) =/>/< number

while True:
    # to create a request to youtube api to retrieve comments we use this line
    #youtube_service_object is the one which we created a coonection between api and us, using build function
    #commentThreads(). allows us to fetch and reterieve comments from youtube  api and we are storing the respone from api in a list()
    #part is a parameter which is tells us which part of video is required and snippet gives the basic details of video
    #the videoId is the parameter which tells us which video details we want by taking the url which is given by the user intially
    # after get the videoid , the max comments per page should be 100 that is written as maxResults = 100 ,where maxResults is a parameter
    # so for the next page of comments we are intiating pageToken = nextPageToken
    #part,videoId,maxResults,pageToken these fixed names given by yotube api
    comment_request = youtube_service_object.commentThreads().list(part='snippet', videoId=input_url,maxResults =100, pageToken = nextPageToken)
    comment_response = comment_request.execute()
    # so to get all comments from comment_response  we are iterating it using for loop
    # so the response given by youtube api is by default a dictionary  and "items" is the key value which is fixed and given by youtube api
    for i in comment_response['items']:
        #now i am fetching details of top comment received for the video among all the comments
        #i['snippet'] gives just general information about the comments
        # ['toplevelcomment']['snippet'] gives the information about the top level comment like text and author information
        top_level_comment_details=i['snippet']['topLevelComment']['snippet']
        comment_text = top_level_comment_details['textDisplay']
        # As i am analysing comments which are not made by uploader, I am going to check if the comment is from uploader or not
        #['authorchannelid'] is a dictionary which is present in the youtube api and this stores another dictionary in it
        #['value'] this gives key for the dictionary which is present in the authorchannelid
        if top_level_comment_details['authorChannelId']['value'] != uploader_channel_id:
            #now i going to store the comments which are not made by uploader in comments list
            #textdisplay is tha actual comments text which is obtained from youtube api
            comments.append(comment_text)
    # similarly I have to get all the comments , as i can only collect 100 comments per page , I have to get next page token from youtubeapi
    nextPageToken = comment_response.get('nextPageToken')
    #if there are no more comments youtube api won't provoke nextpage token, so the loop should end
    if not nextPageToken:
        break
# for sample I would like to print starting 5 comments
print(comments[:5])

# till now I have connected my code to youtube api and fetched comments, now I am going to clean and filter the comments which are fetched
# So now first i like clean the comments and filter them out
#from the comments I would like to remove url's, special characters, excessive spaces from the comments to reduce noise
# re.sub('matched pattern','replace','varaiable')-> this is taken from regular expression module
# sub is function called substitute
# preprocess_comment is a user defined function, and comment is the parameter of the function where single comment is taken
#inside sub(r'')-> after r the pattern starts
def preprocess_comment(comment):
    comment = re.sub(r'^\w\s','', comment) # here ^ means not, \w means word, \s white space, i.e, anything other than word and white space should be removed
    comment = re.sub(r'http\S+', '', comment) # here http means which starts with http \S+ means non-whitespace characters i.e., anything that starts with http should be removed
    comment = re.sub(r'\s+', '',comment)# here \s+ any white spaces should be removed
    return comment.strip().lower() # this removes any spaces , tabs , newlines and converts everything into lower case and stores in comment

# so cleaning our comments is done now we need to filter them out
# for filtering the comments first I want removes comments which have more emojis rather than text as they are not suitable for analysis
# to filter emojis, I am using threshold ratio
#threshold ratio is calculated as total no.of text/(total no.of text + total no.of emojis)
threshold_ratio = 0.65 #i.e., there should 65% text in the comment to be approved
relevent_comments = []# the comments which are approved will be stored in this list
for j in comments:
    j = preprocess_comment(j)
    No_of_emojis = emoji.emoji_count(j)# from emoji module emoji_count, counts the no of emojis in the comment
    No_of_text_characters = len(re.sub(r'/s', ' ',j))
    if any(char.isalnum() for char in j):# checks if the comment is alphanumeric, if yes it goes to next step
        if No_of_emojis == 0 or (No_of_text_characters / (No_of_text_characters + No_of_emojis)) > threshold_ratio:
            relevent_comments.append(j)

print(relevent_comments[:5])

# till now we have reterived comments and cleaned it, now I am going to store those in a text file for analysis
# I have a created a text file in this folder where I would store these comments
f = open("youtubecomments.txt",'w',encoding='utf-8')
#This line opens or creates a file named youtubecomments.txt in write mode ('w').
#The 'w' mode means that if the file exists, it will be overwritten; if it doesn't exist, a new file will be created.
#encoding='utf-8' ensures that the file can handle special characters or non-ASCII characters properly, like those in non-English languages.
for idx, comment in enumerate(relevent_comments):
    #This loop iterates over each comment in the list relevent_comments.
    #enumerate(relevent_comments) gives both the index (idx) and the actual comment (comment) for each item in the list. In this case, the index idx is not used inside the loop, but it's helpful if you want to number or track each comment.
    f.write(str(comment) + "\n")
    #Writes each comment to the file.
    #str(comment) converts the comment to a string, in case it's not already one (e.g., if it’s an integer or other data type).
    #The "\n" adds a newline character after each comment, so every comment will be written on a new line in the file.
f.close()
#Closes the file after all the comments have been written.Closing the file is important because it ensures that all data is flushed from the buffer to the file, preventing data loss.
print("Comments stored successfully!")

# so now I have successfully stored comment in text file, now i am going to analyze comments using sentiment analysis
# sentiment_analysis is a function which take 2 parameters, comment stores string of comment and polarity is a list which stores polarity score of the comment
def sentiment_analysis(comment, polarity):
    sentiment_analyzer = SentimentIntensityAnalyzer()#from vadersentiment module i imported sentimentintenstiyanalyzer class to calculate sentiment score of a comment and it is then stored in sentiment analyzer
    sentiment_score = sentiment_analyzer.polarity_scores(comment)
    # polarity_scores is a built-in method which is provided by sentimentintensityanlyzer class which is used to analyze the comment and give score
    # polarity_scores returns a dictonary with 4 sentiment scores, neg, pos, neu, compound and the score is stored in sentiment_score as a dict
    # compound key in the dictionary stores the overall sentiment score of the comment
    polarity.append(sentiment_score['compound'])
    # polarity is an empty list which we have created in sentiment_analysis function
    # from sentiment_score dictionary i am going to take the values for compound key and is stored in polarity list using append
    return polarity
polarity=[]
positive_comments=[]
negative_comments=[]
neutral_comments=[]
# the above 4 are the empty lists in which sentiment score and positive, negative, neutral comment are stored.
# now i am going to get comments stored in the youtubecomments.txt  text file
f = open("youtubecomments.txt",'r',encoding='utf-8')
# the above line opens the text file in reading mode , utf-8 ensures that any kind of special characters in comments can be read correctly
comment_list = f.readlines()# it reads comments from file and stored as a list, each item in list is each comment
f.close()
# now analyzing of comments starts
print("Analyzing Comments...")
for index, item in enumerate(comment_list): # loop over comments in the comment_list
    # index is the positon of comment like 0 for 1st comments, 1 for 2nd comment
    # item is the comment from comment_list
    # enumerate is a built-in python function which basically gives index for the text
    polarity = sentiment_analysis(item, polarity)
    #polarity[-1] is nothing but from polarity list , it checks recent polarity score of the latest comment
    if polarity[-1]>0.05:
        positive_comments.append(item)
    elif polarity[-1]<-0.05:
        negative_comments.append(item)
    else:
        neutral_comments.append(item)
print(polarity[:5])

# so above I have got all the polarity scores for the comments, but to know the whole video is positive one or negative one,
# I have to get a average polarity of the video
#  to get the average polarity, we have to add sum of all polarity of comments divided by no.of polarity scores(i.e., number of comments)
# if average polarity is >0.05 the response for the video is positive
# if it's <-0.05 the response if negative
# if it is in between 0.05 to -0.05 then the video is neutral

average_polarity = sum(polarity)/len(polarity)
print("average polarity of video = ",average_polarity)
if average_polarity > 0.05:
    print("The video got positive feedback")
elif average_polarity <-0.05:
    print("The video got negative feedback")
else:
    print("The video got neutral feedback")

# I am also going to find the highest positve and negative comments for the video

max_polarity_index = polarity.index(max(polarity)) # gives the index of maximum polarity comment
most_positive_comment = comment_list[max_polarity_index] # retrieves most positive comment
max_score = max(polarity)# retrieves the most positive comments score
comment_length=len(most_positive_comment)# retrieves the most positive comments length
print("The comment with most positive feedback is, ",most_positive_comment)
print("the score of the most positive comment:",max_score)
print("the length of the most positive comment:", comment_length)

# now I am going to find the highest negative comment for the video

min_polarity_index = polarity.index(min(polarity))
most_negative_comment = comment_list[min_polarity_index]
min_score = min(polarity)
comment_length_negative = len(most_negative_comment)
print("The comment with most negative feedback is,", most_negative_comment)
print("The score of the most negative comment:", min_score)
print("The length of the most negative comment:", comment_length_negative)


# now I am going to show the no.of comments which have positive, negative and neutral feedback visually by using matplotlib

#1st I will find the no.of positive, negative, neutral comments
positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

# for the bar chart I would like to have labels for them, so I will give label names as a list of strings in label
label =['postive', 'negative', 'neutral']
# now I will take the count os comments as a list and store in comments_count
comments_count=[positive_count,negative_count,neutral_count]

# now I will assign a bar graph with green for positive, red for negative and yellow for neutral
plt.bar(label,comments_count, color=['green','red','yellow'])
# now i am adding names for x-axis as sentimentanalysis and y-axis as comment count and title for the graph as raw talks video feedback
plt.xlabel("sentiment analysis")
plt.ylabel("comment count")
plt.title("Raw Talks Youtube video feedback")
# to display the graph we will use show
plt.show()

# I have taken
#https://youtu.be/md6MWbeLt3c?si=Mi3CvMBpSthgaU1M
#this video.
