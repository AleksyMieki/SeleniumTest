from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def get_top_trending_videos():
    # Create a new instance of the browser driver
    driver = webdriver.Chrome()

    # Navigate to the YouTube trending page
    driver.get("https://www.youtube.com/feed/trending")

    try:
        # Wait until the video elements are present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="video-title"]'))
        )

        # Find the video elements using XPath
        video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    except Exception as e:
        print("An error occurred: ", e)
        driver.quit()
        return []

    # Get the titles of the top 3 videos
    top_videos = [video_element.get_attribute("title") for video_element in video_elements[:3]]

    # Close the browser
    driver.quit()

    return top_videos


def save_videos_to_file(videos, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for video in videos:
            file.write(video + "\n")



def main():
    # Get the top 3 trending videos
    top_videos = get_top_trending_videos()

    # Define the file path and name
    file_path = "videos.txt"

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the existing file contents
        with open(file_path, "r", encoding="utf-8") as file:
            existing_videos = file.read().splitlines()

        # Check if the contents have changed
        if set(top_videos) == set(existing_videos):
            print("The top trending videos have not changed since the last run.")
            return

    # Save the videos to the file
    save_videos_to_file(top_videos, file_path)
    print("The top trending videos have been updated.")

if __name__ == "__main__":
    main()

