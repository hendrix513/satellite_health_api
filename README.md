# satellite_health_api

Dependencies:
  Docker must be installed and running, and Docker Compose installed

To run webapp:
  from root of project:
  ```
  docker-compose up web --build
  ```

  Server runs on localhost:5000, so go to localhost:5000/health and localhost:5000/stats for health and stats endpoints

To run tests:
  from root of project:
  ```
  docker-compose up tests --build
  ```
