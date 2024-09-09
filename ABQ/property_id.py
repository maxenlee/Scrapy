import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

# Set up Selenium WebDriver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(), options=options)

# Memoization for storing parcel IDs and their details
all_parcel_data = {}

def extract_parcel_data():
    """Extract data from the current page and store it in a dictionary."""
    try:
        # Locate the table body containing the search results
        table_body = driver.find_element(By.XPATH, '//*[@id="searchResults"]/tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Loop through the rows and extract the data
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) > 0:
                parcel_id = cells[0].text  # First column is Parcel ID
                owner_name = cells[1].text  # Adjust index based on actual data
                address = cells[2].text     # Adjust index based on actual data
                rp_type = cells[3].text     # Adjust index based on actual data
                year = cells[4].text        # Adjust index based on actual data

                # Store the Parcel ID and associated data in the dictionary
                all_parcel_data[parcel_id] = {
                    'Owner Name': owner_name,
                    'Address': address,
                    'RP Type': rp_type,
                    'Year': year
                }
    except Exception as e:
        print(f"Error extracting parcel data: {e}")

def navigate_next_page():
    """Click the 'Next' button using the <a> element or manually trigger the JS."""
    try:
        # Try clicking the "Next" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[font/b[contains(text(), "Next")]]'))
        )
        next_button.click()

        return True
    except Exception as e:
        print(f"No more pages or error navigating to the next page: {e}")
        return False

def scrape_all_pages():
    """Scrape parcel data from all pages by iterating through the search results."""
    while True:
        # Extract parcel data from the current page
        extract_parcel_data()
        
        # Try to navigate to the next page
        if not navigate_next_page():
            break  # If no more pages or error in navigation, break out of the loop
        
        # Wait before loading the next page
        time.sleep(.5)  # Adjust the sleep time if needed

def perform_search(search_prefix):
    """Perform a search based on the given prefix."""
    try:
        # Navigate to the search page and accept disclaimer if not already done
        driver.get('https://assessor.bernco.gov/public.access/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=realprop')
        
        login_form = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btAgree"]'))
        )
        login_form.click()

        # Perform the search based on the search prefix
        search_bar = driver.find_element(By.XPATH, '//*[@id="inpSuf"]')
        search_bar.clear()
        search_bar.send_keys(f'{search_prefix}*')
        
        # Set the dropdown for page size to display more results
        dropdown_element = driver.find_element(By.XPATH, '//*[@id="selPageSize"]')
        dropdown = Select(dropdown_element)
        dropdown.select_by_index(4)  # Example: selecting the 50-item-per-page option

        # Start the search
        search_bar.send_keys(Keys.RETURN)
        
        # Scrape data across all pages
        scrape_all_pages()

        # After search, check for 'No results found'
        try:
            no_results = driver.find_element(By.XPATH, f'//*[@id="frmMain"]/table/tbody/tr/td/div/div/table[2]/tbody/tr/td/table/tbody/tr[3]/td/center/table[1]/tbody/tr[1]/td/div/p')
            if no_results.text == 'No results found':
                print(f'No results found for prefix {search_prefix}')
                return False  # No need to expand further
        except:
            # Continue if no 'No results found' message is displayed
            return True  # Results were found, continue expanding the search

    except Exception as e:
        print(f"Error during search with prefix '{search_prefix}': {e}")
        return False

def brute_force_search(base_prefix, max_depth):
    """Recursively perform brute force search using prefixes."""
    # First perform the search with the current prefix
    if not perform_search(base_prefix):
        return  # Stop expanding if no results found

    # Base case: Stop if the maximum depth is reached
    if len(base_prefix) >= max_depth:
        return

    # Recursive case: Continue building the prefix by adding digits (0-9)
    for i in range(10):
        next_prefix = base_prefix + str(i)
        brute_force_search(next_prefix, max_depth)

def save_data_to_csv():
    """Save the extracted data to a CSV file locally."""
    df = pd.DataFrame.from_dict(all_parcel_data, orient='index')
    file_path = os.path.join(os.getcwd(), 'parcel_data.csv')  # Save to current working directory
    df.to_csv(file_path)
    print(f"Data saved to {file_path}")

# Step 1: Perform brute force search with a starting prefix and max depth
base_prefix = "1"  # Start with '1', you can modify this
max_depth = 7  # Adjust depth to handle cases like '1000235*'

brute_force_search(base_prefix, max_depth)

# Step 2: Save the data to CSV after all searches are completed
save_data_to_csv()

# Close the browser
driver.quit()
