from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import json
import time

class HuerfanoSiteScraper:

    def __init__(self, base_url='https://www.thecountyrecorder.com/'):
        self.base_url = base_url
        self.driver = webdriver.Chrome()

    def query_docs_from_year(self, year):
        self.driver.get(self.base_url)

        state_selector_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_ctl00_cboStates")
        state_selector_element.send_keys("Colorado")
        time.sleep(1)
        state_go_button_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_ctl00_btnChangeState")
        state_go_button_element.click()
        time.sleep(1)
        county_selector_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_ctl00_cboCounties")
        county_selector_element.send_keys("Huerfano")
        time.sleep(1)
        document_search_link_element = self.driver.find_element_by_id("TreeView1t5")
        document_search_link_element.click()
        time.sleep(1)

        start_date = "01/01/" + str(year)
        start_date_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbDateStart")
        start_date_element.send_keys(start_date)
        time.sleep(1)
        end_date = "01/01/" + str(year + 1)
        end_date_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbDateEnd")
        end_date_element.send_keys(end_date)
        time.sleep(1)

        execute_search_button_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_btnSearchDocuments")
        execute_search_button_element.click()
        time.sleep(1)
    
    def set_doc_page(self, page_index):
        doc_page_dropdown_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_cboPage")
        doc_page_dropdown = Select(doc_page_dropdown_element)
        doc_page_dropdown.select_by_index(page_index)
        time.sleep(1)
    
    def get_doc_page_count(self):
        doc_page_dropdown_element = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_cboPage")
        options = [x for x in doc_page_dropdown_element.find_elements_by_tag_name("option")]
        return len(options)
    
    def scrape_docs_from_page(self):
        global year
        doc_table = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_Table2")
        rows_except_header = doc_table.find_elements_by_xpath(".//tr")[1:]
        for row in rows_except_header:
            document_link_element = row.find_element_by_xpath(".//a")
            self.driver.execute_script(
                "window.open(arguments[0]);",
                document_link_element)

            document_window = self.driver.window_handles[1]
            self.driver.switch_to.window(document_window)

            time.sleep(1)

            # Scrape window for doc data.
            document_id = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbReceptionNo").get_property("value")
            book_page = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbBookPage").get_property("value")
            recording_date = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbReceptionDate").get_property("value")
            document_type = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbDocumentType").get_property("value")
            description = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_tbDescription").get_property("value")
            grantor_table = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_Table2").text
            grantee_table = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_Table3").text
            legal_table_1 = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_Table1").text
            legal_table_2 = self.driver.find_element_by_id("MainContent_searchMainContent_ctl00_Table5").text
            legal_table_3 = self.driver.find_element_by_id("Table205").text
            legal_table_4 = self.driver.find_element_by_id("Table206").text

            legal_table_1_rows = legal_table_1.split('\n')[1:]
            legal_table_1 = ''
            if len(legal_table_1_rows) > 0:
                legal_table_1 = legal_table_1_rows[0]
                for row in legal_table_1_rows[1:]:
                    legal_table_1 = legal_table_1 + '\n' + row

            legal_table_2_rows = legal_table_2.split('\n')[1:]
            legal_table_2 = ''
            if len(legal_table_2_rows) > 0:
                legal_table_2 = legal_table_2_rows[0]
                for row in legal_table_2_rows[1:]:
                    legal_table_2 = legal_table_2 + '\n' + row

            file_name = './o_' + str(year) + '.txt'
            file = open(file_name, 'a')
            data = {
                'document_id': document_id,
                'book_page': book_page,
                'recording_date': recording_date,
                'document_type': document_type,
                'description': description,
                'grantor_table': grantor_table,
                'grantee_table': grantee_table,
                'legal_table_1': legal_table_1,
                'legal_table_2': legal_table_2,
                'legal_table_3': legal_table_3,
                'legal_table_4': legal_table_4
            }
            data_string = json.dumps(data)
            file.write(',')
            file.write(data_string)

            self.driver.close()
            
            document_window = self.driver.window_handles[0]
            self.driver.switch_to.window(document_window)

    def close(self):
        self.driver.close()



year = 0
if __name__ == '__main__':
    years = [ 2009 ]
    for y in years:
        try:
            site = HuerfanoSiteScraper()
            year = y
            site.query_docs_from_year(year)
            doc_page_count = site.get_doc_page_count()
            for page_index in range(0, doc_page_count):
                site.set_doc_page(page_index)
                site.scrape_docs_from_page()
        except:
            pass

# 386204