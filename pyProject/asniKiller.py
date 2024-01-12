import os


# Get the current working directory
cwd = os.getcwd()

files_dir = os.path.join(cwd, "files")

files = os.listdir(files_dir)

for file in files:
   if file.endswith(".txt"):
        print('checking: ', file)
        
        # create array of encodings
        encodings = ['cp950', 'mbcs', 'euc_kr', 'cp949', 'iso2022_jp_2', 'iso2022_kr', 'johab']

        # each encoding in the array, perform the following
        for encoding in encodings:
            try:
                with open(os.path.join(files_dir, file), encoding=encoding) as f:
                    # replace mbcs with utf-8 encoding
                    content = f.read()
                    content = content.replace(encoding, 'utf-8')
                    # write the content back to the file
                    with open(os.path.join(files_dir, file), 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(file, ' converted to utf-8')    
            except:
                print(file, ' failed to open with ', encoding)
