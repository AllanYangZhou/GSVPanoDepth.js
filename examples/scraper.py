import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict
import os
import base64

parser = argparse.ArgumentParser()
parser.add_argument('out', type=str)
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--end', type=int, default=1000)
args = parser.parse_args()

driver = webdriver.Chrome(executable_path='./chromedriver')
i = args.start
pids = OrderedDict()

os.mkdir(args.out)

while i < args.end:
    try:
        driver.get('file:///home/allan/Projects/GSVPanoDepth.js/examples/example.html')
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'pano')))
        element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'depth')))
        pid = driver.find_element_by_tag_name('p').text
        if pid in pids:
            print('{:d} Repeat, skipping.'.format(i))
            continue
        pids[pid] = True
        pano = driver.find_element_by_id('pano')
        depth = driver.find_element_by_id('depth')
        data = {'pano': pano, 'depth': depth}
        for key in data:
            canvas = data[key]
            canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
            canvas_png = base64.b64decode(canvas_base64)
            with open(os.path.join(args.out, '{:s}{:d}.png'.format(key, i)), 'wb') as f:
                f.write(canvas_png)
        i += 1
    except TimeoutException:
        print('{:d} Timeout, skipping...'.format(i))
    finally:
        driver.refresh()

driver.quit()

with open(os.path.join(args.out, 'panoIds.txt'), 'w') as f:
    i = 0
    for pid in pids:
        f.write('{:d} {:s}\n'.format(i, pid))
        i += 1
