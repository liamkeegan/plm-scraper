# Import the selenium webdriver package
# Requires selenium, a local instance of chrome, as well as the chrome driver package
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Use ptable/PrettyTable to format the output into a nice list
from prettytable import PrettyTable

# URLs, descriptions and username/passwords and the Teams Bot access key are kept in the auth.py file
from auth import plm_list
from auth import teams_access_token, teams_room_id

# WebEx Teams to output results to a Teams room
from webexteamssdk import WebexTeamsAPI

# Used to create the tempfile for Teams attachment
import os
import tempfile
from datetime import datetime

# Sets the Room ID in teams


# Sets the Selenium driver options
options = Options()
# Run in headless mode (no window), suppress logging messages, run in incogneto, no notifications, cert errors
options.add_argument("--headless")
options.add_argument("--disable-notifications")
options.add_argument("--incognito")
options.add_argument("log-level=3")
options.add_argument("--ignore-certificate-errors")

# Creates a driver object to gather webpages. Requires the chromedriver to be located in the same folder.
# Read selenium docs for more info
driver = webdriver.Chrome(options=options, executable_path="./chromedriver")


# Function to connect to ELM and screenscrape
# This finds the elements on the page, then pulls out just the text
def get_plm(url, username, password):
    try:
        # Get the URL passed into the function
        driver.get(url)
        # Have a 10 second timeout waiting for data to appear on page
        driver.implicitly_wait(10)
        # Type username into username field
        driver.find_element_by_id("dijit_form_TextBox_0").clear()
        driver.find_element_by_id("dijit_form_TextBox_0").send_keys(username)
        # Type password into password field
        driver.find_element_by_id("dijit_form_TextBox_1").clear()
        driver.find_element_by_id("dijit_form_TextBox_1").send_keys(password)
        # Click submit
        driver.find_element_by_id("LP_loginSubmit_label").click()
        # Grab the output of the summary table for licensing errors
        summary_raw = driver.find_element_by_xpath(
            "//*[@id='connecttable']/div[4]/div[2]"
        ).text
        # Find top menu, click on it
        driver.find_element_by_xpath(
            "//li[@id='xwt_widget_navigation_NavigationMenuItem_1']/span/span[3]"
        ).click()
        # Click on "Usage"
        driver.find_element_by_xpath(
            "//li[@id='xwt_widget_navigation_TaskBasedMenuItem_0']/span"
        ).click()
        # Reads data out of the raw table for license usage
        plm_raw = driver.find_element_by_class_name("table-body").text

        # Splits the output into a list
        plm = plm_raw.splitlines()
        summary = summary_raw.splitlines()

        # Takes every six objects and sends them into a new list
        x = 0
        plm_output = []
        for i in range(x, len(plm), 6):
            x = i
            plm_output.append(plm[x : x + 6])
        # Returns the list of lists

        summary_output = []
        x = 0
        for i in range(x, len(summary), 3):
            x = i
            summary_output.append(summary[x : x + 3])
        return {"plm": plm_output, "summary": summary_output}

    except:
        # If there's a problem gathering data, return a bunch of NO DATA values
        return {
            "plm": '["NO DATA","NO DATA","NO DATA","NO DATA","NO DATA","NO DATA"]',
            "summary": '["NO DATA", "NO DATA", "NO DATA"]',
        }


# The output_table will hold the text representation of each PLM table and error table output. It starts as an empty string
if __name__ == "__main__":
    plm_output_table = ""
    summary_output_table = ""

    # This reads the value of the list of dicts called plm_list from the auth.py file and stars iterating through each
    for plm in plm_list:
        # Calls the get_plm function and returns the list of lists into a var plm_data
        plm_data = get_plm(plm["url"], plm["username"], plm["password"])
        # Creates a new PrettyTable object called table
        plm_table = PrettyTable()
        # For each row in the plm_data list of lists, add it to the PrettyTable
        for row in plm_data["plm"]:
            plm_table.add_row(row)
        # Adds the headers
        plm_table.field_names = [
            "Type",
            "Product",
            "Required",
            "Installed",
            "Available",
            "Status",
        ]
        # Writes the table with a header and newline to the output_table string
        plm_output_table = (
            plm_output_table
            + "\n"
            + plm_table.get_string(title=plm["descr"] + ": License Usage")
        )

        # If there isn't anything in the summary table, just skip this section
        if "No data available" in plm_data["summary"][0]:
            pass
        else:
            # if there is a summary table, create a summary_table object and add contents to it
            summary_table = PrettyTable()
            for inv in plm_data["summary"]:
                summary_table.add_row(inv)
            summary_table.field_names = ["Product", "Message", "Date Raised"]
            summary_output_table = (
                summary_output_table
                + "\n"
                + summary_table.get_string(title=plm["descr"] + ": ISSUES")
            )

    # Cleanly exit the WebDriver as to not leave any processes running
    driver.quit()

    # Let's format the output into one big blob
    # First, check if there are any licensing issues present. If so, add them into the license table first.
    if len(summary_output_table) > 1:   
        message = summary_output_table + "\n\n" + plm_output_table
    else:
        message = plm_output_table
    print(message)
    # Send results to Teams room
    dateTimeObj = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp = tempfile.NamedTemporaryFile(mode='w+t', suffix='.txt', prefix=f'cloud-lic-{dateTimeObj}_', delete=False)
    try:
        temp.write(message)
    finally:
        temp.close()
        api = WebexTeamsAPI(access_token=teams_access_token)
        api.messages.create(teams_room_id, markdown="Cloud Licensing Report", files=[temp.name])
        os.remove(temp.name)
    