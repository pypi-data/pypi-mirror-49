COPY {schema}.{table}
FROM 's3://{bucketpath}'
CREDENTIALS 'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'
json 'auto'
GZIP
ACCEPTINVCHARS
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
;