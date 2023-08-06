DELETE FROM `{project}.{dataset}.{table}` m
WHERE {not_condition} EXISTS ({subquery});