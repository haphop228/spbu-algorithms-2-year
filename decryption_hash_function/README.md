# Исследование хеш-функций с различными вводными условиями

## Для использования программы
1. Необходимо установить [hashcat](https://hashcat.net/hashcat/).  
Перейдите по ссылке и скачайте *hashcat binaries*, затем распакуйте архив в удобную для Вас папку.
2. Теперь откройте *.xlsx* файл полученный от преподавателя. Скопируйте первый столбец, без первой ячейки, в файл *hashes.txt*.
А третий столбец в файл *given_numbers.txt*.
3. Создайте файл *config.py* в основной директории(там же, где и *decryption_hash.py*) и добавьте туда следующие переменные:
    - *hashcat_file_path*
    - *md5_file_path*
    - *sha1_file_path*
    - *sha256_file_path*
    - *output_file_path*
    - *hashes_file_path*
    - *potfile_file_path*
    - *output_md5_file_path*
    - *output_sha1_file_path*
    - *output_sha256_file_path*
