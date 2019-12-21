# Twitter Advanced Search Export Tool

Export Tweets by using a Twitter Advanced Search similar UI, written in Python. This project was inspired by Jefferson Henrique's Python script at https://github.com/Jefferson-Henrique/GetOldTweets-python for getting old tweets without using the Twitter's API.

This tool offers a nice User Interface for passing search criteria and export options before executing a Twitter Search. It offers all the options that Twitter's Advanced Search tool (https://twitter.com/search-advanced?lang=eng) offers, but it can also export all results in a CSV file which can be easily converted to an Excel spreadsheet. It is capable of producing results up to 2+ years old. It is a great tool for marketeers, data analysts, CEO's and anyone else looking to get Twitter data exported in a single file.

<h3>:: Availability</h3>
<ul>
  <li>Run directly as a Python3 script (main.py). Requirements: certifi==2018.11.29, pyquery==1.4.0, urllib3==1.25.7, PyQt5==5.13.2</li>
   <li>Run on Mac OS by downloading the <a href="https://github.com/yiannakasgeorge/pythonGUI-twitter-advanced-search/blob/master/dist/twitterSearchMac.app.zip">TwitterSearchMac.app</a> located in the 'Dist' folder of this repo. No need for libraries. Just open the archive and run the APP!</li>
   <li>Run on Windows by downloading the <a href="https://github.com/yiannakasgeorge/pythonGUI-twitter-advanced-search/blob/master/dist/twitterSearchWin.exe.zip">TwitterSearchWin.exe</a> located in the 'Dist' folder of this repo. No need for libraries. Just open the archive and run the EXE file!</li>
  <p>*The CSV exports will be stored on your desktop</p>
</ul>

![img](https://i.imgur.com/MizSASQ.png)

<h3>:: Search Criteria</h3>

<h4>Words</h4>
<ul>
  <li>All of these words</li>
   <li>This Exact Phrase</li>
   <li>Any of these words</li>
   <li>None of these words</li>
   <li>Any of these hashtags</li>
</ul>
  
<h4>Language</h4>
  
<h4>People</h4>
<ul>
  <li>From these accounts</li>
   <li>To these accounts</li>
   <li>Mentioning these accounts</li>
</ul>
  

<h4>Places</h4>
<ul>
  <li>Near this place</li>
</ul>
  

<h4>Dates (Get tweets from any period)</h4>
<ul>
  <li>From this date</li>
   <li>To these date</li>
</ul>

<h3>:: Export options</h3>

<h4>Exported fields</h4>
<ul>
  <li>Tweet permalink</li>
   <li>Tweet id</li>
   <li>Tweet's poster (Username)</li>
   <li>Tweet's posted date/time</li>
   <li>Tweet's poster (Profile name)</li>
    <li>Tweet's text (supports emojis)</li>
   <li>Tweet's number of retweets</li>
   <li>Tweet's retweet status (Yes/No)</li>
   <li>Tweet's poster number of followers</li>
</ul>

<h4>Export to CSV</h4>
<ul>
  <li>The exported CSV file can be easily converted to an excel spreadsheet by selecting the first column and using the "Text to columns" option in Excel. Use 'tabs' as the selected option for the delimiter type and change the 'Tweet id" column format to 'Number' without any decimals.</li>
</ul>


<h3>:: Contribution</h3>
<p>Feel free to contribute to this project either by finding and resolving bugs and/or adding more features. Please make sure to follow the <a href="https://github.com/yiannakasgeorge/pythonGUI-twitter-advanced-search/blob/master/CONTRIBUTING.md">Contribution Guidelines</a>.</p>
