## Setup 

```
	Install Docker vs Docker Compose
```
## How To Run
```
**Build docker with docker-compose**
```
	docker build -t baomoi-scraper .
```
**Run docker**
```
	mkdir -p output && docker run -v $(pwd)/output:/app/output baomoi-scraper
```
