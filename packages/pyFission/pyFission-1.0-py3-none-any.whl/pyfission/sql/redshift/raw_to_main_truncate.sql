TRUNCATE TABLE {schema}.{table}
;

INSERT INTO {schema}.{table}
SELECT * FROM {schema}.{table_raw}
;