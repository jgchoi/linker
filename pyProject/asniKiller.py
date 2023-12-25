import os


# Get the current working directory
cwd = os.getcwd()

files_dir = os.path.join(cwd, "files")

files = os.listdir(files_dir)

for file in files:
   if file.endswith(".txt"):
        print('checking: ', file)
        
        try:
            with open(os.path.join(files_dir, file), encoding='mbcs') as f:
                # replace mbcs with utf-8 encoding
                content = f.read()
                content = content.replace('mbcs', 'utf-8')
                # write the content back to the file
                with open(os.path.join(files_dir, file), 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except:
            print(file, ' failed to open with mbcs')
    