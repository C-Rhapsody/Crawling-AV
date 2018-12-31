# Crawling-AkibaOnline

## 환경

* Raspbian
  * Raspi 3B
* Python 3.5.2
  * Selenium
  * WebDriver : ChromeDriver

## 참고
1. [클리앙 NAS당 : 토렌트 사이트에서 RSS.xml 생성하기](https://m.clien.net/service/board/cm_nas/12534455)

2. [Selenium으로 무적 크롤러 만들기](https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/)

3. [How to run Selenium Chrome webdriver on Raspberry pi](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/)

4. [라즈베리파이에서 selenium 사용](http://cinnamonapple.tistory.com/18)
## Command

### Selenium 설치
~~~
  pip install selenium
~~~

### Chrome Driver 설치
~~~
  wget http://launchpadlibrarian.net/361669488/chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
~~~

* 의존성 실패시
~~~
  apt --fix-broken install 
~~~

* Chrome-Driver 설치위치
  * /usr/lib/chromium-browser/chromedriver

### pyvirtualdisplay 설치

~~~
  pip3 install pyvirtualdisplay
~~~

  * 'Xvfb' 미설치 시
~~~
  apt install Xvfb
~~~