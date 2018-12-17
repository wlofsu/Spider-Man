'''利用execute_script()方法将进度条下拉到底部，然后弹出alert提示框
基本上有了这个方法，API没有提供的所有功能都可以用执行JavaScript的方式来实现了'''
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')