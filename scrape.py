import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the site
url = "https://hprera.nic.in/PublicDashboard"

# Send a GET request to the site
response = requests.get(url, verify=False)  # Bypass SSL verification
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing registered projects
projects_table = soup.find('table', {'id': 'example'})

# Get the first 6 projects
rows = projects_table.find_all('tr')[1:7]  # Skipping the header row

# List to store project details
projects = []

for row in rows:
    cells = row.find_all('td')
    rera_number = cells[0].text.strip()
    project_name = cells[1].text.strip()
    
    # Get the detail page link
    detail_link = cells[0].find('a')['href']
    detail_url = f"https://hprera.nic.in{detail_link}"
    
    # Send a GET request to the detail page
    detail_response = requests.get(detail_url, verify=False)  # Bypass SSL verification
    detail_response.raise_for_status()
    
    # Parse the detail page content
    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
    
    # Extract required details
    gstin_no = detail_soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblGSTNo'}).text.strip()
    pan_no = detail_soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblPANNo'}).text.strip()
    name = detail_soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblPromoterName'}).text.strip()
    permanent_address = detail_soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblPromoterAddress'}).text.strip()
    
    # Append the details to the projects list
    projects.append({
        'RERA Number': rera_number,
        'Project Name': project_name,
        'GSTIN No': gstin_no,
        'PAN No': pan_no,
        'Name': name,
        'Permanent Address': permanent_address
    })

# Create a DataFrame and display the details
df = pd.DataFrame(projects)
print(df)

# Save the DataFrame to a CSV file
df.to_csv('registered_projects.csv', index=False)
