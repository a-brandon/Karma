from dotenv import dotenv_values as load
from selenium.webdriver.chrome import options, webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait as Wait
from tqdm import tqdm

driver_options = options.Options()
# driver_options.add_experimental_option('detach', True) <- Will leave for future testing with GUI if necessary.
driver_options.add_argument('--headless')
driver_options.add_argument('--log-level=3')  # Disables unnecessary logging to terminal. Only outputs WARNINGs.
driver = webdriver.WebDriver(options=driver_options)


def main():
    login()
    Wait(driver, timeout=10).until(condition.url_to_be('https://www.reddit.com/'))
    join_subreddits(retrieve_subreddits())
    driver.quit()


def login():
    credentials = load('config/.env')
    driver.get('https://www.reddit.com/login/')

    for credential, info in credentials.items():
        if credential in ['USERNAME', 'PASSWORD']:
            driver.find_element(By.ID, f'login{credential.capitalize()}').send_keys(info)

    Wait(driver, timeout=10).until(condition.element_to_be_clickable((By.XPATH, '/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button'))).click()


def retrieve_subreddits():
    return [f'https://reddit.com/r/{sub_name}' for sub_name in load('config/.env')['MASTER_LIST'] .removeprefix('https://www.reddit.com/r/').split('+') if 'u_' not in sub_name]


def join_subreddits(sub_list: list):
    for sub_reddit in tqdm(sub_list):
        driver.get(sub_reddit)
        if driver.find_element(By.XPATH,'//*[@id="AppRouter-main-content"]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[1]/button').text == 'Joined':
            continue
        else:
            Wait(driver, timeout=10).until(condition.element_to_be_clickable((By.XPATH,'//*[@id="AppRouter-main-content"]/div/div/div[2]/div[1]/div/div/div/div[2]/div/button'))).click()

    print('All sub reddits joined.')


if __name__ == '__main__':
    main()
