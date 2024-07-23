from PIL import ImageGrab
import sys,os,time,zipfile,shutil
screenshot_information="screenshot.png"
number_of_iterations = int(sys.argv[1])*2

folder_name = 'screenshots'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def screenshot(iteration):
    screenshot_name = os.path.join(folder_name, f"screenshot{iteration}.png")
    im = ImageGrab.grab()
    im.save(screenshot_name)

for i in range(1, number_of_iterations + 1):
    time.sleep(30)
    screenshot(i)

zip_filename = 'screenshots.zip'
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(folder_name):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zipf.write(file_path, os.path.relpath(file_path, folder_name))
shutil.rmtree(folder_name)
