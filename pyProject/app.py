import tkinter as tk
import main
import asyncio
import threading

# Define an async function that will call main.download_novel
async def download_novel_async(url, progress_callback):
    await main.download_novel(url, progress_callback=progress_callback)

# Create the main window with width 500 height 300
root = tk.Tk()
root.geometry("500x900")

def create_widgets():
    label = tk.Label(root)
    label.pack()

    entry = tk.Entry(root, width=500)
    entry.pack()

    button = tk.Button(root, text="Start")
    button.pack()

    progressLabel = tk.Label(root, text="")
    progressLabel.pack()

    button.config(command=lambda: handleStartButton(label, entry, button, progressLabel))

# Modify the handleStartButton function
def handleStartButton(label, entry, button, progressLabel):
    create_widgets()

    url = entry.get()

    def update_progress(progress, url):
        if progress is not None:
            progressLabel.config(text=f"다운로드중: {progress}")
        if url is not None:
            # Update content in entry
            entry.delete(0, tk.END)
            entry.insert(0, url)

    # Run the asyncio event loop in a new thread
    threading.Thread(target=asyncio.run, args=(download_novel_async(url, update_progress),)).start()

create_widgets()


# Start the event loop
root.mainloop()