docker build . -t mysql_udf
docker run -p 3308:3308 -d mysql_udf