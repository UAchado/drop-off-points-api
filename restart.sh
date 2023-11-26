docker compose down -v
docker image rm mysql
docker image rm drop-off-points-api-drop-off-points-api
docker system prune --force
docker compose up --build