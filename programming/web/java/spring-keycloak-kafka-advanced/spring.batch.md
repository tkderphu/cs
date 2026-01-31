# Note about spring batch

Spring batch is used for processing large volumes of data in batches(intead of handling one by one in real-time)

Typical use cases:
- reading data from a file/database
- processing/converting it
- writting it to another file/db

Example: `Example: Read a CSV → Process → Write to Database`

Dependencies:

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-batch</artifactId>
</dependency>
```

# Some keyword in batch

- Job: A batcg process. It's the container for steps
- Step:  A phase of the job. A job can have multiple steps
- ItemReader: Reads data(from db, json, file)
- ItemProcessor: optional, used to transform, filter, or validate data before do something
- ItemWriter: writes data to the target(db, file, aoi)
- Chunk: the number of items processed before committing to db
- JobRepository: stores metadata about jobs in db
- RunIdIncrementer: helps run the same job multiple times by incrementing its ID
