BEGIN;

CREATE OR REPLACE VIEW mvg_avg AS (
    SELECT AVG(price) as price FROM (SELECT price FROM stock ORDER BY _time DESC LIMIT 10)
);

END;
