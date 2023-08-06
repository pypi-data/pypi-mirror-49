# PyPGQueue


#### A job queue built on PostgreSQL's listen/notify functionality

PyPGQueue is a simple job queue that uses PostgreSQL's listen/notify functionality, featuring job prioritizaion and serialization.


### PyPGQueue Features


#### Serialization

Job serialization allows you to ensure that for a set of jobs, only one of them is running at a give time. For instance if you need one job to run only after another job is finished, you can give them the same prioritization and the same serialization key, and whichever was created first will be run first, and only when it is done will another job with the same serialization key be able to run.


#### Prioritization

Jobs are started in FIFO order, however you can bump jobs up higher in the queue by assigning them a higher prioritization value.


#### Why build another job queue?

I initially started PyPGQueue for three reasons:

1. I had very simple job queuing needs
2. I needed first-class job serialization
3. I didn't want to add new dependencies to the project I was working on at the time
4. I wanted to play with Postgres' listen/notify features


#### Postgres version

PyPGQueue expects a version of PostgreSQL that has a JSONB data type and the json_build_object function, which were both added in version 9.4. These are just conveniences, and the DDL could be altered to work with text types, if you're stuck on a version of Postgres older than 9.4. The payload is passed directly to the job handler functions, so the Queue code itself also does not rely on the database supporting JSON types.

If you want to use multiple queues on the same schema, you need 9.5+ to use the row_lock cooperative mode. See "Running Multiple Queues on One Schema" below for more details.


### Install

    pip install pypgqueue


### Build the Database

    createdb pypgq
    python3 -m pypgq schema | psql pypgq


### Run Tests

    python3 -m tests -h


### Queue a Job From Code

    from bidon.db.access import ModelAccess
    from bidon.db.core import get_pg_core
    from pypgq import queue_job

    ma = ModelAccess(get_pg_core("dbname=pypgq")).open(autocommit=True)
    job_name = "A job"
    job_payload = {"arg0": "val0", "arg1": "val1"}
    serialization_key = "key"

    queue_job(ma, job_name, job_payload, serialization_key, priority=10)


### Queue a Job From PSQL

    insert into jobs (name, payload) values('A job', '{"arg0": "val0", "arg1": "val1"}');


### Run a Queue

A job queue can be created and configured by calling the pypgq module with the -m flag and providing some command line arguments:

    python3 -m pypgq start -c "dbname=pypgq" -w 5 -f /path/to/job-assignment-script.py

The -f option is the job assignment script, which needs to implement a top-level `setup_jobs` method that accepts two arguments: a pypgq.Queue instance and a string argument. See [tests/run_sample.py](tests/run_sample.py) for a working eample.

You can also daemonize a queue by specifying a pid file and telling the shell to run the queue in the background, e.g.:

    python3 -m pypgq start -c "dbname=pypgq" -w 5 -f job-script.py -p /tmp/pypgq.pid &

See `python3 -m pypgq start -h` for more details.


### Query a Queue

You can query a queue's status by sending the SIGINFO signal to it:

    kill -INFO pid

If you started the queue with a -p option, you can query it with:

    python3 -m pypgq status -p /path/to/pidfile

See `python3 -m pypgq status -h` for more details.

This will write the queue's status to STDERR of the queue's process, not the
calling process.


### Stop a Queue

Queues started via `python3 -m pypgq start ...` can be stopped gracefully with signals. See the log output from the queue for command samples that include the PID.

    kill -HUP pid #stops the queue when there are no more waiting jobs
    kill -INT pid #stops the queue when the currently running jobs are done
    kill -TERM pid #cancels all running jobs and stops the queue asap

If you started the queue with a -p option to write a pid file, you can stop it easily with:

    python3 -m pypgq stop -p /path/to/pidfile [mode]

This will read the pid from the pid file and send a kill signal, based on mode. Mode must be one of "current", "all", "now" which maps to SIGHUP, SIGINT, and SIGTERM respectively.

If you started the queue with -q greater than 1, all the child processes will be passed signals from the parent process.

See `python3 -m pypgq stop -h` for more details.


### Running Multiple Queues on One Schema

It is possible to have multiple queues running on a single set of tables. You can spawn multiple queue processes via the --queues command line option. There are two modes of cooperation:

1. Advisory Locks
2. Row Locks


#### Advisory Locks

Advisory lock cooperative mode uses Postgres' advisory lock functionality. You can configure the queue to use one of the two keyspaces either bigint, or (int, int) and each queue will obtain the given advisory lock before getting its next job.


#### Row Lock

If the queues are running on version 9.5+ of Postgres, you can use row locking mode, which utilizes the `select for update skip locked` functionality to keep jobs coordinated.

See the documentation of the pypgq.Queue.Cooperative class for more details.
