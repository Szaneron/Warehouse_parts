from pymongo import MongoClient

# Configuration variables
mongo_url = "mongodb+srv://admin:admin@test0.kw6oixv.mongodb.net"
database_name = "armin_bolen"


# Function to initialize the database
def init_database():
    client = MongoClient(mongo_url)
    database = client[database_name]

    # Check if the 'categories' collection exists
    if 'categories' not in database.list_collection_names():
        # Create the 'categories' collection if it does not exist
        database.create_collection('categories')

        database.categories.insert_many([
            {"name": "Electronics", "parent_name": ""},
            {"name": "Resistors", "parent_name": "Electronics"},
            {"name": "Switches", "parent_name": "Electronics"}
        ])

    # Check if the 'parts' collection exists
    if 'parts' not in database.list_collection_names():
        # Create the 'parts' collection if it does not exist
        database.create_collection('parts')

        # Add sample data for 'categories' and 'parts'
        database.parts.insert_many([
            {
                "serial_number": "5904422305512",
                "name": "THT CF carbon resistor 1/4W 47kΩ - 30 pcs",
                "description": "Set of 30 1/4 W resistors. Elements in a THT housing.",
                "category": "Resistors",
                "quantity": 40,
                "price": 0.49,
                "location": {
                    "room": "A1",
                    "bookcase": "B2",
                    "shelf": "C3",
                    "cuvette": "D4",
                    "column": "1",
                    "row": "2"
                }
            },
            {
                "serial_number": "5904422374051",
                "name": "THT resistor RWA 10W 0.33 Ohm - 10 pcs",
                "description": "Precision resistor with high stability, RWA type, power of 10 W and resistance of 0.33 Ω. The price includes 10 pieces.",
                "category": "Resistors",
                "quantity": 70,
                "price": 2.99,
                "location": {
                    "room": "A1",
                    "bookcase": "B2",
                    "shelf": "C3",
                    "cuvette": "D3",
                    "column": "1",
                    "row": "3"
                }
            },
            {
                "serial_number": "5904422307622",
                "name": "Tact Switch 6x6mm / 4.3mm THT - 5 pcs",
                "description": "A small monostable button mounted through-hole - THT, size: 6x6 mm, height: 4.3 mm. Price for 5 pieces.",
                "category": "Switches",
                "quantity": 35,
                "price": 1.99,
                "location": {
                    "room": "A1",
                    "bookcase": "B4",
                    "shelf": "B2",
                    "cuvette": "D3",
                    "column": "1",
                    "row": "1"
                }
            },
            {
                "serial_number": "5904422304218",
                "name": "SS12T44 2-position slide switch - 5 pcs",
                "description": "Slide switch, straight for printing, dimensions 12.1 x 8.7 x 5.5 mm. Pin pitch 3.00 mm.",
                "category": "Switches",
                "quantity": 35,
                "price": 1.99,
                "location": {
                    "room": "A1",
                    "bookcase": "B4",
                    "shelf": "B2",
                    "cuvette": "D3",
                    "column": "1",
                    "row": "2"
                }
            },
            {
                "serial_number": "5904422373740",
                "name": "On-Off switch MK111 12V/20A - red",
                "description": "On-Off switch with built-in backlight. The contact load capacity is 12 V / 20 A.",
                "category": "Switches",
                "quantity": 20,
                "price": 0.30,
                "location": {
                    "room": "A1",
                    "bookcase": "B4",
                    "shelf": "B2",
                    "cuvette": "D3",
                    "column": "1",
                    "row": "3"
                }
            },
            {
                "serial_number": "5900804016427",
                "name": "On-Off switch MK111 12V/20A - green",
                "description": "On-Off switch with built-in backlight. The contact load capacity is 12 V / 20 A.",
                "category": "Switches",
                "quantity": 20,
                "price": 0.30,
                "location": {
                    "room": "A1",
                    "bookcase": "B4",
                    "shelf": "B2",
                    "cuvette": "D3",
                    "column": "1",
                    "row": "4"
                }
            },
        ])


print("Database initialization complete.")
