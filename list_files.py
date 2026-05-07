import os

def gabung_semua_file_rekursif():
    root_dir = os.getcwd()
    output_file = "gabungan_semua_source_code.txt"
    
    # Daftar ekstensi yang ingin diambil (biar file gambar/binary gak ikut)
    valid_extensions = ('.ts', '.js', '.json', '.py', '.md', '.txt', '.yml', '.yaml')
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        # os.walk akan menelusuri semua folder dan sub-folder secara otomatis
        for root, dirs, files in os.walk(root_dir):
            for filename in files:
                # Hindari file output sendiri dan file binary
                if filename == output_file or filename == os.path.basename(__file__):
                    continue
                
                # Cek apakah file termasuk kode/teks berdasarkan ekstensi
                if filename.endswith(valid_extensions):
                    file_path = os.path.join(root, filename)
                    
                    # Mendapatkan path relatif untuk header di txt agar rapi
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            outfile.write(f"\n{'='*30}\n")
                            outfile.write(f"PATH: {relative_path}\n")
                            outfile.write(f"{'='*30}\n\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                    except Exception as e:
                        outfile.write(f"\n[Gagal membaca {relative_path}: {e}]\n")

    print(f"Selesai! Seluruh kode dari sub-folder telah digabung ke: {output_file}")

if __name__ == "__main__":
    gabung_semua_file_rekursif()