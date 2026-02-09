import requests
import os

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'static/images/{filename}', 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

images = [
    ("https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=800&q=80", "luxury_suite.jpg"),
    ("https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80", "standard_double.jpg"),
    ("https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80", "economy_single.jpg")
]

def main():
    if not os.path.exists('static/images'):
        os.makedirs('static/images')

    for url, filename in images:
        download_image(url, filename)

if __name__ == '__main__':
    main()
