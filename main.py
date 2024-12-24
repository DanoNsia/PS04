from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def search_wikipedia(query):
    # Запускаем браузер
    driver = webdriver.Firefox()

    # Открываем сайт Википедии
    driver.get("https://www.wikipedia.org/")

    # Находим поле ввода и вводим запрос
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    return driver


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text[:200]}...")  # Обрезаем текст для удобства


def list_related_links(driver):
    links = driver.find_elements(By.XPATH,
                                 "//div[@class='mw-parser-output']//a[contains(@href, '/wiki/') and not(contains(@href, ':'))]")
    related_links = {i + 1: link for i, link in enumerate(links)}
    for num, link in related_links.items():
        print(f"{num}: {link.text} - {link.get_attribute('href')}")
    return related_links


def main():
    initial_query = input("Введите ваш запрос: ")
    driver = search_wikipedia(initial_query)

    while True:
        print("\nВыберите действие:")
        print("1: Листать параграфы текущей статьи")
        print("2: Перейти на одну из связанных страниц")
        print("3: Выйти из программы")
        choice = input("Введите номер действия: ")

        if choice == '1':
            list_paragraphs(driver)
        elif choice == '2':
            related_links = list_related_links(driver)
            link_choice = int(input("Введите номер ссылки для перехода: "))
            if link_choice in related_links:
                driver.get(related_links[link_choice].get_attribute('href'))
                print(f"\nПерешли на страницу: {related_links[link_choice].text}")
            else:
                print("Неверный выбор ссылки.")
        elif choice == '3':
            print("Выход из программы.")
        break
    else:
        print("Неверный выбор. пожалуйста, попробуйте снова.")


    driver.quit()

if __name__ == "__main__":
    main()
