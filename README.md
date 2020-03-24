# Description
Hi, this is the first project i played with Flask. The purpose are check the SSL Certificate, and get the 2 field "not Before" and "notAfter", then i can know when the domain will be expire.
This project is very simple functions, and i did not do more advanced, just for my testing with flask RESTFul

# What did i do?
- I used "flask_api" library, here is http://www.flaskapi.org/ (i can use current flask, but i dont have time to create a Web GUI)
- Use "concurrent.futures" to improve the performance
- Custome some logging for more futher
- CRUD: GET, POST, PUT and UPDATE

# Import domain
- content type header: application/x-www-form-urlencoded"
```shell
for i in `cat example_domain.txt`; do curl -XPOST -H "Content-Type: application/x-www-form-urlencoded" -d "domain_name=$i" http://127.0.0.1:5000/api/v1/domains/; done 
```
- content type header: application/json
```shell
curl -XPOST -H "Content-Type: application/json" -d "{'domain_name': 'github.com'}" http://127.0.0.1:5000/api/v1/domains/
```

# Get all
![alt text](https://github.com/hungdnv9/ssl-certificate-check-restfullAPI/blob/master/images/get_all.png)
# Get by ID
![alt text](https://github.com/hungdnv9/ssl-certificate-check-restfullAPI/blob/master/images/get_by_id.png)
# Update
![alt text](https://github.com/hungdnv9/ssl-certificate-check-restfullAPI/blob/master/images/update.png)
