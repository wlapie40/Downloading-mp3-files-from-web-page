import threading
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve

def MainJob(q):
    while (True):
        item = q.get();
        driver = webdriver.Chrome()
        main_window = driver.current_window_handle
        driver.get(link + "/" + str(item))
        try:
            content = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='circle circle-btn sound audio_play_button']")))
            url = download_link + "/" + content.get_attribute("data-src-mp3")
            urlretrieve(url, "MP3/" + item + ".mp3")
            driver.close()
            q.task_done()
        except Exception as e:
            print(str(e) + " There was an issue with word: " + item)
            q.task_done()
            continue

def Queue(q):
    for i in range(len(new_words)):
        item = str(new_words[i])
        q.put(item)
    q.join()


if __name__ == '__main__':
    q = queue.Queue()
    link = 'https://dictionary.cambridge.org/dictionary/english'
    download_link = 'https://dictionary.cambridge.org'
    new_words = [word.replace('\n', '') for word in open(r'new_words.txt', 'r').readlines()]
    threads_num = 4

    for i in range(threads_num):
        t = threading.Thread(name="ConsumerThread-" + str(i), target=MainJob, args=(q,))
        t.start()

    t = threading.Thread(name="ProducerThread", target=Queue, args=(q,))

    t.start()
    q.join()


print('Finished')
