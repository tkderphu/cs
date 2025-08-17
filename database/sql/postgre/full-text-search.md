# Note about fulltext search

Fulltext search it's used for search large text documents;

# Components of full-text-search in postgres

| Component        | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `to_tsvector`    | Converts text to a searchable document format (a vector of lexemes). Ex we has this sentence: 'quang and phu' then using `to_tsvector` => phu: 2, quang: 3    |
| `to_tsquery`     | Converts a search phrase into a query that can match against `tsvector`. |
| `tsvector`       | A data type that stores normalized, searchable text (used in indexing).  |
| `tsquery`        | A data type for representing parsed search queries (can include logic).  |
| `GIN/GiST index` | Indexes on `tsvector` columns to speed up searches.                      |
| Dictionaries     | Define how words are broken down and normalized (e.g., stemming).        |
| Configurations   | Tie together tokenizers, dictionaries, and stopwords for parsing text.   |

# 2. How it works

- Example: Search the phrase 'jumped fox' in an article.

## Step 1: Normalize the Document

Use to_tsvector:

```
SELECT to_tsvector('english', 'The quick brown fox jumped over the lazy dog');
```

Output:

```
'brown':3 'dog':9 'fox':4 'jump':5 'lazi':8 'quick':2 'the':1,6,7
```

### Notes:

- First parameter is a language used for parsing sentence in here we are using english

- Words are lowercased and stemmed (jumped → jump, lazy → lazi).

- Positions of words are stored ('fox':4 means "fox" was the 4th word).

- Stop words (e.g., "over", "the") may be removed depending on config.

## Step 2: Parse the Search Query

```
SELECT to_tsquery('english', 'jumped & fox');
```

Output:

```
'jump' & 'fox'
```

## Step 3: Match Query to Document

```
SELECT to_tsvector('english', 'The quick brown fox jumped over the lazy dog') @@ to_tsquery('english', 'jumped & fox');
```

Output:

```
true
```

This tells you that both word jumped and for exists in the sentence.

# 3. Ranking Search Results

Use `ts_rank` or `ts_rank_cd` to score relavance:

```
SELECT ts_rank(to_tsvector('english', body), to_tsquery('english', 'fox & jump')) AS rank
FROM articles
WHERE to_tsvector('english', body) @@ to_tsquery('english', 'fox & jump');
```

- Higher ranks is more relavant result

# 4.Index for performance

Index the tsvector to improve performance of query:


```
-- Option 1: Add a generated column
ALTER TABLE articles ADD COLUMN tsv tsvector
    GENERATED ALWAYS AS (to_tsvector('english', body)) STORED;

-- Then index it
CREATE INDEX idx_fts_body ON articles USING GIN(tsv);
```

## 4.1: What is GIN index

- GIN stands for Generalized Inverted Index.

- It’s designed to index composite data types like tsvector, jsonb, array, etc.

### In the fulltext search 

When you use `to_tsvector('english', text)` then it will return data type tsvector

#### A GIN index stores an inverted index like this:

word → list of documents containing the word

Ex: Think of GIN like a reverse map of terms (lexemes) to physical rows (TIDs):


```
Lexeme     →      TIDs (tuple IDs)
-------------------------------
'quick'    →      (1,2)
'fox'      →      (1,2)
'dog'      →      (1,3)
'hello'    →      (4)
'smart'    →      (2)
'jump'     →      (1)
'running'  →      (3)
```

# 5. Highlighting and Stemming

Highlight (show match in context):

```
SELECT ts_headline('english', body, to_tsquery('english', 'jump & fox'))
FROM articles;
```

This shows the sentence with matched terms highlighted using `  <b/>` tags by default.

## 5.1 Stemming:

Part of the dictionary config — it reduces words to root form:

- jumping, jumped, jumps → jump

- Done using dictionaries like english_stem, controlled by text search configuration

# 6. Dictionary & Configuration System

PostgreSQL uses Text Search Configuration that defines:

- Parser: Breaks text into tokens

- Dictionaries: Normalize/stem tokens

- Stopwords: Common words to ignore

List available configurations:

```
SELECT * FROM pg_ts_config;
```

Inspect a configuration:

```
SELECT * FROM ts_debug('english', 'The foxes were jumping');
```


# 7. Search with no accent

## 1. Enable unaccent extension

```
CREATE EXTENSION IF NOT EXISTS unaccent;
```

`Use this`:

```
unaccent(text 'Nguyễn Quang Phú')
```

## Example:

```
SELECT to_tsvector('simpple', unaccent('Nguyễn Quang Phú'));

#result:

'Phu':3 'Quang':2 'Nguyen':1
```

# 8. How to use this in `tsvector` column

```
ALTER TABLE users
ADD COLUMN fts_name_unaccent tsvector
GENERATED ALWAYS AS (
  to_tsvector('simple', unaccent(full_name))
) STORED; #auto update when full_name update

CREATE INDEX idx_fts_name_unaccent ON users USING GIN(fts_name_unaccent);
```