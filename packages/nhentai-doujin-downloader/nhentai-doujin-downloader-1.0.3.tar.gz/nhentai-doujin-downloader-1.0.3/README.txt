This is a simple program that allows you to download Doujins from nHentai. It will save the Doujins as JPEG files, and will store them in the current directory. It will log to the console the page numbers that have been downloaded whilst the process is running, with a final message once the process has terminated successfully.
Usage:
import importlib  
nh = importlib.import_module("nHentaiDoujinDownloader")
nh.downloadDoujin(177013, 20)
