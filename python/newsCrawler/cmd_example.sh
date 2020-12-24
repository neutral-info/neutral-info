docker run --rm  --shm-size 1G -e PYTHONUNBUFFERED=1 -v $PWD/Screenshots:/app/Screenshots facebook_group
docker run -d --rm  -e PYTHONUNBUFFERED=1 -v $PWD/data:/app/data test_facebook_fanpage