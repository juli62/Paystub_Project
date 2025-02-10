# API to turn a CSV file into a PDF and email it to clients


## Build docker 
```bash
docker build -t paystub-api .
```

## Run docker
```bash
docker run -p 8000:8000 -it paystub-api
```
> Run this commmand inside the directory that has the csv.
```bash
curl -X POST "http://127.0.0.1:8000/process/?country=DO&credentials=AtDev+AtDev123&company=abba" -F "file=@paystub1.csv"
```


### Preview of the Paystub
###
<p align="center">
  
<img src="https://github.com/user-attachments/assets/696d39fe-f0b1-4abd-94e1-a61b8218e1cf" /> 
</p>
