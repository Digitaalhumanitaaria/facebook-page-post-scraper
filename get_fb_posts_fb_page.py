#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Outputting as utf-8 not yet included, but not difficult to add if needed.

# Forked from https://github.com/minimaxir/facebook-page-post-scraper, originally by Max Woolf (minimaxir), https://github.com/minimaxir
# Updated by Peeter Tinits 14.06.2016 to read reactions separately based on http://stackoverflow.com/questions/36930414/how-can-i-get-facebook-graph-api-reaction-summary-count-separately recommendations.
# Runs with Py 2.7.10

import urllib2
import json
import datetime
import csv
import time

#Get your app id and key here on facebook. Help here: https://goldplugins.com/documentation/wp-social-pro-documentation/how-to-get-an-app-id-and-secret-key-from-facebook/
app_id = "YOUR NUMERIC APP ID, see above"
app_secret = "Your app secret key, see above" # DO NOT SHARE WITH ANYONE!
page_id = "postimees" # name of the facebook page, probably works with numbers too.

access_token = app_id + "|" + app_secret

limited = True # limits the number of posts processed. Change to False if you want the whole page.
limit = 200 # The number of pages to be processed if limited is True. Uses multiples of 100 to scrape for bandwith reasons.

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()


# Needed to write tricky unicode correctly to csv; not present in tutorial
def unicode_normalize(text):
	return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22, 0xa0:0x20 }).encode('utf-8')

def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.6/"
    node = "/" + page_id + "/posts" 
    parameters = "/?fields=message,link,created_time,type,name,id,comments.limit(1).summary(true),shares,reactions.limit(1).summary(true)&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data
def getFacebookPostData(page_id, access_token):
    num_statuses = 1
    # construct the URL string
    base = "https://graph.facebook.com/v2.6/"
    node = page_id 
    #parameters = "/?fields=reactions.summary(true),reactions.type(LIKE).limit(0).summary(true).as(like),reactions.type(LOVE).limit(0).summary(true).as(love),reactions.type(WOW).limit(0).summary(true).as(wow),reactions.type(HAHA).limit(0).summary(true).as(haha),reactions.type(SAD).limit(0).summary(true).as(sad),reactions.type(ANGRY).limit(0).summary(true).as(angry),reactions.type(THANKFUL).limit(0).summary(true).as(thankful)&limit=%s&access_token=%s" % (num_statuses, access_token) # changed

    #Potentially quicker, but maybe no difference:
    parameters = "/?fields=reactions.summary(total_count),reactions.type(LIKE).limit(0).summary(total_count).as(like),reactions.type(LOVE).limit(0).summary(total_count).as(love),reactions.type(WOW).limit(0).summary(total_count).as(wow),reactions.type(HAHA).limit(0).summary(total_count).as(haha),reactions.type(SAD).limit(0).summary(total_count).as(sad),reactions.type(ANGRY).limit(0).summary(total_count).as(angry),reactions.type(THANKFUL).limit(0).summary(total_count).as(thankful)&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    #print(data) - for debugging
    return data
    
   

def processFacebookPageFeedStatus(status):
    
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.
    
    # Additionally, some items may not always exist,
    # so must check for existence first
    #print(status['id'])
    status_id = status['id']

    # To access data on particular reactions, accessing by post was easier than accessing by page.
    # data is returned with each reaction data point.
    # This slows down the script a bit and probably better ways are out there.
    data = getFacebookPostData(status_id,access_token)

    
    status_message = '' if 'message' not in status.keys() else unicode_normalize(status['message'])
    link_name = '' if 'name' not in status.keys() else unicode_normalize(status['name'])
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else unicode_normalize(status['link'])
    
    
    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.
    
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
    
    # Nested items require chaining dictionary keys.
    
    #num_reactions1 = 0 if 'reactions' not in status.keys() else status['reactions']['type']['like']#.limit(0).summary(true).as(like)
    num_reactions = 0 if 'reactions' not in status.keys() else status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
    num_likes = 0 if 'like' not in data.keys() else data['like']['summary']['total_count']
    num_loves = 0 if 'love' not in data.keys() else data['love']['summary']['total_count']
    num_wows = 0 if 'wow' not in data.keys() else data['wow']['summary']['total_count']
    num_hahas = 0 if 'haha' not in data.keys() else data['haha']['summary']['total_count']
    num_sads = 0 if 'sad' not in data.keys() else data['sad']['summary']['total_count']
    num_angries = 0 if 'angry' not in data.keys() else data['angry']['summary']['total_count']
    num_thankfuls = 0 if 'thankful' not in data.keys() else data['thankful']['summary']['total_count']
    # return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
           status_published, num_reactions, num_comments, num_shares, num_likes,
            num_loves, num_wows, num_hahas, num_sads, num_angries, num_thankfuls)

def scrapeFacebookPageFeedStatus(page_id, access_token):
    with open('%s_facebook_statuses.csv' % page_id, 'wb') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", "status_type", "status_link",
           "status_published", "num_reactions", "num_comments", "num_shares", "num_likes",
                    "num_loves","num_wows","num_hahas","num_sads","num_angries","num_thankfuls"])
        
        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        
        print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)
        
        statuses = getFacebookPageFeedData(page_id, access_token, 100)
        #print(statuses)
        
        while has_next_page:
            for status in statuses['data']:
                w.writerow(processFacebookPageFeedStatus(status))
                
                # output progress occasionally to make sure code is not stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print "%s Statuses Processed: %s" % (num_processed, datetime.datetime.now())
                if limited == True and num_processed >= limit:
                    has_next_page = False
                    
            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(statuses['paging']['next']))
            else:
                has_next_page = False
                
        
        print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)


if __name__ == '__main__':
	scrapeFacebookPageFeedStatus(page_id, access_token)


# The CSV can be opened in all major statistical programs. Have fun! :)
