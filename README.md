# quickcam
a middleware based camera system that can be used for Dashcams or custom open-source home survailance systems



## Quickstart Web Portal (with Docker for testing)

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

## Building the cpp framework
> [!NOTE]
> you will need to have cyclonedds installed on your system, as its used as the middleware between modules.
> the `c++` version of cyclonedds can be found and installed from [here](https://github.com/eclipse-cyclonedds/cyclonedds-cxx)
```bash
mkdir  orchestrator/build
cd orchestrator
cmake -S . -B build
cmake --build .

```


## [Camera System Architecture](/camera/readme.md)
