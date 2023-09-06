from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.Logging.Logger import Logger
from src.ScraperMethod.ExtensionMethod.ScraperModules.UrlUtility import UrlUtility


class ApiUtility:
    def __init__(self, configJson):
        self.browser = None
        self.timeout = 10
        self.urlUtils = UrlUtility()
        self.logger = Logger(configJson, "ApiUtility").logger


    def executeJsToGetJson(self, url):
        self.logger.info(f"Executing JS to get JSON from URL")
        apiJsonScript = f"""
            return new Promise((resolve, reject) => {{
                fetch("{url}")
                    .then(response => response.json())
                    .then(data => {{
                        resolve(data);
                    }})
                    .catch(error => {{
                        reject(error);
                    }});
            }});
        """
        return self.browser.execute_script(apiJsonScript)


    def getCourseApiContentJson(self, courseApiUrl):
        try:
            self.logger.info(f"Getting Course API Content JSON from URL: {courseApiUrl}")
            jsonData = self.executeJsToGetJson(courseApiUrl)
            if "components" in jsonData:
                jsonData = jsonData["components"]
                return jsonData
            return None
        except Exception as e:
            lineNumber = e.__traceback__.tb_lineno
            raise Exception(f"ApiUtility:getCourseApiContentJson: {lineNumber}: {e}")


    def getCourseCollectionsJson(self, topicUrl):
        try:
            self.logger.info(f"Getting Course Collections JSON from URL: {topicUrl}")
            courseApiUrl = self.urlUtils.getCourseApiCollectionListUrl(topicUrl)
            self.browser.get("https://www.educative.io/api/")
            jsonData = self.executeJsToGetJson(courseApiUrl)
            jsonData = jsonData["instance"]["details"]
            authorId = str(jsonData["author_id"])
            collectionId = str(jsonData["collection_id"])
            categories = jsonData["toc"]["categories"]
            courseTitle = jsonData["title"]
            topicApiUrlList = []
            topicNameList = []
            baseApiUrl = f"https://educative.io/api/collection/{authorId}/{collectionId}/page/"
            for category in categories:
                if not category["pages"]:
                    topicApiUrlList.append(baseApiUrl + str(category["id"]))
                    topicNameList.append(category["title"])
                for page in category["pages"]:
                    topicApiUrlList.append(baseApiUrl + str(page["id"]))
                    topicNameList.append(page["title"])
            return {
                "courseTitle": courseTitle,
                "topicApiUrlList": topicApiUrlList,
                "topicNameList": topicNameList
            }
        except Exception as e:
            lineNumber = e.__traceback__.tb_lineno
            raise Exception(f"ApiUtility:getCourseCollectionsJson: {lineNumber}: {e}")


    def getCourseTopicUrlsList(self, topicUrl):
        try:
            self.logger.info(f"Getting Course Topic URLs List from URL: {topicUrl}")
            courseUrlSelector = self.urlUtils.getCourseUrlSelector(topicUrl)
            self.browser.get(topicUrl)
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, courseUrlSelector)))
            topicUrlElements = self.browser.find_elements(By.XPATH, courseUrlSelector)
            topicUrls = []
            for topicUrlElement in topicUrlElements:
                topicUrls.append(topicUrlElement.get_attribute("href"))
            return topicUrls
        except Exception as e:
            lineNumber = e.__traceback__.tb_lineno
            raise Exception(f"ApiUtility:getCourseTopicUrlsList: {lineNumber}: {e}")
