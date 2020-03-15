![img](https://i.imgur.com/fApFGmM.png)

# TwittyJar - Twitter Advanced Search Export Tool

Export Tweets by using a Twitter Advanced Search similar UI, written in Python. This project was inspired by Jefferson Henrique's Python script at https://github.com/Jefferson-Henrique/GetOldTweets-python for getting old tweets without using the Twitter's API.

This tool offers a nice User Interface for passing search criteria and export options before executing a Twitter Search. It offers all the options that Twitter's Advanced Search tool (https://twitter.com/search-advanced?lang=eng) offers, but it can also export all results in a CSV file which can be easily converted to an Excel spreadsheet. It is capable of producing results up to 2+ years old. It is a great tool for marketeers, data analysts, CEO's and anyone else looking to get Twitter data exported in a single file.

<h3>:: Availability</h3>
<ul>
  <li>Run directly as a Python3 script (main.py). Requirements: certifi==2018.11.29, pyquery==1.4.0, urllib3==1.25.7, PyQt5==5.13.2</li>
   <li>Run on Mac OS by downloading the <a href="https://github.com/yiannakasgeorge/pythonGUI-twitter-advanced-search/raw/master/dist/twitterSearchMac.app.zip">TwitterSearchMac.app</a> located in the 'Dist' folder of this repo. No need for libraries. Just open the archive and run the APP!</li>
   <li>Run on Windows by downloading the <a href="https://github.com/yiannakasgeorge/pythonGUI-twitter-advanced-search/raw/master/dist/twitterSearchWin.exe.zip">TwitterSearchWin.exe</a> located in the 'Dist' folder of this repo. No need for libraries. Just open the archive and run the EXE file!</li>
  <p>*The CSV exports will be stored on your desktop</p>
</ul>

<h3>:: Demo</h3>

[![Watch the video here](https://j.gifs.com/mOk3PO.gif)](https://www.youtube.com/watch?v=lWIdSR3aVD8)

<a href="https://www.youtube.com/watch?v=lWIdSR3aVD8">https://www.youtube.com/watch?v=lWIdSR3aVD8</a>

<h3>How to convert the exported CSV to an Excel spreadsheet</h3>

*Instructions: https://www.youtube.com/watch?v=4a3I5oLj3JU 

*The above method truncates the text following a comma (,).
Instead of opening the CSV directly into Excel try the following:
<ul>
<li>Open a blank workbook in Excel.</li>
<li>Navigate to the "Data" tab</li>
<li>Select the "From Text" Option</li>
<li>Select the CSV file exported</li>
<li>Keep the default options in step 1 (Delimited, Start import at row 1, Unicode (UTF-8) as file origin</li>
<li>Make sure to select "Tab" in the Delimiters column in step 2</li>
<li>Select "General" in Column data form in step 3</li>
<li>Select the existing sheet when prompted to select "Where do you want to put the data"</li>
</ul>

That's it. You will notice that tweets with comma (,) are no longer being truncated.

*Using the method above, will incorrectly convert the "Poster username" context to formulas.

Select the "Poster username" column and its contents and click "Text to columns" option from the "Data" tab. Choose 'delimited' in step 1, "Tab" in step 2 and "Text" in step 3 to convert them to text. Then just clear the "=" sign from the context.

**For the "Tweet id" column , just form the cells to "Number" with zero decimal places.

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
