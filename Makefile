PROJ_NAME=todo-simpletrack
NGINX_CONF=nginx-todo-simpletrack
SYSTEMD_CONF=docker-todo-simpletrack.service
NGINX_CONF_PATH=/etc/nginx
SYSTEMD_CONF_PATH=/etc/systemd/system


dev: Dockerfile
	docker build -t tahabi/simpletrack:dev .
	docker run --name $(PROJ_NAME)-test --rm -v ~/projects/$(PROJ_NAME)/simpletrack.db:/app/simpletrack.db -v ~/projects/$(PROJ_NAME)/socket:/app/socket tahabi/simpletrack:dev
	docker stop -t 0 todo-simpletrack-test

prod: Dockerfile
	docker build -t tahabi/simpletrack:latest .
	docker run --name $(PROJ_NAME) -v ~/projects/$(PROJ_NAME)/simpletrack.db:/app/simpletrack.db -v ~/projects/$(PROJ_NAME)/socket:/app/socket tahabi/simpletrack:latest

place-nginx: nginx-todo-simpletrack
	sudo ln -s ~/projects/$(PROJ_NAME)/$(NGINX_CONF) $(NGINX_CONF_PATH)/sites-available/$(NGINX_CONF)
	sudo ln -s $(NGINX_CONF_PATH)/sites-available/$(NGINX_CONF) $(NGINX_CONF_PATH)/sites-enabled/$(NGINX-CONF)

place-systemd: docker-todo-simpletrack.service
	sudo ln -s ~/projects/$(PROJ_NAME)/$(SYSTEMD_CONF) $(SYSTEMD_CONF_PATH)/$(SYSTEMD_CONF)
