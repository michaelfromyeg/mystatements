def get_pdf_files_from_folder(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.pdf') and "TFSA" not in f]



if __name__ == "__main__":
  folder_path = '/mnt/c/Users/mdema/Documents/td'

  filenames = get_pdf_files_from_folder(folder_path)

  # Find missing days
  missing = find_missing_days(filenames)
