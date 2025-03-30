import nltk

# Show downloaded packages
nltk.download('all') # This will download everything that has not been downloaded.
nltk.download() # This will open the downloader.
# or
# print("Downloaded Packages:")
# for package in nltk.downloader.Downloader().packages():
#     if package.status == 1: # 1 means downloaded.
#         print(f"- {package.id}")

# # Show downloaded corpora (similar approach)
# print("\nDownloaded Corpora:")
# for corpus in nltk.downloader.Downloader().corpora():
#     if corpus.status == 1:
#         print(f"- {corpus.id}")