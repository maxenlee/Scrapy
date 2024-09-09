# Scrapy

## Project Overview
This project is designed to scrape property information from the Bernalillo County Assessor's Office public records. The script automates searches for property data using Selenium, leveraging a brute-force search strategy to find Parcel IDs and retrieve associated data.

The project is containerized using Docker to provide a consistent development environment. You can set up the project in a Docker container using Docker Desktop and the provided Dockerfile and docker-compose-dev.yaml.

## Repo Structure
```
.Scrapy
├── ABQ
│   ├── property_id.py         # Main Selenium script to scrape data
│   ├── test_config.py         # Script to test and verify Selenium configuration
├── Bern Co - Current.ipynb     # Jupyter Notebook for additional experimentation
├── Dockerfile                  # Dockerfile to containerize the scraper environment
├── compose-dev.yaml            # Docker Compose configuration for development
├── main.py                     # Main entry script to launch the scraper
```
## Dev Environment Setup (Docker Desktop)
Step 1: Install Docker Desktop
Make sure you have Docker Desktop installed on your machine. You can download it from the official Docker website: https://www.docker.com/products/docker-desktop.

Step 2: Use Docker Desktop for the Dev Environment
Docker Desktop allows you to set up a complete dev environment automatically. Here’s how to do it:

Open Docker Desktop.
Navigate to the Dev Environments tab.
Click Create and point it to this repository.
Docker will automatically use the docker-compose-dev.yaml and Dockerfile to set up the dev environment.
Note: The docker-compose-dev.yaml and Dockerfile are already configured to build the development environment. This will include all necessary dependencies (like Selenium, ChromeDriver, etc.).

## How to Run the Project
Once the Docker dev environment is set up, you can start using the development container to run the scraper.

1. Running the Main Scraper Script
To run the main scraper, execute the following command from the dev container's terminal:
```
python ABQ/property_id.py
```
This will initiate the scraping process, and the extracted data will be saved as a CSV file (parcel_data.csv) in the current working directory.

2. Testing the Setup
You can run the test_config.py script to verify that the Selenium setup is functioning correctly:

```
python ABQ/test_config.py
```
This script is designed to ensure that Selenium is properly configured and able to launch the browser for web scraping.

3. Running Jupyter Notebooks
You can also launch the Jupyter Notebook (Bern Co - Current.ipynb) from within the container. This can be useful for additional data exploration or testing.

To launch the notebook, use the following command:
```
jupyter notebook --ip 0.0.0.0 --allow-root
```
You can then access the notebook through your web browser by visiting the URL displayed in the terminal.

Understanding the Code
1. property_id.py
Purpose: This is the main scraping script. It automates the process of searching property IDs using Selenium and retrieves property data across multiple pages. The data is saved into a CSV file at the end of the process.

Key Components:

perform_search: Executes a search based on a given prefix.
brute_force_search: Recursively expands the search prefix and handles the stopping condition (i.e., when no results are found).
extract_parcel_data: Extracts property data from the search results and stores it in a dictionary.
save_data_to_csv: Saves the extracted data to a CSV file.
2. main.py
Purpose: This script serves as an alternative entry point for launching the scraper. It can be extended or modified based on your project needs.
3. test_config.py
Purpose: This is a simple script designed to test whether the Selenium setup is functioning correctly by launching a browser session and verifying basic interactions.

## Next Steps for Improvement
Optimizing the Search Strategy:

Instead of brute-forcing through every possible prefix, consider implementing a smarter search strategy. You can start by prioritizing more likely ranges of parcel IDs or leverage previous results to skip known gaps in the numbering.
Parallelization for Faster Scraping:

To speed up the scraping process, consider using parallelization via asyncio, threading, or multiprocessing. This can allow you to perform multiple searches in parallel, significantly reducing execution time.
Robust Error Handling and Logging:

Improve the error handling in case of Selenium crashes, timeouts, or unexpected changes to the website structure. Adding logging will also help track issues more efficiently.
Database Integration:

Rather than storing the scraped data as a CSV, consider integrating with a database like PostgreSQL or MongoDB for better scalability and query efficiency.
Automated Job Scheduling:

Set up a cron job or a task queue (e.g., Celery) to run the scraper at scheduled intervals. This ensures that your data stays up to date without manual intervention.
Testing Framework:

Expand the test_config.py into a full-fledged testing suite using a tool like pytest. This will help ensure that future changes to the code do not break functionality.
Dynamic Web Page Handling:

If the target website changes its structure frequently, it may be useful to implement more dynamic XPath handling, using more generalized selectors or even machine learning to adapt to website changes.
