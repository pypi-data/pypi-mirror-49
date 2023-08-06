DELETE FROM {schema}.{table}
USING {schema}.{table}_{guid}
WHERE {primarykeyjoins}
;

INSERT INTO {schema}.{table}
SELECT distinct * FROM {schema}.{table}_{guid}
;