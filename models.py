import random
import re
import searchController
validProxiesList = []

class FormSeachCriteria:

   def __init__(self):
         pass

   def setAllOfTheseWords(self, allOfTheseWords):
      self.allOfTheseWords = self.getInputVal(allOfTheseWords)
      return self

   def setThisExactPhrase(self, thisExactPhrase):
      self.thisExactPhrase = self.getInputVal(thisExactPhrase)
      return self

   def setAnyOfTheseWords(self, anyOfTheseWords):
      self.anyOfTheseWords = self.getInputVal(anyOfTheseWords)
      return self

   def setNoneOfTheseWords(self, noneOfTheseWords):
      self.noneOfTheseWords = self.getInputVal(noneOfTheseWords)
      return self

   def setTheseHashtags(self, theseHashTags):
      self.theseHashTags = self.getInputVal(theseHashTags)
      return self

   def setLanguage(self, language):
      self.language = self.getInputVal(language)
      return self

   def setFromTheseAccounts(self, fromTheseAccounts):
      self.fromTheseAccounts = self.getInputVal(fromTheseAccounts)
      return self

   def setToTheseAccounts(self, toTheseAccounts):
      self.toTheseAccounts = self.getInputVal(toTheseAccounts)
      return self

   def setMentioningTheseAccounts(self, mentioningTheseAccounts):
      self.mentioningTheseAccounts = self.getInputVal(mentioningTheseAccounts)
      return self

   def setNearThisPlace(self, nearThisPlace):
      self.nearThisPlace = self.getInputVal(nearThisPlace)
      return self

   def setFromThisDate(self, fromThisDate):
      self.fromThisDate = self.getInputVal(fromThisDate)
      return self

   def setToThisDate(self, toThisDate):
      self.toThisDate = self.getInputVal(toThisDate)
      return self

   def isValidForm(self):
    
      if (self.allOfTheseWords or self.thisExactPhrase or self.anyOfTheseWords or self.noneOfTheseWords or self.theseHashTags or self.fromTheseAccounts or self.toTheseAccounts or self.mentioningTheseAccounts or self.nearThisPlace) and (self.fromThisDate) and (self.toThisDate):
         return True

      return False

   def getInputVal(self, input):
      if(input and len(input) > 1):
            return input
      return False


class FormExportOptions:

   def __init__(self):
         pass
   
   @staticmethod
   def getMappingsBetweenExportFieldsAndColumnNames():
      
      fieldsMPColumns = {
         'dateTime': 'Tweet post Date',
         'id': 'Tweet id',
         'permalink': 'Tweet Permalink',
         'posterUsername': 'Poster username',
         'posterProfileName': 'Poster profile name',
         'posterNumberOfFollowers': 'Poster followers count',
         'text': 'Tweet text',
         'numberOfRetweets': 'Number of retweets',
         'isARetweetStatus': 'Tweet type',
      }
      return fieldsMPColumns


   def setExportFilename(self, filename):
      if(re.match(r'^.*\.csv$', filename)):
         self.filename = filename
         return self
      
      self.filename = "results.csv"
      return self

   def setExportPermalink(self, getPermalink):
      self.permalink = getPermalink
      return self

   def setExportTweetID(self, getTweetId):
      self.id = getTweetId
      return self

   def setExportPosterUsername(self, getPosterUsername):
      self.posterUsername = getPosterUsername
      return self

   def setExportTweetDate(self, getTweetDate):
      self.dateTime = getTweetDate
      return self

   def setExportPosterProfileName(self, getPosterProfileName):
      self.posterProfileName = getPosterProfileName
      return self

   def setExportTweetText(self, getTweetText):
      self.text = getTweetText
      return self

   def setExportNumOfRetweets(self, getNumOfRetweets):
      self.numberOfRetweets = getNumOfRetweets
      return self

   def setExportRetweetStatus(self, getRetweetStatus):
      self.isARetweetStatus = getRetweetStatus
      return self

   def setExportFollowersCount(self, getFollowersCount):
      self.posterNumberOfFollowers = getFollowersCount
      return self


class FormProxyOptions: 

   def __init__(self):
         pass

   def setUseProxy(self, useProxy):
      self.useProxy = useProxy
      return self

   def setProxyURL(self, proxyURL):
      self.proxyURL = proxyURL
      return self

   def isValidProxyOptions(self):
      if (self.useProxy and self.proxyURL and self.checkProxyURL(self.proxyURL)):
         
         global validProxiesList
         if(validProxiesList.index(self.proxyURL) > -1):
            return True

         randomUserAgent = UserAgents.getRandomUserAgent()
         req = searchController.SearchController.urlRequest('https://www.twitter.com', self.proxyURL, '', randomUserAgent)
         if(req):
            validProxiesList.append(self.proxyURL)
            return True

      if(self.useProxy == False):
         return True

      return False

   @staticmethod
   def checkProxyURL(url):
      if(re.match(r'^(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::\d+)?|(?![.\d:]+$)(?:https?://)?\w+(?:\.\w+)*(?::\d+)?(?:[/?].*)?|\w+:\w+@(?:https?://)?\w+(?:\.\w+)+:\d+)$', url)):
         return True

      return False


class FormOptions:  

   def __init__(self):
         pass

   def setFormSearchCriteria(self, formSearchCriteria):
      self.formSearchCriteria = formSearchCriteria
      return self

   def setFormExportOptions(self, formExportOptions):
      self.formExportOptions = formExportOptions
      return self
   
   def setFormProxyOptions(self, formProxyOptions):
      self.formProxyOptions = formProxyOptions
      return self
  

    
  
class Languages:

    def __init__(self):
         pass
    
    @staticmethod
    def getLanguageValue(index):
        lang = ['any','ar','bn','eu','bg','ca','hr','cs','da','nl','en','fi','fr','de','el','gu','he','hi','hu','id','it','ja','kn','ko','mr','no','fa','pl','pt','ro','ru','sr','zh-cn','sk','es','sv','ta','th','zh-tw','tr','uk','ur','vi']
        return lang[index]

class UserAgents:

    def __init__(self):
         pass

    @staticmethod
    def getRandomUserAgent():
       user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/71.0',
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/71.0',
       'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/71.0',
       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edg/44.18362.449.0']

       return random.choice(user_agent_list)

class Tweet:

    def __init__(self):
        pass
    
    def setId(self, id):
       self.id = id
       return self

    def setPermalink(self, permalink):
       self.permalink = permalink
       return self

    def setPosterUsername(self, posterUsername):
       self.posterUsername = posterUsername
       return self

    def setDateTime(self, dateTime):
       self.dateTime = dateTime
       return self

    def setPosterProfileName(self, posterProfileName):
       self.posterProfileName = posterProfileName
       return self

    def setText(self, text):
       self.text = text
       return self

    def setNumberOfRetweets(self, numberOfRetweets):
       self.numberOfRetweets = numberOfRetweets
       return self

    def setIsARetweetStatus(self, isARetweetStatus):
       self.isARetweetStatus = isARetweetStatus
       return self

    def setPosterNumberOfFollowers(self, posterNumberOfFollowers):
       self.posterNumberOfFollowers = posterNumberOfFollowers
       return self
