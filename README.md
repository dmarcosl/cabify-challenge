My solution uses a back-end application, a front-end webpage, two data files for products and discounts and a file database for the baskets.

I have used a CSV file for the products and another for the discounts. It is the most simple and versatile way that I thought to manage the stock and discounts without an external database, and can be edited while the server is running.

To store the baskets I have used a Python shelve, to store them in a file with the structure of a dictionary (similar to json), in order to not lose the basket at refresh the page, change the browser or at stop the server.

For the back-end, I have created a REST API writen in Python3 using Flask, because Python comes with most UNIX operating systems, and with a couple of libraries you can have a simple REST API.

For the front-end, I have used a simple HTML and raw JS, to do not use a large amount of libraries and complicate things.

The project requires a simple setup, install the Flask libraries:

```
pip3 install -r requirements.txt
```

and execute it

```
python3 run.py
```

A simple description of each file:

- **run.py**: Flask setup
- **controllers.py**: Endpoints and operations
- **models.py**: Product and Discount classes
- **index.html**: Webpage
- **behavior.js**: JS scripts
- **styles.css**: CSS styles
- **products.csv** & **discounts.csv**: Data files