BEGIN;

CREATE MATERIALIZED VIEW symbols AS SELECT DISTINCT symbol FROM stock;

END;
