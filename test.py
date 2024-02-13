import os
from instabot import Bot
import schedule
import time
import threading

def crawl_folder_and_post(folder_path="scheduler/Camera", caption="Your caption here", posting_time="20:31"):
    """
    Crawls a folder, posts new images to Instagram, and schedules itself to run again.

    Args:
        folder_path: The path to the folder containing images.
        caption: The caption to use for each posted image.
        posting_time: The time of day (in "HH:MM" format) to post images.

    Raises:
        KeyError: If the `csrftoken` is missing from Instagram API cookies.
        Exception: For any other errors during login or posting.
    """

    bot = Bot()

    try:
        bot.login(username="also_pratyush0095", password="Pratyush@123")

        for root, _, files in os.walk(folder_path):
            for filename in files:
                if is_image_file(filename):
                    file_path = os.path.join(root, filename)
                    if os.path.exists(file_path):
                        try:
                            schedule.every().day.at(posting_time).do(bot.upload_photo, file_path, caption=caption)
                        except KeyError:
                            print("Error: Instagram API login token (csrftoken) not found. Check your login credentials.")
                        except Exception as e:
                            print(f"Error posting {file_path}: {e}")

        while True:
            schedule.run_pending()
            time.sleep(1)

    finally:
        bot.logout()

def is_image_file(filename):
    """
    Checks if the filename has a valid image extension.

    Args:
        filename: The name of the file.

    Returns:
        True if the filename ends with a common image extension, False otherwise.
    """
    return filename.endswith((".jpg", ".png", ".jpeg"))

if __name__ == "__main__":
    crawl_folder_and_post()

