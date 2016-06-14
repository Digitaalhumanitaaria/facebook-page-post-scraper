# facebook-page-post-scraper

**UPDATE June 2016**: Forked the script from minimaxir, the python scraper now counts each type of reaction separately. It now accesses each post by their id and gets the results from there. 14.06.2016 @peeter-t2

**UPDATE April 2016**: This script now supports v2.6 of the Graph API; as a result, `reactions` are used instead of `likes`, as that endpoint is more accurate.

Data scraper for Facebook Pages, and also code accompanying the blog post [How to Scrape Data From Facebook Page Posts for Statistical Analysis](http://minimaxir.com/2015/07/facebook-scraper/).

The actual data scraper is implemented in `get_fb_posts_fb_pages.py`; fill in the App ID and App Secret of a Facebook app you control (I strongly recommend creating an app just for this purpose) and the Page ID of the Facebook Page you want to scrape at the beginning of the file.

The CSVs for NYTimes and BuzzFeed data are not included in this repository due to size; you can download the [NYTimes data here](https://dl.dropboxusercontent.com/u/2017402/nytimes_facebook_statuses.zip) [4.6MB] and the [BuzzFeed data here](https://dl.dropboxusercontent.com/u/2017402/buzzfeed_facebook_statuses.zip) [1.5MB]
