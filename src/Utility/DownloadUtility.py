import os
import ssl
import zipfile

import wget

from src.Common.Constants import constants
from src.Logging.Logger import Logger
from src.Utility.ConfigUtility import ConfigUtility
from src.Utility.FileUtility import FileUtility
from src.Utility.OSUtility import OSUtility

ssl._create_default_https_context = ssl._create_unverified_context


class DownloadUtility:
    def __init__(self):
        self.logger = None
        self.configUtil = ConfigUtility()
        self.fileUtil = FileUtility()
        self.config = self.configUtil.loadConfig(constants.commonConfigPath)["DownloadUrls"]
        self.app = None
        self.progressVar = None
        self.osUtil = OSUtility()


    def downloadChromeDriver(self, app, progressVar, configJson):
        self.app = app
        self.progressVar = progressVar
        self.logger = Logger(configJson, "DownloadUtility").logger
        self.logger.debug("downloadChromeDriver called...")
        chromeDriverUrl = self.config[constants.chromedriverConfigKey]
        self.fileUtil.deleteFolderIfExists(constants.chromeDriverFolderPath)
        self.fileUtil.createFolderIfNotExists(constants.chromeDriverFolderPath)
        chromeDriverOutputPath = os.path.join(constants.chromeDriverFolderPath, "ChromeDriver.zip")
        self.logger.info(f"""  Downloading Chrome Driver and Extracting..
                                URL: {chromeDriverUrl}
                                Output Path: {constants.chromeDriverFolderPath}
                                OS: {self.osUtil.getCurrentOS()}
                            """)

        wget.download(chromeDriverUrl, out=chromeDriverOutputPath, bar=self.updateProgress)
        self.logger.debug("Download Complete now Extracting...")
        with zipfile.ZipFile(chromeDriverOutputPath, "r") as zip_ref:
            zip_ref.extractall(constants.chromeDriverFolderPath)
            self.logger.info("Download and Extraction of Chromedriver completed.")

        self.fileUtil.deleteFileIfExists(chromeDriverOutputPath)


    def downloadChromeBinary(self, app, progressVar, configJson):
        self.app = app
        self.progressVar = progressVar
        self.logger = Logger(configJson, "DownloadUtility").logger
        self.logger.debug("downloadChromeBinary called...")
        chromeBinaryUrl = self.config[constants.chromebinaryConfigKey]
        self.fileUtil.deleteFolderIfExists(constants.chromeBinaryFolderPath)
        self.fileUtil.createFolderIfNotExists(constants.chromeBinaryFolderPath)
        chromeBinaryOutputPath = os.path.join(constants.chromeBinaryFolderPath, "ChromeBinary.zip")
        self.logger.info(f"""  Downloading Chrome Binary and Extracting..
                                URL: {chromeBinaryUrl}
                                Output Path: {constants.chromeBinaryFolderPath}
                                OS: {self.osUtil.getCurrentOS()}
                            """)

        wget.download(chromeBinaryUrl, out=chromeBinaryOutputPath, bar=self.updateProgress)
        self.logger.debug("Download Complete now Extracting...")
        with zipfile.ZipFile(chromeBinaryOutputPath, "r") as zip_ref:
            zip_ref.extractall(constants.chromeBinaryFolderPath)
            self.logger.info("Download and Extraction of ChromeBinary completed.")

        self.fileUtil.deleteFileIfExists(chromeBinaryOutputPath)


    def updateProgress(self, current, total, width=80):
        percentage = (current / total) * 100
        self.progressVar.set(percentage)
        self.app.update_idletasks()