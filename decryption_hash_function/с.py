import hashlib
import os

# hashcat_file_path - путь до папки, в которой находится hashcat.exe
# sha1_file_path - путь до файла, из которой мы берем наши, захешированные с помощью sha1, номера 
# sha256_file_path - путь до файла, из которой мы берем наши, захешированные с помощью sha256, номера 
# output_file_path - путь до файла, из которой мы берем вывод, который получили после hashcat'a
# hashes_file_path - путь до файла, из которой мы берем начальный хэш
# potfile_file_path - путь до файла, который принимает весь вывод hashcat'a по дефолту
from config import hashcat_file_path, sha1_file_path, sha256_file_path, output_file_path, hashes_file_path, potfile_file_path

def get_salt_and_results():
    f = open("decryption_hash_function/txt_folder/given_numbers.txt") # Получаем 5 номеров, которые дали
    phones = []
    for i in f.read().split():
        phones.append(int(i))

    results = open("decryption_hash_function/txt_folder/output.txt").read().split()
    results = [int(i[-11:]) for i in results]
    for k in results:
        counter = 0
        salt = k-phones[0]
        for v in results:
            if v-salt in phones:
                counter +=1
        if counter == len(phones):
            break
    with open("decryption_hash_function/txt_folder/dehashed_given_hash.txt", 'w') as file:
        for item in results:
            file.write(f"{item - salt}\n")

def sha1(phones):
    phones_sha1 = [hashlib.sha1(phone.encode()).hexdigest() for phone in phones]
    with open('decryption_hash_function/txt_folder/sha1.txt', 'w') as f:
        for phone in phones_sha1:
            f.write(phone + '\n')

    #os.remove('hashcat.potfile')
    os.system(f'cd {hashcat_file_path} && hashcat -a 3 -m 100 -o output_sha1.txt "{sha1_file_path}" ?d?d?d?d?d?d?d?d?d?d?d')


def sha256(phones):
    phones_sha256 = [hashlib.sha256(phone.encode()).hexdigest() for phone in phones]
    with open('decryption_hash_function/txt_folder/sha256.txt', 'w') as f:
        for phone in phones_sha256:
            f.write(phone + '\n')

    #os.remove('hashcat.potfile')
    os.system(f'cd {hashcat_file_path} && hashcat -a 3 -m 1400 -o output_sha256.txt "{sha256_file_path}" ?d?d?d?d?d?d?d?d?d?d?d')
        
        
if __name__ == "__main__":
    os.remove(f"{potfile_file_path}")
    os.system(f'cd "{hashcat_file_path}" && hashcat -a 3 -m 0 -o "{output_file_path}" "{hashes_file_path}" ?d?d?d?d?d?d?d?d?d?d?d')
    #get_salt_and_results()
    with open(r'decryption_hash_function\txt_folder\output.txt') as r:
        phones = [line.strip()[33:] for line in r.readlines()] #Номера полученные после MD5
    sha1(phones) # 5 mins, 36 secs
    sha256(phones) # 6 mins, 15 secs
    