DELETE FROM `{project}.{dataset}.{table}`
WHERE EXISTS
(select * from `{project}.{dataset}.{table}_{guid}`
    WHERE {conditions}
)
;

INSERT INTO `{project}.{dataset}.{table}`
({columns_list})
SELECT
    {columns_list}
from `{project}.{dataset}.{table}_{guid}`
;

DROP TABLE IF EXISTS `{project}.{dataset}.{table}_{guid}`
;