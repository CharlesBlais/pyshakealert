# Testing Alerting with ActiveMQ Artemis

As of May 2022, the ShakeAlert project is using Apache ActiveMQ v5 and are working towards using Apache ActiveMQ Artemis.  The following is testing instructions using docker (or podman) to start using ActiveMQ Artemis that will be used to distribute alerts to clients.  The following are key difference between the testing and the current production setup:

* ActiveMQ broker connections use SSL.  We opt not to distribute this with SSL to simplify setup/instructions.
* Artemis does not use "/topic/" topic prefix in STOMP

## Build the ActiveMQ Artemis

**Prerequisite** - git, docker (or podman)

The easier way to start testing is by building the ActiveMQ Artemis container.  To build, do the following.

```bash
git clone https://github.com/apache/activemq-artemis
cd activemq-artemis/artemis-docker
# follow the instructions in the readme or simply do the following example
# NOTE: the version below may change, look at https://downloads.apache.org/activemq/activemq-artemis/, for the latest number
./prepare-docker.sh --from-release --artemis-version 2.22.0
cd _TMP_/artemis/2.22.0
# with docker
docker build -f ./docker/Dockerfile-debian -t artemis-debian .
# or with podman
podman build -f ./docker/Dockerfile-debian --format docker -t artemis-debian .
```

## Running ActiveMQ Artemis

To run the broker, you must expose the ports that will be used for messaging.  The pyshakealert library uses STOMP protocol
therefore it is recommended to open that port on the container.  The list of ports can be found below.

```bash
# Run Artemis in the background (replace "docker" with "podman" for podman)
docker run -d -p 61613:61613 artemis-debian
# or Run Artermis in temporarily (easy cleanup)
docker run --rm -p 61613:61613 artemis-debian
```

The above will expose the port 61613 (2nd number) to the localhost system on port 61613 (1st number).

| Port  | Protocol |
| ----- | -------- |
| 1883  | MQTT |
| 61613 | STOMP |
| 61616 | CORE,MQTT,AMQP,HORNETQ,STOMP,OPENWIRE |

Important to note that this will use the default credentials username "artemis" and password "artemis" for your testing.  If you wish to use alternate credentials, see the documentation in the broker readme of using Environment Variables.

## Running a ShakeAlert scenarios

The library comes with a series of [scenarios](../scenarios) for you to test with.

To simplify the build and testing of the ShakeAlert project, we recommend you also use docker to run the exercise.

First, build the container

```bash
# from the root of this porject
# build the container with tag nrcan/pyshakealert
docker build -t nrcan/pyshakealert .
# or with podman
podman build -t nrcan/pyshakealert .
```

Second, run the container with the sample scenario.

```bash
docker run --rm -ti --network host -v `pwd`/scenarios:/scenarios nrcan/pyshakealert shake_play2shakealert -f /scenarios/test/play.csv -u artemis -p artemis --log-level DEBUG
# or with podman
podman run --rm -ti --network host -v `pwd`/scenarios:/scenarios nrcan/pyshakealert shake_play2shakealert -f /scenarios/test/play.csv -u artemis -p artemis --log-level DEBUG
```

The above will:

* "run" = run the newly built container
* "--rm" = self terminating container therefore remove it after run
* "-ti" = show terminal
* "--network" = use the hosts network in order to connect to the artermis broker
* "-v" = add a mount at the root of the /scenarios folder
* "shake_play2shakealert" = call the shake_play2shakealert executable with the scenario CSV file and credentials

The CSV contains the information regarding the ActiveMQ topics it will send too.  Your subscriber program must read from those topics.

### Listening to your scenario messages

For a quick test, you can listen to your test messages using the STOMP utility that also comes with the container.

```bash
docker run --rm -ti --network host nrcan/pyshakealert stomp -U artemis -W artemis -L eew.#
# or with podman
podman run --rm -ti --network host nrcan/pyshakealert stomp -U artemis -W artemis -L eew.#
```
