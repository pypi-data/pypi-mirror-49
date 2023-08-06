# Required with every package
# Initializes package upon import call from python
#
# ex. 
# import package_name.other_python_file

def delDotPrefix(string):
    '''Delete dot prefix to file extension if present'''
    return string[1:] if string.find(".") == 0 else string

def filesInFolder(folder, fileType="*"):  
    '''Returns list of files of specified file type'''
    fileType = delDotPrefix(fileType)
    file_regex = re.compile(rf".*\.{fileType}", re.IGNORECASE)  # Regular Expression; dot star means find everything
    file_list = []
    for dirpath, _, filenames in os.walk(folder,):  # for each folder
        for file in filenames:
            file_search = file_regex.findall(file)
            if file_search:  # if file_search is not empty
                file_list.append(dirpath + '\\' + file)
    return file_list