from django.db import migrations


CREATE_EXTENSION_SQL = 'CREATE EXTENSION IF NOT EXISTS ltree;'
DROP_EXTENSION_SQL = 'DROP EXTENSION IF EXISTS ltree;'

# Function to transform ltree to an array of strings.
# Delimiter - is the default delimiter `.` as in ltree.
CREATE_LTREE_TO_ARRAY_FUNCTION_SQL = [
    '''--sql
    -- Splitting ltree by path separator(.)
    CREATE OR REPLACE FUNCTION ltree2array(item ltree) RETURNS text[] AS
    $BODY$
        SELECT string_to_array(ltree2text(item), '.')
    $BODY$
    LANGUAGE SQL;
    ''',

    '''--sql
    -- Splitting text as ltree
    CREATE OR REPLACE FUNCTION ltree2array(item text) RETURNS text[] AS
    $BODY$
        SELECT string_to_array(item, '.')
    $BODY$
    LANGUAGE SQL;
    '''
]
DROP_LTREE_TO_ARRAY_FUNCTION_SQL = 'DROP FUNCTION IF EXISTS ltree2array;'

# Function to transform array of strings to ltree.
# Delimiter - is the default delimiter `.` as in ltree.
CREATE_ARRAY_TO_LTREE_FUNCTION_SQL = '''--sql
-- Splitting ltree by path separator(.)
CREATE OR REPLACE FUNCTION array2ltree(item text[]) RETURNS ltree AS
$BODY$
    SELECT text2ltree(array_to_string(item, '.'))
$BODY$
LANGUAGE SQL;
'''

DROP_ARRAY_TO_LTREE_FUNCTION_SQL = 'DROP FUNCTION IF EXISTS array2ltree;'

# Function to `unnest(item ltree)` into a containing elements.
CREATE_LTREE_UNNEST_FUNCTION_SQL = '''--sql
-- Splitting ltree by path separator(.)
CREATE OR REPLACE FUNCTION unnest(item ltree) RETURNS SETOF text AS
$BODY$
BEGIN
    RETURN QUERY SELECT unnest(ltree2array(item));
    RETURN;
END;
$BODY$
LANGUAGE plpgsql;
'''
DROP_LTREE_UNNEST_FUNCTION_SQL = 'DROP FUNCTION IF EXISTS unnest(ltree);'


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunSQL(CREATE_EXTENSION_SQL, DROP_EXTENSION_SQL),
        migrations.RunSQL(
            CREATE_LTREE_TO_ARRAY_FUNCTION_SQL,
            DROP_LTREE_TO_ARRAY_FUNCTION_SQL,
        ),
        migrations.RunSQL(
            CREATE_ARRAY_TO_LTREE_FUNCTION_SQL,
            DROP_ARRAY_TO_LTREE_FUNCTION_SQL,
        ),
        migrations.RunSQL(
            CREATE_LTREE_UNNEST_FUNCTION_SQL,
            DROP_LTREE_UNNEST_FUNCTION_SQL,
        ),
    ]
