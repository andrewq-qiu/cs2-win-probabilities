"""Download all CS2 demo files for a subset of maps at a list of HLTV events.

Arguments:
    --events-path: Path to a .txt file where each line contains an HLTV event ID, ignoring comments prefixed by #
    --maps-path: Path to a .txt file where each line contains a map name. Represents the subset of maps to download
    --output-path: Directory to store demos in
    --chrome-bin: Path to a chrome binary for use with selenium
"""

import logging
import time
import argparse
import os
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup
from selenium import webdriver

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
HLTV_BASE = 'https://www.hltv.org'
HLTV_EVENTS_MATCH_LIST_URL = 'https://www.hltv.org/results?event={}'

# Download parameters
DOWNLOAD_TIMEOUT = 1000 # Number of seconds before timing out a download
DOWNLOAD_COMPLETION_CHECK_PERIOD = 5 # Number of seconds between each check for download completio


class ParseException(Exception):
    pass


def config_parser() -> None:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--events-path', type=str, required=True, 
                            help='Path to a .txt file where each line contains an HLTV event ID')
    parser.add_argument('--maps-path', type=str, required=True, 
                            help='Path to a .txt file where each line contains a map name')
    parser.add_argument('--output-path', type=str, required=True, 
                            help='Directory to store demos in')
    parser.add_argument('--chrome-bin', type=str, required=True, 
                            help='Path to a chrome binary for use with selenium')
    
    return parser.parse_args()


def init_browser(chrome_bin: str, output_path: str) -> webdriver.Chrome:
    """Initialize and return a new selenium headless browser
    
    Args:
        chrome_driver: path to a chrome driver
        chrome_bin: path to a chrome binary
        output_path: directory to download files to
    """
    
    download_prefs = {
        "download.default_directory": os.path.abspath(output_path),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    
    options = uc.ChromeOptions()
    options.add_experimental_option("prefs", download_prefs)
    options.binary_location = chrome_bin
    
    browser = uc.Chrome(use_subprocess=True, options=options)
    
    return browser


def get_matches_urls(browser: webdriver.Chrome, event: str) -> list[str]:
    """Return a list of HLTV match urls, for all matches in event.
    
    Args:
        browser: the selenium browser to use to make requests
        event: an HLTV event id
    """
    
    url = HLTV_EVENTS_MATCH_LIST_URL.format(event)
    
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    containers = soup.find_all('div', class_='result-con')
    match_urls = []
    
    for c in containers:
        a = c.find_all('a', recursive=False)
        
        if len(a) != 1:
            raise ParseException("Unrecognized HLTV event matches page format")
        
        match_urls.append(HLTV_BASE + a[0]['href'])
                
    return match_urls


def newest_file(directory: str):
    """Return the name of the newest file in directory.
    
    Args:
        - directory: the path to the directory to probe
    """
    
    files = sorted(os.listdir(directory),
                   key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    
    if len(files) == 0:
        raise FileNotFoundError("No files found in directory")
    
    return files[-1]


def wait_for_download_completion(download_dir: str,
                                 timeout: int = DOWNLOAD_TIMEOUT,
                                 check_period: int = DOWNLOAD_COMPLETION_CHECK_PERIOD):
    """Wait for download completion of the latest file in download_dir.
    Assumes that the file is downloaded using Chrome, and has a .crdownload extension.
    
    Args:
        - download_dir: the path to the downloads folder
        - timeout: the maximum amount of seconds allowed for the download, before termination
        - check_period: the period in seconds between each check for download completion
        
    Returns:
        - the seconds elapsed for the download, or -1 if the download reached timeout
    """
    
    start_time = time.time()
     
    while (time.time() - start_time) < timeout:
        time.sleep(check_period)
        
        if not newest_file(download_dir).endswith('.crdownload'):
            return time.time() - start_time
                
    return -1


def parse_match_page(page_source: str) -> tuple[str, list[str]]:
    """Parse an HLTV match page and return the demo download url
    and the match's list of maps
    
    Args:
        - page_source: a string of the HTML page source
    """
    
    soup = BeautifulSoup(page_source, 'html.parser')
    
    a = soup.find_all('a', {'data-demo-link': True})
    
    if len(a) != 1:
        raise ParseException("Unrecognized HLTV demos page format: unable to retrieve demo link")
    
    demo_link = HLTV_BASE + a[0]['data-demo-link']
    
    map_divs = soup.find_all('div', {'class': 'mapname'})
    
    if len(map_divs) == 0:
        raise ParseException("Unrecognized HLTV demos page format: unable to retrieve map list")
    
    maps = [div.text.strip() for div in map_divs]
    
    return demo_link, maps


def download_demo_zip(browser: webdriver.Chrome, match_url: str, maps: list[str], output_path: str):
    """Download the full demo zip file for match_url. Skip matches without at least 
    one map in maps. Return whether a download was successfully downloaded.
    
    Args:
        browser: the selenium browser to use to make requests
        match_url: the url of the HLTV match
        maps: a list of map names
        output_path: directory to download files to
    """
    
    browser.get(match_url)
    
    demo_link, match_maps = parse_match_page(browser.page_source)
    
    if set(match_maps).isdisjoint(maps):
        logging.info(f"Skipping {match_url} because no maps overlap")
        return False
    
    browser.get(demo_link)
        
    logging.info(f"Waiting for download {match_url} @ {demo_link}")
    
    if wait_for_download_completion(output_path) == -1:
        logging.error(f"Download for {match_url} reached timeout")
        return False
    else:
        logging.info(f"Download completed for {match_url}")
        return True
        

def download(browser: webdriver.Chrome, events: list[str], maps: list[str], output_path: str) -> None:
    """Download all CS2 demo files for a subset of maps at a list of HLTV events.
    
    Args:
        browser: the selenium browser to use to make requests
        events: A list of HLTV event ids
        maps: A list of map names
        output_path: The output path to store the demo files
    """
    
    for event in events:
        logging.info(f"Retrieving match list for {event}")
        match_urls = get_matches_urls(browser, event)
        
        logging.info(f"Downloading demos for {event}") 
        
        for match_url in match_urls:
            download_demo_zip(browser, match_url, output_path)
                
        
def parse_txt_file_list(filename: str) -> list[str]:
    """Read filename and return a list of each row, ignoring comments deliminated by #"""
    
    lst = []
    
    with open(filename, 'r') as f:
        for row in f:
            pound_loc = row.find('#')
            
            if pound_loc == -1:
                lst.append(row)
            elif pound_loc > 0: # Comment not first character
                lst.append(row[:pound_loc])
                
    return lst
        
        
if __name__ == '__main__':
    args = config_parser()
    
    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)
    
    browser = init_browser(args.chrome_bin, args.output_path)
    
    events = parse_txt_file_list(args.events_path)
    maps = parse_txt_file_list(args.maps_path)
    
    download(browser, events, maps, args.output_path)