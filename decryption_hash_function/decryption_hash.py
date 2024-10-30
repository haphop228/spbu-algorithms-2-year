import hashlib
import os
import time

### Абсолютные пути

##
# hashcat_file_path - путь до папки, в которой находится hashcat.exe

## ПУТИ ДО ФАЙЛОВ, ИЗ КОТОРЫХ МЫ БЕРЕМ НАШИ, ЗАХЕШИРОВАННЫЕ С ПОМОЩЬЮ N АЛГОРИТМА, НОМЕРА 
# sha1_file_path
# sha256_file_pathъ
# md5_file_path


# output_file_path - путь до файла, из которой мы берем вывод, который получили после hashcat'a
# output_md5_file_path - путь до файла, из которой мы берем вывод, который получили после hashcat'a
# output_sha1_file_path - путь до файла, из которой мы берем вывод, который получили после hashcat'a
# output_sha256_file_path - путь до файла, из которой мы берем вывод, который получили после hashcat'a
# hashes_file_path - путь до файла, из которой мы берем начальный хэш

from config import (hashcat_file_path, sha1_file_path, sha256_file_path,
                    output_file_path, output_md5_file_path, output_sha1_file_path,
                    md5_file_path, output_sha256_file_path, hashes_file_path)


# salt = 41224301
def find_salt():
    with open("decryption_hash_function/txt_folder/output.txt", "r", encoding="utf-8") as output_file:
        d = dict()
        given_numbers_file = open("decryption_hash_function/txt_folder/given_numbers.txt") # Получаем 5 номеров, которые дали
        phones = []
        for i in given_numbers_file.read().split():
            phones.append(int(i))

        for el in output_file:
            el = el.split(":")[-1]
            for i in range(5):
                if (int(el) - phones[i]) not in d.keys():
                    d[(int(el) - phones[i])] = 1
                else:
                    d[(int(el) - phones[i])] += 1
        for key, value in d.items():
            if value >= 5:
                salt = key
                return salt


def put_correct_phones_into_file(salt: int):
    with open('decryption_hash_function/txt_folder/dehashed_given_hash.txt', "w", encoding="utf-8") as dehashed_given_hash_file:
        tmp_list = list()
        with open("decryption_hash_function/txt_folder/output.txt", "r", encoding="utf-8") as output_file:
            for el in output_file:
                el = int(el.split(":")[-1])
                tmp_list.append(str(el - salt))
        s = "\n".join(tmp_list)
        dehashed_given_hash_file.write(s)


def hash_sha1(correct_phones_file, salt: int):
    with open('decryption_hash_function/txt_folder/sha1.txt', 'w', encoding='utf-8') as sha1:
        correct_phones_file = open(correct_phones_file, "r", encoding="utf-8")
        for el in correct_phones_file:
            el = int(el.split(":")[-1])
            string = str(el + salt)
            sha1.write(str(hashlib.sha1(string.encode()).hexdigest()) + "\n")
        print("done")


def hash_sha256(correct_phones_file, salt: int):
    with open('decryption_hash_function/txt_folder/sha256.txt', 'w', encoding='utf-8') as sha256:
        correct_phones_file = open(correct_phones_file, "r", encoding="utf-8")
        for el in correct_phones_file:
            el = int(el.split(":")[-1])
            string = str(el + salt)
            sha256.write(str(hashlib.sha256(string.encode()).hexdigest()) + "\n")
        print("done")


def hash_md5(correct_phones_file, salt: int):
    with open('decryption_hash_function/txt_folder/md5.txt', "w", encoding="utf-8") as md5:
        correct_phones_file = open(correct_phones_file, "r", encoding="utf-8")
        for el in correct_phones_file:
            el = int(el.split(":")[-1])
            string = str(el + salt)
            md5.write(str(hashlib.md5(string.encode()).hexdigest()) + "\n")
        print("done")


def get_time_hashcat(output_file_path, hashes_file_path, hash_algorithm):
    start_time = time.time()
    os.system(f'cd "{hashcat_file_path}" && hashcat -a 3 -m {hash_algorithm} -o "{output_file_path}" "{hashes_file_path}" ?d?d?d?d?d?d?d?d?d?d?d --potfile-disable')
    end_time = time.time()
    return round(end_time - start_time, 2)


def main():
    md5_flag = 0 # флаг для MD-5 в hashcat
    sha1_flag = 100 # флаг для SHA-1 в hashcat
    sha256_flag = 1400 # флаг для SHA-256 в hashcat
    
    salt = find_salt()
    print(salt)
    put_correct_phones_into_file(salt)
    
    correct_phones_file = "decryption_hash_function/txt_folder/dehashed_given_hash.txt"
    time_md5 = get_time_hashcat(output_file_path, hashes_file_path, md5_flag)
    
    salt = find_salt()
    print(salt)
    put_correct_phones_into_file(salt)
    
    correct_phones_file = "decryption_hash_function/txt_folder/dehashed_given_hash.txt"
    
    hash_sha1(correct_phones_file, salt)
    hash_sha256(correct_phones_file, salt)
    
    time_sha1 = get_time_hashcat(output_sha1_file_path, sha1_file_path, sha1_flag)
    print("done_sha1")
    time_sha256 = get_time_hashcat(output_sha256_file_path, sha256_file_path, sha256_flag)
    print("done_sha256")
    
    print(
        f"время для md5: {time_md5}\nвремя для sha1: {time_sha1}\nвремя для sha256:{time_sha256}"
    )
    
    
    for salt in {
        1,
        11,
        111,
        1111,
        11111,
        111111,
        1111111,
        11111111,
        111111111,
        1111111111,
    }:
        hash_md5(correct_phones_file, salt)
        hash_sha1(correct_phones_file, salt)
        hash_sha256(correct_phones_file, salt)
        
        time_md5 = get_time_hashcat(output_md5_file_path, md5_file_path, md5_flag)
        time_sha1 = get_time_hashcat(output_sha1_file_path, sha1_file_path, sha1_flag)
        time_sha256 = get_time_hashcat(output_sha256_file_path, sha256_file_path, sha256_flag)
        
        print(
            f"При соли длинны {len(str(salt))}\nвремя для md5: {time_md5}\nвремя для sha1: {time_sha1}\nвремя для sha256:{time_sha256}"
        )
    
    

if __name__ == "__main__":
    main()