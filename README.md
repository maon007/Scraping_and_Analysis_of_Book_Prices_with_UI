# BookBot project
Scraping data from AbeBooks website.

## Project Description

Část.1: Zisk cen knih
1. Na stránce prodejce Bookbot (https://www.abebooks.de/Bookbot-Prag/87044093/sf)
chceme vybrat 1000 nejdražších knih, které mají zároveň uvedeno ISBN13.
2. Tato ISBN následně chceme na webu abebooks vyhledat. Od každého prodejce
chceme nejvýše jednu nabídku (pokud některý prodejce nabízí stejnou knihu
vícekrát, zvolíme nejlevnější).
3. Výstup bude .csv se sloupci isbn, title, název obchodu 1, název obchodu 2...

Část.2: Základní statistiky
4. Spočítejte, jak často je Bookbot jediným prodávajícím.
5. Zjistěte, jak často je cena od Bookbota mezi 25% nejlevnějšími a nejdražšími
nabídkami.
6. Identifikujte prodejce, kteří mají častěji nižší cenu než BookBot.
7. Vypočítejte průměrnou odchylku nabídek Bookotu od nejnižší ceny.
8. Analyzujte relativní zastoupení nabídek ze zahraničí ve stažených datech.

## Attached files
- **bookbot_scraping.py**: This script scraping data from AbeBooks website.
- **bookbot_statistics.py**: This script calculates statistics.
- **app.py**: Front-end script.
- **Bookbot_statistics.ipynb**: Notebook with the test data to test correctness of statistics.
- **Dockerfile**: This file contains instructions for building your Docker image.
- **requirements.txt**: This file contains all the Python libraries your Streamlit app depends on.
- **1000_ISBNs_all.csv**: This file contains the first 1000 books (all offers) ordered from the most expensive.
- **1000_ISBNs_cheapest_variant.csv**: This file contains the first 1000 books but just the cheapest offer.

## Start the Application

### Directly (using streamlit library)
First, make sure you have Streamlit and Pandas installed (e.g. pip install streamlit). 
To run the app, navigate to the directory containing the script in your terminal and run:
```python
streamlit run app.py
```

### Using a Dockerfile
You can also use a Dockerfile to build the image for the scraper script. Open a terminal and navigate to the directory containing your Dockerfile and Streamlit app files.
Build the image using the following command:
```bash
docker build -t my_streamlit_app .
```
You can replace "my_streamlit_app" with the desired name for your Docker image.

Run the Docker container: Once the image is built, you can run it as a container:
```bash
docker run -p 8501:8501 my_streamlit_app
```

This command maps port 8501 of your local machine to port 8501 inside the container, where Streamlit is running.

Access your Streamlit app: Open a web browser and go to http://localhost:8501 to access your Streamlit app running inside the Docker container.



