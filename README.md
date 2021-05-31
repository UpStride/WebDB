## A python implementation of the IROS 2017 paper: [Learning Deep Visual Object Models From Noisy Web Data: How to Make it Work](https://www.researchgate.net/publication/314115657_Learning_Deep_Visual_Object_Models_From_Noisy_Web_Data_How_to_Make_it_Work)


Create image databases from the Web.
This software will expand a list of visual queries and download images from 3 search engines (google, yahoo and bing).

### Requirements

* Python 3.8 or above
* [Selenium](https://www.selenium.dev/documentation/en/selenium_installation/installing_selenium_libraries/#_python_) 3.141 or above
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/#Download) 4.9.3 or above
* [tqdm](https://pypi.org/project/tqdm/)
* Firefox
* [Firefox webdriver](https://github.com/mozilla/geckodriver/releases)

Use the `requirements.txt` at the root of the repository for installing python dependencies.

#### Setting up Firefox Webdriver

There are couple of ways to install Firefox Webdriver.

* If you are on Ubuntu based distribution `sudo apt-get install firefox-geckodriver` would install the Firefox webdriver.

or

* Extract the contents of the downloaded file.
File ending with `.zip` extension use `unzip <filename>` or file ending with `.tar.gz` extension use `tar -xvf <filename>`

Finally, add the extracted file to `$PATH`. Refer [how to add executables to PATH](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/#adding-executables-to-your-path)

### Create Expanded Query list

The query expansion works by finding the top 50 keywords that best match the initial query using [http://mykeyworder.com/keywords](http://mykeyworder.com/keywords). The result is initial query append by each keyword found.
e.g. If initial query is `dog` the query expansion output would be `dog animal`, `dog pet`. etc.

Run the bash script `expand.sh` with 1 argument file containing (the list of queries that are separated by line) from terminal

For e.g.
```bash
sh expand.sh queries.txt
```

The expanded query will be saved to the file `expanded_queries.txt` with entries comma separated.

### Download Web Images

User can download the images by running download.py using 5 arguments:
example:

```bash
python download.py \
	--search_engine all
	--queries <queries.txt or expanded_queries.txt> \
	--directories dirnames.txt \
	--num_of_images 100 \
	--run_headless
```

* `--search_engine` Specify `all` as an argument, if user wishes to run the image scraper for all the engines or provide argument as `bing` or `google` or `yahoo` for respective search engine.
* `--queries` A file containing the search queries or the expanded queries.
* `--directories`: A file containing the directory name where the downloaded images are stored
* `--num_of_images` Specify the total number of images the user wishes to scrape. Note: its not necessary the number of images will be download and scraped to be equal. There might be some scenarios the image url might not be a valid one or download might fail depending on source website's response.
* `--run_headless`: Argument that doesn't display the browser when script runs. Don't pass this argument when you don't need to visualize the script in action. This is useful for debugging purposes and browser navigation works as expected.

Note: There will be a `links.txt` file present inside each `directories` folder, which is used to check for duplicates.

where queries.txt is a text file containing list of queries and dirnames.txt is the equivalent directory name of each query line by line.


		queries.txt:	query1
				query2
				...
		dirnames.txt:	dir1
         		 	dir2
				...

Note: It's also possible to provide single entry in the dirnames.txt file, so that all the images are saved in a single folder.

In case of query expansion the queries provided on the same line separated with a comma can be downloaded into the same directory name.

	queries.txt: query1.1, query1.2, query1.3...     dirnames.txt: dir1
        	     query2.1, query2.2, query2.3...                   dir2
  		     ...                                               ...


### How to debug

All the search engines constantly try to introduce changes to their webpages in order to restrict webscraping, therefore scripts in this repository requires maintenance when they break.

We provide very basic methods for debugging the scripts.

* We try to catch and log the exceptions in the console during HTML parsing or image retrieval. Analyzing the stack trace could help identify the root cause.
* Visualizing the selenium action on the browser could help quickly identify any browser rendering issue. Remove `--run_headless` flag argument when invoking `download.py`.
* We use [css selectors](https://www.w3schools.com/cssref/css_selectors.asp) in order identify unique  selector tags in the webpage. Search engines could update these tags which might cause the script to fail.
* Ensure you are using the latest version of Firefox browser and update the `User-Agent` accordingly. Depending upon browser version and User-Agent the page might render differently which could cause the script to fail.
* If you observe slower network speed. Try increasing the script sleep time.

The script is expected to run slower with varying sleep times. This is mimic human behavior and not to flood server with constant requests.
`Warning:` Repeated requests with almost no wait time could lead to blacklisting of the user's IP.

### How to use css selector
* How to check tags are uniquely identified.
	* Open Firefox, Navigate to "www.google.com"
	* Press `F12` to open the developer tools
	* Press `Ctrl + Shift + c` to pick elements from the page
	* Hover the mouse over `Input Search` text box in google search page.
	* In the inspector tab, you should see the `<input class="gLFyf gsfi"..etc..>` selected
	* Now click `Console` tab. Type `$$("input.gLFyf.gsfi")` and hit enter. Spaces in the class name should be replace with `.`
	* You should see the output html tag displayed
* Using the above tag in selenium is very easy
	```python
	input_text_box = driver.find_element_by_css_selector("input.gLFyf.gsfi")
	```
