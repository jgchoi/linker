import os
import filechecker
import epubToTxt

# Get the current working directory
cwd = os.getcwd()

# Get the path of the files directory
files_dir = os.path.join(cwd, "files")

# Get the list of files in the files directory
files = os.listdir(files_dir)

# Print out the file names
for file in files:
    if file.endswith(".epub"):
        
        epub_path = os.path.join(files_dir, file)  # replace with your epub file path
        txt_path = os.path.splitext(epub_path)[0] + '.txt'  # create txt file path

        text = epubToTxt.epub_to_txt(epub_path)
        epubToTxt.write_to_txt(text, txt_path)
        print(f"Converted {file} to {txt_path}")

    if file.endswith(".txt"):
        file = file[:-4]

        if "[" in file or "]" in file or "(" in file or ")" in file or "-" in file or "?" in file:
            print("File name contains invalid character")
            continue


        author, lastEpisodNumber = filechecker.get_author_and_episode(file)
        print(author, lastEpisodNumber)

        # if author is None, break
        if author is None:
            print("Author is None")
            continue

        newfileName = f"[{author}] {file} {lastEpisodNumber} 완.txt"

        os.rename(os.path.join(files_dir, file + ".txt"), os.path.join(files_dir, newfileName))
        print(f"Renamed {file} to {newfileName}")
 


        
    

    