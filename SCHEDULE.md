Day 1

    BACKEND: gRPC Service in Python for pulling/pushing financial data into a Postgres database
    COMPUTE: Python gRPC service that does numerical analysis on the financial data
    SCRAPPER: Simple Python service scrapping financial data and pushing to BACKEND
    REST API: Simple FAST API in Python fetching data from BACKEND
    CACHE: MongoDB as a caching layer
    PACKAGING
        Docker
        AWS Lambda using SAM
        Using Serverless (maybe)
    TESTING: Testing strategies for multi-layer apps


Day 2

    BACKEND: Replace Python BACKEND with C++
    COMPUTE: Replace Python with a C kernel wrapped in Python
    SCRAPPER: Replace with C++
    REST API: Replace with C++
    CACHE: Replace with C++
    PACKAGING:
        Docker
        AWS (maybe)
    TESTING: Replace with C++


Day 3

    Multi-layer docker builds
    C compute kernel compiler optimization
    When to write custom C kernels and when not to.
    Optimizing for repeatable builds, tests, etc. No more "It works on my machine"
    SQL Optimization
        Materialized Views
        Partitioning, Indexing, etc.
    Schema migration with SQL in CI/CD
    CI/CD practices
    Advanced testing strategies
        Unit test reuse
        Integration tests as e2e/smoke tests
        Chaos testing