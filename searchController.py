import urllib.parse,urllib.error,json,re,datetime,sys
import certifi
import models
import urllib3
import urllib3.exceptions
http = urllib3.PoolManager()
from pyquery import PyQuery
from urllib.parse import urlsplit

class SearchController:

	def __init__(self):
		pass

	@staticmethod
	def urlRequest(url, proxyURL, cookie, userAgent):

		http = urllib3.PoolManager(
			cert_reqs='CERT_REQUIRED',
			ca_certs=certifi.where(),
			maxsize=20)

		rHeaders = {
			'Host': "{0.netloc}".format(urlsplit(url)),
			'User-Agent': userAgent,
			'Accept': "application/json, text/javascript, */*; q=0.01",
			'X-Requested-With': "XMLHttpRequest",
			'Referer': url,
			'Connection': "keep-alive"
			# 'Cookie': cookie
		}

		if proxyURL:
			_http = urllib3.ProxyManager(proxyURL)
		else:
			_http = http

		try:
			r = _http.request(
				'GET',
				url,
				headers = rHeaders,
				retries=urllib3.Retry(1, redirect=2)
			)
		

		except urllib3.exceptions.HTTPError as e:
			print('HTTP error', e)
			return
		except urllib3.exceptions.ProxyError as e:
			print('Proxy error', e)
			return
		except urllib3.exceptions.ProxySchemeUnknown as e:
			print('Proxy error', e) 
			return

		# finally:
		# 	#

		return r

	@staticmethod
	def getTweets(worker, receiveBuffer=None, bufferLength=500, proxyURL=None):
		cursorHash = ''
		results = []
		resultsAux = []
		cookie = '' 
		active = True
		formSearchCriteria = worker.formSearchCriteria
		formExportOptions = worker.formExportOptions
		formProxyOptions = worker.formProxyOptions

		url = SearchController.constructURL(formSearchCriteria)
		randomUserAgent = models.UserAgents.getRandomUserAgent()

		while active and worker.running():
			searchResults = SearchController.getTweetSearchResults(
			    url, cursorHash, cookie, proxyURL, randomUserAgent)
			
			if (searchResults == None):
				worker.sgnOutput.emit('Connection Error!')
				break

			if (searchResults and len(searchResults['items_html'].strip()) == 0):
				break

			cursorHash = searchResults['min_position']
			scrapedTweets = PyQuery(searchResults['items_html']).remove('div.withheld-tweet')
			tweets = scrapedTweets('div.js-stream-tweet')

			if len(tweets) == 0:
				break

			for tweetHTML in tweets:

				if worker.running() == False:
					break

				tweetPQ = PyQuery(tweetHTML)

				tweet = models.Tweet()
				tweetPermalink = tweetPQ.attr("data-permalink-path")

				if(formExportOptions.dateTime):
					tweet.setDateTime(datetime.datetime.fromtimestamp(int(
					tweetPQ("small.time span.js-short-timestamp").attr("data-time"))).strftime("%Y-%m-%d %H:%M:%S"))
			
				if(formExportOptions.id):
					tweet.setId(tweetPQ.attr("data-tweet-id"))

				if(formExportOptions.permalink):
					tweet.setPermalink('https://twitter.com' + tweetPermalink)

				if(formExportOptions.posterUsername):
					tweet.setPosterUsername('@' + re.split('/', tweetPermalink)[1])

				if(formExportOptions.posterProfileName or formExportOptions.posterNumberOfFollowers):
					rData = SearchController.getFollowersCountAndProfileName(tweet.posterUsername, cookie, proxyURL, randomUserAgent)
					if(formExportOptions.posterProfileName):
						tweet.setPosterProfileName(rData[1])
					if(formExportOptions.posterNumberOfFollowers):
						tweet.setPosterNumberOfFollowers(rData[0])

				# tweet.language = tweetPQ("p.js-tweet-text").attr("lang")
				tweetTextHtml = tweetPQ("p.js-tweet-text").outerHtml()
				tweetTextHtmlWithEmojis = re.sub(r"<img.*?alt=\"(.*?)\"[^\>]+>", r'\1', tweetTextHtml)
				tweetTextHtmlWithEmojis = re.sub(
					r"\s+", " ", tweetPQ(tweetTextHtmlWithEmojis).text())
				tweet.setText(tweetTextHtmlWithEmojis)

				
				if(formExportOptions.numberOfRetweets):
					tweet.setNumberOfRetweets(int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
					"data-tweet-stat-count").replace(",", "")))
			
				if(formExportOptions.isARetweetStatus):
					tweet.setIsARetweetStatus('Retweet' if len(tweetPQ("div.QuoteTweet")) > 0 else 'Tweet')

				results.append(tweet)
				resultsAux.append(tweet)

				if receiveBuffer and len(resultsAux) >= bufferLength:
					receiveBuffer(resultsAux)
					resultsAux = []
					randomUserAgent = models.UserAgents.getRandomUserAgent()
			
				if receiveBuffer and len(resultsAux) > 0:
					receiveBuffer(resultsAux)


	@staticmethod
	def constructURL(formSearchCriteria):

		url = 'https://twitter.com/i/search/timeline?f=tweets&q='

		if formSearchCriteria.allOfTheseWords:
			urlQuery1 = formSearchCriteria.allOfTheseWords
			url += urllib.parse.quote(urlQuery1)

		if formSearchCriteria.thisExactPhrase:
			urlQuery2 = formSearchCriteria.thisExactPhrase
			url += ' "' + urllib.parse.quote(urlQuery2) + '"'

		if formSearchCriteria.anyOfTheseWords:
			urlQuery3 = ' ' + formSearchCriteria.anyOfTheseWords.replace(' ', ' OR ')
			url += urllib.parse.quote(urlQuery3)

		if formSearchCriteria.noneOfTheseWords:
			urlQuery4 = ' -' + formSearchCriteria.noneOfTheseWords.replace(' ', ' -')
			url += urllib.parse.quote(urlQuery4)

		if formSearchCriteria.theseHashTags:
			urlQuery5 = ' ' + formSearchCriteria.theseHashTags.replace(' ', ' OR ')
			url += urllib.parse.quote(urlQuery5)
		
		if formSearchCriteria.fromTheseAccounts:
			urlQuery6 = 'from:' + formSearchCriteria.fromTheseAccounts.replace(' ', ' OR from:')
			url += urllib.parse.quote(urlQuery6)

		if formSearchCriteria.toTheseAccounts:
			urlQuery7 = ' to:' + formSearchCriteria.toTheseAccounts.replace(' ', ' OR to:')
			url += urllib.parse.quote(urlQuery7)

		if formSearchCriteria.mentioningTheseAccounts:
			urlQuery8 = ' ' + formSearchCriteria.mentioningTheseAccounts.replace(' ', ' OR ')
			url += urllib.parse.quote(urlQuery8)

		if formSearchCriteria.nearThisPlace:
			urlQuery9 = ' near:"' + formSearchCriteria.nearThisPlace + '" within:15mi'
			url += urllib.parse.quote(urlQuery9)

		if formSearchCriteria.fromThisDate:
			urlQuery10 = ' since:' + formSearchCriteria.fromThisDate
			url += urllib.parse.quote(urlQuery10)

		if formSearchCriteria.toThisDate:
			urlQuery11 = ' until:' + formSearchCriteria.toThisDate
			url += urllib.parse.quote(urlQuery11)

		url += '&src=typd'

		if(formSearchCriteria.language != 'any'):
			url += '&lang=&' + formSearchCriteria.language

		url = url.replace(' ','')
		
		return url
				

	@staticmethod
	def getTweetSearchResults(url, cursorHash, cookie, proxyURL, randomUserAgent):

		url += '&max_position=' + cursorHash
		
		try:
			request = SearchController.urlRequest(url, proxyURL, cookie, randomUserAgent)
			dataJson = json.loads(request.data.decode('utf-8'))
		except Exception as ex:
			print("Error while connecting to: " + url + " Error: " + str(ex))
			return
		
		return dataJson		

	@staticmethod
	def getFollowersCountAndProfileName(posterUsername, cookie, proxyURL, randomUserAgent):
			
			
			posterNumberOfFollowers = 0
			posterProfileName = ''
			# url = "https://twitter.com/" + tweet.username.replace('@', '')

			url = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=" + posterUsername.replace('@', '')
			
			try:

				request = SearchController.urlRequest(url, proxyURL, cookie, randomUserAgent)
				jsonResponse = json.loads(request.data.decode('utf-8'))
				
				if(jsonResponse and jsonResponse[0]):
					posterNumberOfFollowers = jsonResponse[0]['followers_count']
					posterProfileName = jsonResponse[0]['name']
					rData = [posterNumberOfFollowers,posterProfileName]

				# DEPRECIATED METHOD OF GETTING FOLLOWERS COUNT 
				# followers_count = re.search("followers_count&quot;:(\d+)", jsonResponse)
				# screen_name = re.search("screen_name&quot;:&quot;(\w+)", jsonResponse)
		
				# if followers_count:
				# 	tweet.user_followers_count = format(followers_count.group(0).replace('followers_count&quot;:',''))
				# else:
				# 	tweet.user_followers_count = '0'
				# if screen_name:
				# 	tweet.screen_name = format(screen_name.group(1))
				# else:
				# 	tweet.screen_name = tweet.username
			except Exception as ex:
				print("Error while connecting to: " + url + " Error: " + str(ex))
				return rData

			return rData
	
