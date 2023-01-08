import sys, os, re, shutil
import os.path

def main(path):
    path_root = path
    dst_doc = path_root + '\\' + 'documents'
    global new_folders
  
    
    photo_files = ['\.jpeg$','\.png$','\.jpg$','\.svg$']
    video_files = ['\.avi$','\.mp4$','\.mov$','\.mkv$']
    doc_files = ['\.doc$','\.docx$','\.txt$','\.pdf$', '\.xls$', '\.xlsx$', '\.pptx$', '\.mpp$']
    audio_files = ['\.mp3$', '\.ogg$', '\.wav$', '\.amr$']
    arch_files = ['\.zip$', '\.gz$', '\.tar$', '\.7z$', '\.rar$']
    unknown_files = []
    unknown_files.extend(photo_files)
    unknown_files.extend(video_files)
    unknown_files.extend(doc_files)
    unknown_files.extend(audio_files)
    unknown_files.extend(arch_files)
    
    new_folders = ['images', 'documents', 'audio', 'video', 'archives', 'unknown']
    dst_doc = os.path.join(path_root, 'documents')
    dst_img = os.path.join(path_root, 'images')
    dst_aud = os.path.join(path_root, 'audio')
    dst_vid = os.path.join(path_root,'video')
    dst_arh = os.path.join(path_root,'archives')
    dst_un = os.path.join(path_root,'unknown')
 
    
    def creat_folder(path, new_folders):                # створюємо папки для сортування файлів
        global path_root, dst_doc, dst_img, dst_aud, dst_vid, dst_arh, dst_un
        path_root = path
        for el in new_folders:
            try:
                os.mkdir(path_root + '\\' + el)
            except FileExistsError:
                print("File already exists:", el)
        
    def normalize(name):                                 # заміна кирилиці на латиницю
        CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!#$%&()*+,-/:;<>=?@[]^~{|}'\\`. "
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
               "_", "_", "_","_","_","_", "_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_","_" )
        TRANS = {}
        CYRILLIC = tuple(CYRILLIC_SYMBOLS)
        
        for c, l in zip(CYRILLIC, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()
        
        s_res =  re.search('\..{2,5}$', name)
        suffix = s_res.group()
        name = name.removesuffix(suffix)
        name = name.translate(TRANS)
        name = name + suffix
        return name
      
    def move_file(files_patrn, path, el, dst):          #перемфщує відомі файлу у спеціальну теку
        
        for doc_patern in files_patrn:
            if re.search(doc_patern, el):
                new_el = normalize(el)       #змінюю назву файлу 
                src = os.path.join(path, el)
                dst = os.path.join(dst,new_el)
                print('Source standart file after normmalizing:', src)
                try:
                    shutil.copy(src, dst)
                    os.remove(src)
                    print("File is copied successfully.")
                except shutil.SameFileError:
                    print("Source and destination represents the same file.")
                except PermissionError:
                    print("Permission denied.")
                except:
                    print("Error occurred while copying file.", src)
                    
    def move_unknown_file(files_patrn, path, el, dst):   #перемфщує невідомі файлу у спеціальну папку
        for doc_patern in files_patrn:
            result_seach = re.search(doc_patern, el)
    
            if  re.search(doc_patern, el) == None:
                new_el = normalize(el)       #змінюю назву файлу 
                src = os.path.join(path, el)
                dst = os.path.join(dst,new_el)
                try:
                    shutil.copy(src, dst)
                    os.remove(src)
                    print("File is copied successfully.")
                except shutil.SameFileError:
                    print("Source and destination represents the same file.")
                except PermissionError:
                    print("Permission denied.")
                except:
                    print("Error occurred while copying file.")
    
    def delete_empty_folders(path):                     #видаляє порожні папки
        for el in os.listdir(path):
            if os.path.isdir(path + '\\' + el):
                try:
                    os.rmdir(path + '\\' + el)
                    # print("Directory '%s' has been removed successfully" %(path + '\\' + el))   
                    delete_empty_folders(path)
                except OSError:
                    # print("Directory '%s' can not be removed" %(path + '\\' + el))  
                    delete_empty_folders(path + '\\' + el) 
                  
    def decode_folder(dst_arh):                         #розпаковуємо архіви
        python_arch_list = ['\.zip$', '\.tar\.gz$', '\.tar\.bz2$', '\.tar\.xz$', '\.tar\.Z$', '.tar$' ]
        path = dst_arh
        arch_list = os.listdir(path)
        for arch in arch_list:
            if os.path.isdir(path + '\\' + arch) == False: # it is a file
                for arch_file in python_arch_list:          #find python's arch
                    s_res =  re.search(arch_file, arch)
                    if s_res:
                        suffix = s_res.group()
                        extract_folder = arch.removesuffix(suffix)
                        extract_dir = os.path.join(path, extract_folder)
                        try:
                            os.mkdir(extract_dir)
                            shutil.unpack_archive(path + '\\' + arch, extract_dir)
                            os.remove(path + '\\' + arch)
                        except FileExistsError:
                            print('File already existed')
    
    def rec_sort(path):                                 # сортуємо файли
        el_list = os.listdir(path)  
        for folder in new_folders:               # видаляємо стандартні папки з циклу
            for el in el_list:
                if folder == el:
                    el_list.remove(el) 
        for el in el_list:
            if os.path.isdir(path + '\\' + el) == False: #It is a file
                #move the file
                move_file(photo_files, path, el, dst_img)    
                move_file(video_files, path, el, dst_vid)
                move_file(doc_files, path, el, dst_doc)
                move_file(audio_files, path, el, dst_aud)
                move_file(arch_files, path, el, dst_arh)
                move_unknown_file(unknown_files, path, el, dst_un)     
            elif os.path.isdir(path + '\\' + el): # It is a folder
                rec_sort(path + '\\' + el)  
    
    # main program                        
    creat_folder(path, new_folders)            
    rec_sort(path)  
    delete_empty_folders(path)
    decode_folder(dst_arh)       
   
if __name__ == '__main__':
    if sys.argv[1]:
        path = sys.argv[1]
    else:
        print('The path is not found. You should input the path to the folder after the script name.')
    main(path)
    
    