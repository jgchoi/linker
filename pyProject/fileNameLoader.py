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

        try:
            text = epubToTxt.epub_to_txt(epub_path)
            epubToTxt.write_to_txt(text, txt_path)
            print(f"Converted {file} to {txt_path}")
        except:
            print(f"Failed to convert {file} to {txt_path}")
            continue
    if file.endswith(".txt"):
        file = file[:-4]
        print(file)

        # if file contains any of following character, break "[]()-?"
        if "[" in file or "]" in file or "(" in file or ")" in file or "-" in file or "?" in file:
            print("File name contains invalid character")
            continue

        author, lastEpisodNumber = filechecker.get_author_and_episode(file)
        print(author, lastEpisodNumber)

        # if author is None, break
        if author is None:
            print("Author is None")
            continue

        new_file_name = f"[{author}] {file}.txt"

        os.rename(os.path.join(files_dir, file + ".txt"), os.path.join(files_dir, new_file_name))
        print(f"Renamed {file} to {new_file_name}")
 


        
    

    