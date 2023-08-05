# LogDiv: A Module for Diversity

LogDiv allows to calculate diversity of log files.

The initial purpose to calculate diversity is to study distributions of requests toward differents topics.

Diversity can be interpreted as the mesure of equilibrium in distributions. 

## Getting Started

### Prerequisites

DivPy requires:

* Python
* Numpy - Essential
* Pandas - Essential
* Matplotlib - Essential
* tqdm - Optionnal: progression bar
* Graph-tool - Optionnal: only one function requires it


```shell
$ pip install numpy
$ pip install panda
$ pip install matplotlib 
$ pip install tqdm 
```

### Installing

To install LogDiv, you need to execute:

```shell
$ pip install logdiv
```

### Entries format

LogDiv needs a specific format of entries to run:

- A file describing all requests under a table format, whose fields are:
* user ID
* timestamp
* requested page ID
* referrer page ID

- A file describing all pages visited under a table format, whose fields are:
* page ID
* topic 
* category

## Example

### Entries example
The following example illustrates the entries format of the package.

![](example.png)

| user ID |   timestamp       | requested page ID  | referrer page ID  |
| ------- |:-----------------:|:------------------:|-------------------|
| USER 1  | 2019-7-1 15:20:23 |         P2         |         P1        |
| USER 3  | 2019-7-1 15:20:27 |         P4         |         P2        |
| USER 1  | 2019-7-1 15:21:01 |         P3         |         P2        |
| USER 2  | 2019-7-1 15:23:30 |         P5         |         P3        |
| USER 2  | 2019-7-1 15:23:45 |         P1         |         P5        |

| page ID |   topic   | category  |
| ------- |:---------:|:----------|
|    P1   |  Football |  beginner |
|    P2   |  Tennis   |  pro      |
|    P3   |  Football |  beginner |
|    P4   |  Tennis   |  advanced |
|    P5   |  Rugby    |  medium   |

In that example, the topic is a sport and the category is the level of the sport. 

### Test of LogDiv

To check if the module is successfully installed, and see what kind of results can be obtained, you can run the script in section example, using the entries given in the same directory.

