# ThemePro

Code that was developed for the demo of ThemePro. Please cite this paper if you use this tool for a scientific publication:

Dominguez, M., Soler, J., & Wanner, L. (2020, May). ThemePro: A Toolkit for the Analysis of Thematic Progression. In Proceedings of The 12th Language Resources and Evaluation Conference (pp. 1000-1007).

To run the demo, you will need a working Docker installation.

1) Build the docker with the following command (from the same directory where the Dockerfile is):

```
sudo docker build .
```

After building (it takes around 10-15 mins depending on your internet connection, so sit tight or go grab some coffee), you will see the following terminal output:

```
Step 22/22 : CMD ./launch.sh
 ---> Running in 304891c51eea
Removing intermediate container 304891c51eea
 ---> <DOCKER_ID>
Successfully built <DOCKER_ID>
```
Copy the DOCKER_ID, since you will need to input it in the following command.

2) Run it:
```
sudo docker run -p 4000:80 <DOCKER_ID>
```

3) Play with the demo! Access the demo using a browser and accessing:

```
http://localhost:4000/themePro/
```