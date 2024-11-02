# RPi-Dashcam



## Quickstart (with Docker for testing)

Run

```sh
docker build -t pi-cam .
docker run -p 3000:80 pi-cam
```

Then open <localhost:3000> 🎈

## Deploying

Clone/copy the repo to the pi and run,

```sh
./setup.bash
```


## [Camera System Architecture](/camera/readme.md)