# Note about job scheduling(Quartz)

Quartz is a java job scheduling library

It lets you run tasks(jobs) at a specific time, after a delay, or on a recurring schedule

# Benifit of Quartz

- Precision => Can run a job at exact date & time, not just "every X minutes"
- Persistence => jobs can be stored in db so they survie restarts
- Flexibility => supports cron expressions, one-time jobs, repeated jobs, delayed jobs
- Scalability => can run across multiple servers in a cluster

# Key concepts i Quartz

## 1. Scheduler

- The main engine that manages job and triggers
- Responsible for starting, stopping, and executing jobs
- Get it from `StdSchedulerFactory`(standalne) or Spring boot auto-config

```
Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
scheduler.start(); // start running jobs
```

## 2. Job

- A task you want to run
- Must implement `org.quartz.Job`
- Contains business logic(send an email, generate a report)

## 3. JobDetail

- Metadata that tells Quartz about a job
    - Which `Job` class to run
    - What data to pass(parameters)
    - The job's unique identity(name & group)

```
JobDetail jobDetail = JobBuilder.newJob(EmailJob.class)
    .withIdentity("emailJob", "notifications")
    .usingJobData("email", "user@example.com")
    .build();
```

## 4. Trigger

- Defines when and how often a job runs
- Types:
    - SumpleTrigger => Run once or repeate every X seconds/minutes
    - CronTrigger => Run based on a cron expression
    - CalendarIntervalTrigger => Run every X days/weeks/months

```
Trigger trigger = TriggerBuilder.newTrigger()
    .withIdentity("emailTrigger", "notifications")
    .startAt(new Date(System.currentTimeMillis() + 30 * 60 * 1000)) // 30 min later
    .build();
```

- Run once at a specific date

```
CronTrigger cronTrigger = TriggerBuilder.newTrigger()
    .withSchedule(CronScheduleBuilder.cronSchedule("0 0 9 * * ?"))
    .build();
```

- Run everyday at 9 Am

## 5. JobStore

- Where Quartz saves jobs, triggers, and execution history
- Types:
    - RAMJobStore => default, keeps everything in memory
    - JDBCJobStore => saves jobs to a database

Config in spring boot: `application.properties`

```
# In-memory (default, for testing)
spring.quartz.job-store-type=memory

# Persistent with DB
spring.quartz.job-store-type=jdbc
spring.quartz.jdbc.initialize-schema=always
```

## 6. Listener

- Allow you to react to Quartz events
- Types:
    - JobListener => Before/after a job executes
    - TriggerListener => Before/After a trigger fires
    - SchedulerListener => When jobs/triggers are added/removed

```
public class MyJobListener implements JobListener {
    @Override
    public String getName() { return "MyJobListener"; }

    @Override
    public void jobWasExecuted(JobExecutionContext context, JobExecutionException jobException) {
        System.out.println("Job completed: " + context.getJobDetail().getKey());
    }
}
```