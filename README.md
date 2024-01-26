# Warehouse_parts

Projekt to proste RestAPI przeznaczone do zarządzania Magazynem Części, który przechowuje drobne części elektroniczne wykorzystywane w warsztatach naprawczych. 
API jest zbudowane przy użyciu Pythona i FastAPI i jest połączone z bazą danych MongoDB. Celem jest zapewnienie funkcjonalności CRUD dla dwóch głównych kolekcji: „części” i „kategorie”, wraz z dodatkowym punktem końcowym do wyszukiwania w kolekcji „części”.

## Uzasadnienie Wyboru FastAPI:
FastAPI został wybrany ze względu na swoją wydajność, prostotę użycia, a także wbudowane wsparcie dla typów danych i automatyczne generowanie dokumentacji API. 
FastAPI wykorzystuje typowanie statyczne, co zwiększa bezpieczeństwo kodu i ułatwia jego utrzymanie.


- Proponuję odwiedzić **Endpoint:** **`/docs/`** pod którym znajduje się automatyczna dokumentacja wszystkich endpointów. Jest bardzo przyjrzysta i umożliwia testowanie wszystkich endpointów z jendego miejsca.


## Uruchamianie Aplikacji

### Pierwszy sposób - Docker

1. **Zainstaluj Docker:** 

2. **Pobierz Obraz z Docker Hub:**

    ```bash
    docker pull szaneron/warehouse_api:final
    ```

3. **Uruchom Aplikację: (ważne aby przekazać zmienną środowiskową "MongoDb connection string")**

    ```bash
    docker run -p 8000:80 -e MONGO_URL="recruitment_mongo_connection_string" szaneron/warehouse_api:final
    ```

    Aplikacja będzie dostępna pod adresem [http://localhost:8000/](http://localhost:8000/).

    Upewnij się, że ustawiasz poprawną wartość zmiennej środowiskowej MONGO_URL, która przechowuje klucz do połączenia z bazą danych MongoDB.

### Drugi sposób - Lokalnie

1. **Pobierz Repozytorium:** 

    ```bash
    git clone https://github.com/Szaneron/Warehouse_parts.git
    ```

    Przejdź do folderu projektu:
   
    ```bash
    cd Warehouse_parts
    ```
2. **Zainstaluj Zależności:**
   
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Ustaw Zmienną Środowiskową:**

    Ustaw zmienną środowiskową MONGO_URL, która przechowuje klucz do połączenia z bazą danych MongoDB

    ```bash
    export MONGO_URL="your_mongo_connection_string"
    ```
    
    W przypadku systemów Windows możesz użyć:
   ```bash
   set MONGO_URL="your_mongo_connection_string"
   ```
   
4. **Uruchom Aplikację:**

   ```bash
   uvicorn api:app --reload  
   ```
   Aplikacja będzie dostępna pod adresem http://localhost:8000/.

## Wybór frameworka
FastAPI został wybrany ze względu na swoją wydajność, prostotę użycia, a także wbudowane wsparcie dla typów danych i automatyczne generowanie dokumentacji API. 
FastAPI wykorzystuje typowanie statyczne, co zwiększa bezpieczeństwo kodu i ułatwia jego utrzymanie.


  
## Endpointy
### 0. Dokumentacja API
- **Endpoint:** `/docs/`
- **Opis:** Automatyczna dokumentacja wszystkich endpointów. Przyjrzysta i umożliwia testowanie wszystkich endpointów z jendego miejsca.
  
### 1. Lista Wszystkich Kategorii

- **Endpoint:** `/categories/`
- **Metoda HTTP:** GET
- **Opis:** Pobiera listę wszystkich kategorii.

### 2. Pobierz Kategorię o Określonym ID

- **Endpoint:** `/categories/{category_id}`
- **Metoda HTTP:** GET
- **Opis:** Pobiera informacje o kategorii na podstawie podanego ID.

### 3. Dodaj Nową Kategorię

- **Endpoint:** `/categories/`
- **Metoda HTTP:** POST
- **Opis:** Dodaje nową kategorię.
- **Ciało Zapytania:** JSON z polami `name` i `parent_name`.

### 4. Aktualizuj Kategorię

- **Endpoint:** `/categories/{category_id}`
- **Metoda HTTP:** PUT
- **Opis:** Aktualizuje istniejącą kategorię na podstawie podanego ID.
- **Ciało Zapytania:** JSON z polami `name` i `parent_name`.

### 5. Usuń Kategorię

- **Endpoint:** `/categories/{category_id}`
- **Metoda HTTP:** DELETE
- **Opis:** Usuwa kategorię na podstawie podanego ID.

### 6. Lista Wszystkich Części

- **Endpoint:** `/parts/`
- **Metoda HTTP:** GET
- **Opis:** Pobiera listę wszystkich części.

### 7. Pobierz Część o Określonym ID

- **Endpoint:** `/parts/{part_id}`
- **Metoda HTTP:** GET
- **Opis:** Pobiera informacje o części na podstawie podanego ID.

### 8. Dodaj Nową Część

- **Endpoint:** `/parts/`
- **Metoda HTTP:** POST
- **Opis:** Dodaje nową część.
- **Ciało Zapytania:** JSON z polami `serial_number`, `name`, `description`, `category`, `quantity`, `price`, `location`.

### 9. Aktualizuj Część

- **Endpoint:** `/parts/{part_id}`
- **Metoda HTTP:** PUT
- **Opis:** Aktualizuje istniejącą część na podstawie podanego ID.
- **Ciało Zapytania:** JSON z polami `serial_number`, `name`, `description`, `category`, `quantity`, `price`, `location`.

### 10. Usuń Część

- **Endpoint:** `/parts/{part_id}`
- **Metoda HTTP:** DELETE
- **Opis:** Usuwa część na podstawie podanego ID.

### 11. Wyszukaj Części

- **Endpoint:** `/parts/search/`
- **Metoda HTTP:** GET
- **Opis:** Wyszukuje części na podstawie różnych kryteriów.


## Wymagania
- **Python 3.7+**
- **FastAPI** (wersja 0.109.0)
- **Motor** (wersja 2.5.3)
- **PyMongo** (wersja 4.6.1)
- **Pydantic** (wersja 2.5.3)
- **Python-dotenv** (wersja 1.0.1)

## Inne Informacje

W przypadku gdyby baza danych nie tworzyła się poprawnie, należy usunąć bazę danych "armin_bolen". Udostępnione konto nie posiada takich uprwanień. Wtedy nie powinno być żadnego problemu przy ponownym uruchomieniu aplikacji.

