# Scrapy
A Simple Web Scrapping Script For Wuzzuf.com Using Selenium as part of the AI-Pro internship at ITI

## Table of Contents  
- [Requirements](#requirements)
- [Scraped Data Headers and Representations](#data)
- [Instructions](#instructions)
- [Test Environment](#test)
- [Disclaimer](#disclaimer)

## Requirements <a name="requirements"/>
- Python 3 (Preferably newer than 3.6)
- Selenium `pip install selenium`
- Compatible Browser Driver

## Scraped Data Headers and Representations <a name="data"/>

|     Header Item     | Value Type |                  Representation                 |                                         Notes                                         |
|:-------------------:|:----------:|:-----------------------------------------------:|:-------------------------------------------------------------------------------------:|
|      Job Title      |   String   | The title of the required job                   |                                                                                       |
|       Company       |   String   | The company offering the job                    | Could be `Confidential` meaning they chose not to be public                           |
|   Company Address   |   String   | The address of the company                      |                                                                                       |
|     Posting Time    |  Date/Time | The time at which the job was posted to Wuzzuf  | The time (Hour:Minutes) is not precise unless the job is posted is less than 24 hours |
|     Job Type(s)     |   String   | Full Time, Part Time, Work From Home, etc.      | One job can have multiple types separated with a pipe character '\|'                  |
|     Career Level    |   String   | Experienced, Entry Level, etc.                  |                                                                                       |
| Years of Experience |   String   | The required years of experience to apply       | Can be NULL                                                                           |
|      Industries     |   String   | The field to which the job relates              | One job can relate to multiple industries separated with a pipe character '\|'        |
|       Skill(s)      |   String   | The set of skills required to apply for the job | One job usually have multiple skills separated with a hyphen character '-'            |
|         Link        |   String   | The link to the job posting details             |                                                                                       |


## Instructions <a name="instructions"/>
1. Download and extract the app files: `Scrapy.py`, `__init__.py`, `scrapper_config.json`
2. Download the respective driver for your browser's type and version. Currently only these three are implemented:

|Browser|Driver Link|
|:------:|------|
|Chrome|https://sites.google.com/chromium.org/driver/|
|Firefox|https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/|
|Edge|https://github.com/mozilla/geckodriver/releases|

3. **Note:** If you are using Edge driver, you need to install Edge Selenium Tools as well `pip install msedge-selenium-tools`
4. Place the driver file (without changing its original name) in the same directory as the Scrapy.py file.
5. Edit the `scrapper_config.json` file as needed:

<table>
    <thead>
        <tr>
            <th>Variable</th>
            <th>Options</th>
            <th>Meaning</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3 valign="center" align="center"><code>browser</code></td>
            <td valign="center" align="center">Chrome</td>
            <td>If you are using Chrome driver</td>
        </tr>
        <tr>
            <td valign="center" align="center">Firefox</td>
            <td>If you are using Firefox driver</td>
        </tr>
        <tr>
            <td valign="center" align="center">Edge</td>
            <td>If you are using Edge driver</td>
        </tr>
        <tr>
            <td rowspan=2 valign="center" align="center"><code>headless</code></td>
            <td valign="center" align="center">0</td>
            <td>Run the browser in normal mode (Browser window will show up)</td>
        </tr>
        <tr>
            <td valign="center" align="center">1</td>
            <td>Run the browser in headless mode (Browser window won't show up)</td>
        </tr>
        <tr>
            <td valign="center" align="center"><code>datetime_format</code></td>
            <td valign="center">%d: day, %m: month, %Y: year,<br/>%H: hour, %M: minutes</td>
            <td>You can choose any combination of these elements to customize <br/>the output datetime in the scrapped data</td>
        </tr>
        <tr>
            <td rowspan=2 valign="center" align="center"><code>Windows</code></td>
            <td valign="center" align="center">0</td>
            <td>If you are using an operating system other than Windows</td>
        </tr>
        <tr>
            <td valign="center" align="center">1</td>
            <td>If you are using Windows operating system</td>
        </tr>
    </tbody>
</table>

6. Now you are ready, open the Terminal / CMD in the folder containing Scrapy and the driver files.
7. Run the following command `python3 Scrapy.py`
8. Enter the search query of the job role you want to scrape
9. Enter the number of pages you want to scrape
10. Wait for the scrapped data, a CSV file will be created in `./Wuzzuf Scraped Data/` directory

## Test Environment <a name="test"/>
Tested on **Ubuntu 20.04** using:
- Python 3.9.7
- Firefox 96.0
- Chrome 96.0.4664.110

### Further features might be added in the future...

## Disclaimer <a name="disclaimer"/>
This script is for educational purposes only and I am not responsible for misuse.
