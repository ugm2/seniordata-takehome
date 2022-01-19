# seniordata-takehome

## Intro
Thank you for applying for the Senior Data Scientist position at Opply! With the following task, we would like to see how you approach and solve problems, how well aligned we are in our understanding of the problem space and how you deal with the ambiguity that we are exposed to every day. 

## Task - Website Relevance

### Intro
We are typically interested in finding relevant suppliers for a given product request. 
A request consists, among other things, of a request name and a request description. Let’s consider the following (real) example:

**Request Name:** Organic Almonds

**Request Description:** We’re looking for almonds from an organic producer or grower

Through a preprocessing and filtering algorithm we have created a shortlist of potential suppliers.
Attached you’ll find a JSON file (suppliers.json) with website links of these potential almond producers and wholesalers. The JSON file has 347 records, where each record has the following format:
```
  {
      "supplier": "Garden Produce",
      "rootDomain": "http://www.thegardenproduce.com",
      "pages": [
          "http://www.thegardenproduce.com/2018/03/20/fresh-produce-and-so-much-more/",
          "http://www.thegardenproduce.com/",
          "http://www.thegardenproduce.com/products/vegetables/"
      ]
  }
```
A maximum number of 7 pages are included for each record/supplier. The pages are links in which a preprocessing algorithm has identified relevant keywords.

However, the file contains a lot of records that are not relevant. E.g., there may be websites of suppliers of almond chocolate or beauty products (e.g. almond-based cosmetics). 

### Task
* Please develop a code that helps to identify the most relevant websites (without manually labeling them), i.e. to identify websites that actually deal with almonds (e.g. by providing a likelihood score). The algorithm doesn’t need to be highly accurate, but it should rule out websites that are completely unrelated to almond producers or wholesalers. You can assume that eventually, a human would double-check the suggested results, but we want him/her to start with the more relevant websites.
Relevant websites are for example https://www.tropicalfoods.com, https://hattonhill.com, https://www.americannuts.com/ or https://www.clproduce.com/. Examples of irrelevant websites are http://www.domainmarket.com, https://www.livelifejuiceco.com or www.rawl.net.
* Please elaborate on how you would improve the accuracy of your approach if you had more time, resources or information available.

### Hint
You can use the code snippet given in scraper.py to extract the content of a website using the requests-package. It returns a beautifulsoup-object of the website content. 
Both text-based and image-based approaches are possible. The file scraper.py contains code snippets that extract the text and image links of the websites.

## Submission
* Please do not spend more than 4 hours on the task, just submit your progress after that time.
* Please create a zip-folder with all files (code & results) and send it to martin@opply.io within three working days or alternatively share a github link.



**Thank you!**



