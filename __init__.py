import os, json
from selenium import webdriver

# Getting the path of the script file
dirname = os.path.dirname(__file__)

# Load configurations from config file
config = {}
with open(f"{dirname}/scrapper_config.json", 'r') as config_file:
    config = json.load(config_file)

# Path to the web Driver file:
PATH = f"{dirname}/{config['driver'][config['browser']]}{['', '.exe'][config['Windows']]}"

# Defining a Function to initialize the drivers
def get_driver():
    if config['browser'] == "Chrome":
        # Configuring Chrome Driver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        if config['headless']:
            # Headless Configuration
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        # Return chrome driver invocation
        return webdriver.Chrome(executable_path=PATH, options=chrome_options)

    elif config['browser'] == "Firefox":
        # Cofiguring Firefox Driver
        from selenium.webdriver.firefox.options import Options
        firefox_options = Options()
        if config['headless']:
            # Headless Configuration
            firefox_options.headless = True
        # Return firefox driver invocation
        return webdriver.Firefox(executable_path=PATH, options=firefox_options)

    elif config['browser'] == "Edge":
        # Configuring the Edge Driver
        from msedge.selenium_tools import EdgeOptions
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        if config['headless']:
            # Headless Configuration
            edge_options.add_argument('--headless')
            edge_options.add_argument('--disable-gpu')
        # Return firefox driver invocation
        return webdriver.Edge(executable_path=PATH, options=edge_options)