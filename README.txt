===============
pglog2sql
===============

Convert portion of PostgreSQL log taken with the
log_min_duration_statement option into prepared statement ready to be
explain/analyze.

The log to analyze must contain "execute" and "DETAIL: parameters" infos.

If it is a multi line log you need to remove the log hearders (timestamp
and db information).

pglog2sql tries to guess the parameters type, so far only text, text[]
and integer are take in account.


:: 

  echo "LOG:  duration: 825.000 ms  execute <unnamed>: SELECT "hier"."id" AS "_C1" FROM "hier" LEFT JOIN "misc" ON "hier"."id" = "misc"."id" LEFT JOIN "core" ON "hier"."id" = "core"."id" LEFT JOIN "vers" ON "hier"."id" = "vers"."id" WHERE "hier"."primarytype" IN ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15) AND (EXISTS (SELECT 1 FROM "dc_contributors" WHERE "hier"."id" = "dc_contributors"."id" AND ("dc_contributors"."item" = $16))) AND ("vers"."id" IS NULL) AND ("misc"."lifecyclestate" <> $17) AND ("hier"."name" <> $18) ORDER BY "core"."modified" DESC 
  DETAIL:  parameters: $1 = 'MailMessage', $2 = 'ContextualLink', $3 = 'DocumentLink', $4 = 'Thread', $5 = 'search_results', $6 = 'AdministrativeStatus', $7 = 'Picture', $8 = 'Document', $9 = 'FacetedSearch', $10 = 'File', $11 = 'AdvancedSearch', $12 = 'FacetedSearchDefault', $13 = 'Note', $14 = 'QueryNav', $15 = 'BlogPost', $16 = 'Administrator', $17 = 'deleted', $18 = '/default'" \
    | pgsql2log

  DEALLOCATE foo;

  PREPARE foo(text, text, text, text, text, text, text, text, text, text, text, text, text, text, text, text, text, text) AS
  SELECT hier.id AS _C1 FROM hier LEFT JOIN misc ON hier.id = misc.id LEFT JOIN core ON hier.id = core.id LEFT JOIN vers ON hier.id = vers.id WHERE hier.primarytype IN (, , , , , , , , , 0, 1, 2, 3, 4, 5) AND (EXISTS (SELECT 1 FROM dc_contributors WHERE hier.id = dc_contributors.id AND (dc_contributors.item = 6))) AND (vers.id IS NULL) AND (misc.lifecyclestate <> 7) AND (hier.name <> 8) ORDER BY core.modified DESC;

  EXPLAIN ANALYZE EXECUTE foo('MailMessage', 'ContextualLink', 'DocumentLink', 'Thread', 'search_results', 'AdministrativeStatus', 'Picture', 'Document', 'FacetedSearch', 'File', 'AdvancedSearch', 'FacetedSearchDefault', 'Note', 'QueryNav', 'BlogPost', 'Administrator', 'deleted', '/default');



Install
---------
::
   
  sudo make install

